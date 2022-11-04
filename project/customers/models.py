from project import app, db



class Customers(db.Model):
    
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    bdate = db.Column(db.Integer, nullable=False)
    loans = db.relationship('Loans', backref='customers')

    def __init__(self,customer_name,phone,email,address,bdate):
        
        self.customer_name = customer_name
        self.phone = phone
        self.email = email
        self.address = address
        self.bdate = bdate
        


with app.app_context():
        db.create_all()