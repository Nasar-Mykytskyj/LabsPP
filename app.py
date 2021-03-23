from flask import Flask, request, flash, redirect, url_for, render_template

from flask_httpauth import HTTPBasicAuth
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin



app = Flask(__name__)
app.debug = True
Scss(app, static_dir='static', asset_dir='assets')

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='nemo',pw='nasar58n',url='127.0.0.1:5432',db='labpp')
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI']=DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)



class User( db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(45))
    first_name = db.Column(db.VARCHAR(45))
    email = db.Column(db.VARCHAR(45))
    password = db.Column(db.VARCHAR(255))
    phone = db.Column(db.VARCHAR(45))
    orders=db.relationship('Order', backref='user', lazy=True)
    roles=db.Column(db.VARCHAR(10))
    def __init__(self,username=None,first_name=None,email=None,password=None,phone=None,roles=None):
        self.username=username
        self.first_name=first_name
        self.email=email
        self.password=password
        self.phone=phone
        self.roles=roles



    def __repr__(self):
        return '<User %s %s %s %s %s>' % (self.username, self.first_name, self.email, self.password, self.phone)

class Med(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(45))
    price=db.Column(db.Integer)
    number=db.Column(db.Integer)
    photo_url=db.Column(db.VARCHAR(60))
    description=db.Column(db.TEXT)
    orders= db.relationship('Order', backref='med', lazy=True)
    def __init__(self,name=None,price=None,number=None,photo_url=None,description=None):
        self.name=name
        self.price=price
        self.number=number
        self.photo_url=photo_url
        self.description=description

    def __repr__(self):
        return  '<Med %s %s %s %s %s>' % (self.name,self.price,self.number,self.photo_url,self.description)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    ship_date=db.Column(db.DATE)
    user_id=db.Column(db.Integer , db.ForeignKey('users.id'),nullable=False)
    medicine_id=db.Column(db.Integer,db.ForeignKey('medicine.id'),nullable=False)


    def __init__(self,id=None,user_id=None,medicine_id=None,ship_date=None):
        self.ship_date=ship_date
        self.user_id=user_id
        self.medicine_id=medicine_id

    def __repr__(self):
        return '<Order %s %s %s >' % (self.ship_date,self.user_id,self.medicine_id)


import views
if __name__ == '__main__':
    app.run(debug=True)
