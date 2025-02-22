from app import db

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    address = db.Column(db.String(200),nullable=True)
