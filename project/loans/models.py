from project import app, db



class Loans(db.Model):
    
    loans_id = db.Column(db.Integer, primary_key=True)
    customer= db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    book= db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    loandate = db.Column(db.Integer,nullable=False) 
    returndate = db.Column(db.Date, nullable=False)
    returned = db.Column(db.String, nullable=False)

    def __init__(self,customer,book,loandate, returndate,returned):
        
        self.customer = customer
        self.book= book
        self.loandate = loandate
        self.returndate = returndate
        self.returned = returned


with app.app_context():
        db.create_all()