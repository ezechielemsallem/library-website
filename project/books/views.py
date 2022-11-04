import json
from flask import render_template, url_for, redirect, Blueprint, request
from project import db
from project.customers.models import Customers
from project.books.models import Books


books = Blueprint('books', __name__, template_folder='templates', url_prefix='/books')

#url for show all books or just one book
@books.route("/all_books/<index>")
@books.route("/all_books/")
def all_books(index =-1):
    if int(index) > -1:
        book = Books.query.get(int(index))
        return  render_template('book.html',book= book)
    return render_template('all_book.html',count_books=Books.query.count(), Books= Books.query.all()) 

#url for add a book with form html
@books.route("/add_book/", methods=['GET', 'POST'])
def add_a_book():
    if request.method == "POST":
       
       book_name = request.form.get("book_name")
       author = request.form.get("author")
       year = request.form.get("year")
       type = request.form.get("type")

       new_book= Books(book_name,author,year,type)
       db.session.add (new_book)
       db.session.commit()
       return redirect(url_for('books.all_books')) 
    return render_template('add_book.html')

#url for delete book whith his ID
@books.route("/del_book/<ind>", methods=['DELETE','GET'])
def del_student(ind=-1):
        book=Books.query.get(int(ind))
        try: 
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for('books.all_books')) 
        except:
            return render_template('cant_delete_book.html' , link = "http://127.0.0.1:5000/books/all_books/")


#url for search book with his name 
@books.route("/search_book/", methods=['GET', 'POST'])
def search_book():
    if request.method == "POST":
       book= request.form.get("book_name")
       my_user = Books.query.filter_by(book_name= book).first()
       if my_user:
        return  render_template('book.html',book= my_user)
       return  render_template('not_found.html', object =book, link = "http://127.0.0.1:5000/books/all_books/")
    return render_template('search_book.html' )

#url for modify information of book
@books.route("/upload_book/" ,methods=[ 'POST'])
@books.route("/upload_book/<index>/", methods=['GET', 'POST'])
def upload_book(index=-1):
    if request.method == "GET":
        book=Books.query.get(int(index))
        return render_template('upload_book.html', book=  book)
    if request.method == "POST":
        book_id=request.form["book_id"]
        book=Books.query.get(book_id)
        book.book_name  = request.form.get('book_name', type=str)
        book.author = request.form.get("author")
        book.year = request.form.get("year")
        book.type = request.form.get("type")
        db.session.commit()
        return redirect(url_for('books.all_books')) 