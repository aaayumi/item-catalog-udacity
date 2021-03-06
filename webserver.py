from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   jsonify,
                   make_response)
from functools import wraps
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Recipe, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine('sqlite:///category.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create User
def createUser(login_session):
    """Create a new user and store it in User DB"""
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def login_required(func):
    """Decorator to check if user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    return wrapper

@app.route('/login')
def showLogin():
    """Redirect to login page"""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Get user's information for login"""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['user_id'] = createUser(login_session)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;' \
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Use Google Sign In API to allow login"""
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token Is None'
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        categories = session.query(Category).all()
        recipes = session.query(Recipe).order_by(Recipe.id.desc()).limit(5)
        return render_template('public_catalog.html',
                               categories=categories,
                               recipes=recipes)
    else:
        response = make_response(json.dumps
                                 ('Failed to revoke token for given user'),
                                 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON FILE
@app.route('/categories/<int:category_id>/JSON')
def categoryMenuJSON(category_id):
    """JSON file for each category"""
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Recipe).filter_by(
        category_id=category_id).all()
    return jsonify(Recipe=[i.serialize for i in items]
                   )


@app.route('/categories/<int:category_id>/<int:recipe_id>/JSON')
def recipeJSON(category_id, recipe_id):
    """JSON file for each recipe"""
    recipe = session.query(Recipe).filter_by(id=recipe_id).one_or_none()
    return jsonify(Recipe=recipe.serialize)


# MAIN PAGE
@app.route('/')
@app.route('/catalog/')
def showCategories():
    """Show category for not loggined user,
       show category with adding capability for loginned user"""
    categories = session.query(Category).all()
    recipes = session.query(Recipe).order_by(Recipe.id.desc()).limit(5)
    is_logged_in = 'username' not in login_session
    return render_template('catalog.html',
                           categories=categories,
                           recipes=recipes,
                           is_logged_in=is_logged_in)


# SHOW CATEGORY PAGE
@app.route('/<int:category_id>')
@app.route('/catalog/<int:category_id>')
def categoryList(category_id):
    """Show all categories and latest added recipes"""
    category = session.query(Category).filter_by(id=category_id).one_or_none()
    recipes = session.query(Recipe).filter_by(category_id=category_id)
    return render_template('category.html',
                           category=category,
                           category_id=category_id,
                           recipes=recipes)


# SHOW RECIPE PAGE
@app.route('/catalog/<int:category_id>/<int:recipe_id>')
def showRecipe(category_id, recipe_id):
    """Show recipes per category"""
    showRecipe = session.query(Recipe).filter_by(id=recipe_id).one_or_none()
    return render_template('recipe.html',
                           category_id=category_id,
                           recipe_id=recipe_id,
                           item=showRecipe)


# ADD RECIPE PAGE
@app.route('/catalog/<int:category_id>/new', methods=['GET', 'POST'])
@login_required
def newRecipe(category_id):
    """Create new recipe to the database
    Returns:
        on GET: Page to create a new recipe.
        Authentication: Redirect to Login page if user is not signed in.
        on POST: Redirect to main page after recipe has been created.
        """

    if request.method == 'POST':
        newRecipe = Recipe(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['categories_id'],
            user_id=login_session['user_id'])
        session.add(newRecipe)
        session.commit()
        return redirect(url_for('categoryList',
                                category_id=category_id))
    else:
        return render_template('add_recipe.html',
                               category_id=category_id)


# EDIT RECIPE PAGE
@app.route('/catalog/<int:category_id>/<int:recipe_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editRecipe(category_id, recipe_id):
    """Edit the recipe that the user created
      Returns:
          on GET: Page to create a edit recipe.
          Authentication: Redirect to Login page if user is not signed in.
          Authorization: Redirect to main page
                         if user is not the owner of recipe.
          on POST: Redirect to main page after recipe has been edited.
          """

    editRecipe = session.query(Recipe).filter_by(id=recipe_id).one_or_none()

    # Authorization check
    if editRecipe.user_id != login_session['user_id']:
        redirect(url_for('categoryList', category_id=category_id))

    if request.method == 'POST':
        if request.form['name'] == "":
            editRecipe.name = editRecipe.name
        else:
            editRecipe.name = request.form['name']

        session.add(editRecipe)
        session.commit()
        return redirect(url_for('categoryList', category_id=category_id))
    else:
        return render_template(
            'edit_recipe.html', category_id=category_id,
            recipe_id=recipe_id,
            item=editRecipe)


# DELETE RECIPE PAGE
@app.route('/catalog/<int:category_id>/<int:recipe_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteRecipe(category_id, recipe_id):
    """Delete the recipe that the user created
       Returns:
           on GET: Page to create a delete recipe.
           Authentication: Redirect to Login page if user is not signed in.
           Authorization: Redirect to main page
           if user is not the owner of recipe.
           on POST: Redirect to main page after recipe has been deleted.
           """

    deleteRecipe = session.query(Recipe).filter_by(id=recipe_id).one_or_none()

    # Authorization check
    if deleteRecipe.user_id != login_session['user_id']:
        redirect(url_for('categoryList', category_id=category_id))

    if request.method == 'POST':
        session.delete(deleteRecipe)
        session.commit()
        return redirect(url_for('categoryList',
                                category_id=category_id))
    else:
        return render_template(
            'delete_recipe.html', item=deleteRecipe)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
