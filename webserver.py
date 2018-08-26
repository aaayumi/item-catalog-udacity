from flask import Flask, render_template, request,redirect,url_for,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Recipe
app = Flask(__name__)

engine = create_engine('sqlite:///category.db',connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/categories/<int:category_id>/menu/JSON')
def categoryMenuJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Recipe).filter_by(
        category_id=category_id).all()
    return jsonify(Recipe=[i.serialize for i in items]
    )

@app.route('/category/<int:category_id>/menu/<int:recipe_id>/JSON')
def recipeJSON(category_id, recipe_id):
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    return jsonify(Recipe=recipe.serialize)

@app.route('/')
@app.route('/categories/<int:category_id>/menu')
def categoryList(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    recipes = session.query(Recipe).filter_by(category_id=category.id)
    # output = "a"
    return render_template('category.html', category=category, recipes=recipes)

@app.route('/category/<int:category_id>/new/',methods=['GET','POST'])
def newRecipe(category_id):
   if request.method == 'POST':
       newRecipe = Recipe(
           name=request.form['name'], category_id=category_id)
       session.add(newRecipe)
       session.commit()
       return redirect(url_for('categoryMenu', category_id=category_id))
   else:
       return render_template('add_recipe.html',category_id=category_id)

@app.route('/category/<int:category_id>/<int:recipe_id>/edit/',methods=['GET','POST'])
def editRecipe(category_id, recipe_id):
    editRecipe = session.query(Recipe).filter_by(id=recipe_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editRecipe.name = request.form['name']
        session.add(editRecipe)
        session.commit()
        return redirect(url_for('categoryList', category_id=category_id))
    else:
        return render_template(
            'edit_recipe.html', category_id=category_id, recipe_id=recipe_id, item=editRecipe)

@app.route('/category/<int:category_id>/<int:recipe_id>/delete/', methods=['GET','POST'])
def deleteRecipe(category_id, recipe_id):
    deleteRecipe = session.query(Recipe).filter_by(id=recipe_id).one()
    if request.method == 'POST':
        session.delete(deleteRecipe)
        session.commit()
        return redirect(url_for('categoryList', category_id=category_id))
    else:
        return render_template(
            'delete_recipe.html', item=deleteRecipe)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)