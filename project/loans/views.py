import datetime
import json
from flask import render_template, url_for, redirect, Blueprint, request
from project import  db
from project.books.models import Books
from project.customers.models import Customers
from project.loans.models import Loans
from datetime import datetime, timedelta
import datetime



loans = Blueprint('loans', __name__, template_folder='templates', url_prefix='/loans')

#url for watch all loans 
@loans.route("/all_loans/")
def all_loans(ind =-1):
    loans_active= Loans.query.filter(Loans.returned == 'Not returned')
    loans_late = Loans.query.filter(Loans.returndate < datetime.date.today(), Loans.returned == 'Not returned' )
    all_Loans= Loans.query.all()
    count_loans_active = Loans.query.filter(Loans.returned == 'Not returned').count()
    count_loans_late = Loans.query.filter(Loans.returndate < datetime.date.today(), Loans.returned == 'Not returned' ).count()
    count_loans= Loans.query.count()
    return render_template('all_loans.html',count_loans_active =count_loans_active,count_loans_late=count_loans_late, loans_active= loans_active ,loans_late = loans_late ,count_loans=count_loans ,all_Loans= all_Loans)  


#url for add one loan with html form
@loans.route("/add_loan/", methods=['GET', 'POST'])
def add_loan():
    if request.method == "POST":
       customer = request.form.get("customer")
       book = request.form.get("book")
       loandate = request.form.get("loandate")
       my_user = Books.query.filter_by(book_id= book).first()
       if my_user.type == 1 :
        returndate =  datetime.datetime.strptime(loandate, '%Y-%m-%d') + timedelta(days=5)
       elif my_user.type == 2 :
        returndate =  datetime.datetime.strptime(loandate, '%Y-%m-%d') + timedelta(days=10)
       elif my_user.type == 3 :
        returndate =  datetime.datetime.strptime(loandate, '%Y-%m-%d') + timedelta(days=15)
       returned = "Not returned"
       new_loan= Loans(customer,book,loandate,returndate,returned)
       db.session.add (new_loan)
       db.session.commit()
       return redirect(url_for('loans.all_loans')) 
    return render_template('add_loan.html',  customers_list = Customers.query.all(), Books= Books.query.all()) 



#url for delete one loan with his ID
@loans.route("/del_loan/<ind>", methods=['DELETE','GET'])
def del_loan(ind=-1):
        loan=Loans.query.get(int(ind))
        if loan:
            db.session.delete(loan)
            db.session.commit()
            return redirect(url_for('loans.all_loans')) 
        return redirect(url_for('loans.all_loans'))
       
        
#url for search loan with ID 
@loans.route("/search_loan/", methods=['GET', 'POST'])
def search_loan():
    if request.method == "POST":
       loan= request.form.get("loans_id")
       my_user = Loans.query.filter_by(loans_id= loan).first() 
       if my_user:
        return  render_template('new_loan.html',loan= my_user)
       return render_template('not_found.html', object =f'Loan number {loan}', link = "http://127.0.0.1:5000/loans/all_loans/")
    return render_template('search_loan.html') 


#url for modify information of one loan 
@loans.route("/upload_loan/" ,methods=[ 'POST'])
@loans.route("/upload_loan/<index>/", methods=['GET', 'POST'])
def upload_loan(index=-1):
    if request.method == "GET":
        loan=Loans.query.get(int(index))
        return render_template('upload_loan.html', loan=loan, customers_list = Customers.query.all(), Books= Books.query.all())
    if request.method == "POST":
        loans_id=request.form["loans_id"]
        loan=Loans.query.get(loans_id)
        loan.customer  = request.form.get('customer')
        loan.book = request.form.get("book")
        loan.loandate = request.form.get("loandate")
        loan.returndate = datetime.datetime.strptime(request.form.get("returndate"), '%Y-%m-%d')
        loan.returned = request.form.get("returned")
        db.session.commit()
        return redirect(url_for('loans.all_loans'))



#url for change if book are returned or not 
@loans.route("/return_book/<index>/", methods=['GET', 'PUT'])
def upload_returned (index = -1):
    loan=Loans.query.get(int(index))
    loan.returned = "returned"
    db.session.commit()
    return redirect(url_for('loans.all_loans')) 


