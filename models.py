from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt
from sqlalchemy import Enum
from sqlalchemy.orm import validates

db = SQLAlchemy()
bcrypt = Bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True )
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(Enum('male', 'female', name='gender_enum'), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    contact = db.Column(db.Integer, nullable=False)

@validates('gender')
def validate_gender(self, key, value):
    assert value in ['male', 'female'], "Gender must be male or female"
    return value

class Message(db.Model, SerializerMixin):
     __tablename__ = 'messages'
     id = db.Column(db.Integer, unique=True, primary_key=True)
     name = db.Column(db.String(100), unique=True, nullable=False)
     email = db.Column(db.String(100), unique=True, nullable=False)
     comment = db.Column(db.String, nullable=False)

class Pharmacy(db.Model, SerializerMixin):
    __tablename__ = 'pharmacy'
    
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))

    drugs = db.relationship ('Drug', back_populates='pharmacy')

class Drug(db.Model, SerializerMixin):
    __tablename__ = 'drugs'
    
    id = db.Column(db.Integer, unique=True, primary_key=True)
    pharmacy_name = db.Column(db.String(100), db.ForeignKey('pharmacy.name'))
    drug_category = db.Column(db.string, nullable=False)
    drug_name = db.Column(db.string, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)


    reviews = db.relationship('Review', back_populates='drug')
    orders = db.relationship('Order', back_populates='drug')

    pharmacy = db.relationship('Pharmacy', back_populates='drugs')


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'))
    comment = db.Column(db.String(250), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    drug = db.relationship('Drug', back_populates='reviews')
    
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    drug_id = db.Column(db.Integer, db.ForeignKey('drugs.id'))
    total_price = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='orders')
    drug = db.relationship('Drug', back_populates='orders')
