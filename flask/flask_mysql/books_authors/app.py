from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 
from flask_migrate import Migrate 
app = Flask(__name__)

# flask db init
#flask db upgrade

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_authors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#instance of the ORM
db =  SQLAlchemy(app)
migrate = Migrate(app, db)

book_authors = db.Table('book_authors', \
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True), \
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True))
class Book(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(245))
    description = db.Column(db.String(245))
    author_of_this_book = db.relationship('Author', secondary=book_authors)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Author(db.Model):	
    # f__tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(145))
    last_name = db.Column(db.String(145))
    notes = db.Column(db.String(245))
    books_of_this_author = db.relationship('Book', secondary=book_authors)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


@app.route("/")
def index():
    list_of_all_books = Book.query.all()
    
    return render_template("books.html", books= list_of_all_books,)

@app.route("/add_book", methods =["POST"])
def newbook():
   
    new_instance_of_a_book = Book(
        title=request.form['title'],
        description=request.form['description'])
    db.session.add(new_instance_of_a_book)
    db.session.commit()

    return redirect("/")

@app.route("/authors")
def authors():
   
    list_of_all_authors = Author.query.all()
    
    return render_template("authors.html", authors= list_of_all_authors)

@app.route("/add_author", methods =["POST"])
def newauthor():
   
    new_instance_of_author = Author(first_name=request.form['first_name'], last_name=request.form['last_name'], \
        notes=request.form['note'])
    db.session.add(new_instance_of_author)
    db.session.commit()

    return redirect("/authors")

@app.route("/books/<id>")
def show_books_page(id):
    print (id)
    this_book = Book.query.filter_by(id = id).first()
    authors_of_this_book = db.session.query(Book, Author).join(Author, Book.author_of_this_book).filter(Book.id == id).all()
    list_of_all_authors = Author.query.all()
    print (authors_of_this_book)
    # mysql = connectToMySQL('new_friends')
    # query = "Select * from new_friends.friends where id = {};".format(int(user_id))
    

    return render_template("show_book.html", book = this_book, book_authors= authors_of_this_book, authors= list_of_all_authors)

@app.route("/authors/<id>")
def show_authors_page(id):
    print (id)
    this_author = Author.query.filter_by(id = id).first()
    book_of_this_author = db.session.query(Author, Book).join(Book, Author.books_of_this_author).filter(Author.id == id).all()
    list_of_all_books = Book.query.all()
    print (book_of_this_author)
    # mysql = connectToMySQL('new_friends')
    # query = "Select * from new_friends.friends where id = {};".format(int(user_id))
    

    return render_template("show_author.html", author = this_author, author_books= book_of_this_author, books= list_of_all_books)

@app.route("/add_book_to_author", methods =["POST"])
def add_book_to_author():
    author_id = request.form["author_id"]
    this_author = Author.query.get(author_id)
    books_to_add= Book.query.get(request.form["book_id"])
    this_author.books_of_this_author.append(books_to_add)
    db.session.commit()

    return redirect ( "/authors/{}".format(int(author_id)))

    
@app.route("/add_author_to_book", methods =["POST"])
def add_author_to_book():
    book_id = request.form["book_id"]
    print(request.form["author_id"])
    this_book = Book.query.get(book_id)
    authors_to_add= Author.query.get(request.form["author_id"])
    this_book.author_of_this_book.append(authors_to_add)
    db.session.commit()

    # mysql = connectToMySQL('new_friends')
    # query = "Select * from new_friends.friends where id = {};".format(int(user_id))
    

    return redirect ( "/books/{}".format(int(book_id)))

if __name__== "__main__":
    app.run(debug=True)