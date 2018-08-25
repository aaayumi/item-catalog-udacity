from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Category, Recipe
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///category.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/category/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a new Category<h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/category/new'>"
                output += "<input name = 'newCategoryName' type= 'text' placeholder='New Category Here'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                categoryIDPath = self.path.split("/")[2]
                myCategoryQuery = session.query(Category).filter_by(
                    id=categoryIDPath).one()
                if myCategoryQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myCategoryQuery.name
                    output += "<h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % categoryIDPath
                    output += "<input name= 'newCategoryName' type='text' placeholder='%s'>" % myCategoryQuery.name
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                categoryIDPath = self.path.split("/")[2]

                myCategoryQuery = session.query(Category).filter_by(
                    id=categoryIDPath).one()
                if myCategoryQuery:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % myCategoryQuery.name
                    output += "<form method='POST' enctype= 'multipart/form-data' action='/category/%s/delete'>" % categoryIDPath
                    output += "<input type='submit' value='Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            if self.path.endswith("/category"):
                categories = session.query(Category).all()
                output = ""
                output += "<a href='/category/new'> Make a new Category here</a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for category in categories:
                    output += "</br>"
                    output += category.name
                    output += "</br>"
                    output += "<a href='/category/%s/edit'>Edit</a> " % category.id
                    output += "</br>"
                    output += "<a href='/category/%s/delete'>Delete</a>" % category.id
                output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endwith("/delete"):
                categoryIDPath = self.path.split("/")[2]
                myCategoryQuery = session.query(Category).filter_by(
                    id=categoryIDPath).one()
                if myCategoryQuery:
                    session.delete(myCategoryQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location','/category')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCategoryName')
                    categoryIDPath = self.path.split("/")[2]

                    myCategoryQuery = session.query(Category).filter_by(
                        id=categoryIDPath).one()
                    if myCategoryQuery != []:
                        myCategoryQuery.name = messagecontent[0]
                        session.add(myCategoryQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location','/category')
                        self.end_headers()

            if self.path.endwith("/category/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCategoryName')

                    newCategory = Category(name=messagecontent[0])
                    session.add(newCategory)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type','text/html')
                    self.send_header('Location','/category')
                    self.end_headers()
        except:
            pass

def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print 'Web server running...open localhost:8080/category in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
