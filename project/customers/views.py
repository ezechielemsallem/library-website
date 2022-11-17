from cgitb import text
from itertools import count
import json
import string
from project.customers.models import Customers
from flask import render_template, url_for, redirect, Blueprint, request
from project import db
from sqlalchemy import update


customers = Blueprint('customers', __name__, template_folder='templates', url_prefix='/customers')

@customers.route("/all_customers/<index>")
@customers.route("/all_customers/")
def all_customers(index =-1):
    if int(index) > -1:
        customer = Customers.query.get(int(index))
        return  render_template('customer.html',customer= customer)
    return render_template('all_customer.html' ,count_customers=Customers.query.count(),customers_list = Customers.query.all())



@customers.route("/add_customer/", methods=['GET', 'POST'])
def add_customer():
    if request.method == "POST":
       customer_name = request.form.get("customer_name")
       phone = request.form.get("phone")
       email = request.form.get("email")
       address = request.form.get("address")
       bdate = request.form.get("bdate")
       new_customer= Customers(customer_name,phone,email,address,bdate)
       db.session.add (new_customer)
       db.session.commit()
       return redirect(url_for('customers.all_customers'))
    return render_template('add_customer.html')


@customers.route("/del_customer/<ind>", methods=['DELETE','GET'])
def del_customer(ind=-1):
        customer=Customers.query.get(int(ind))
        try : 
                db.session.delete(customer)
                db.session.commit()
                return redirect(url_for('customers.all_customers'))
        except : 
            return render_template('cant_delete_customer.html', link = "https://my-library-49wh.onrender.com/customers/all_customers/")


@customers.route("/search_customer/", methods=['GET', 'POST'])
def search_customer():
    if request.method == "POST":
       customer= request.form.get("customer_name")
       my_user = Customers.query.filter_by(customer_name= customer).first()
       if my_user:
        return  render_template('customer.html',customer= my_user)
       return render_template('not_found.html', object =customer, link = "https://my-library-49wh.onrender.com/customers/all_customers/")
    return render_template('search_customer.html')

@customers.route("/upload_customer/" ,methods=[ 'POST'])
@customers.route("/upload_customer/<index>/", methods=['GET', 'POST'])
def upload_customer(index=-1):
    if request.method == "GET":
        customer=Customers.query.get(int(index))
        return render_template('upload.html', customer=customer)
    if request.method == "POST":
        customer_id=request.form["customer_id"]
        customer=Customers.query.get(customer_id)
        customer.customer_name  = request.form.get('customer_name')
        customer.phone = request.form.get("phone")
        customer.email = request.form.get("email")
        customer.address = request.form.get("address")
        customer.bdate = request.form.get("bdate")
        db.session.commit()
        return redirect(url_for('customers.all_customers'))
    
   
   

  


