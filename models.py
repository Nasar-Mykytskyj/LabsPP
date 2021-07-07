from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
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
    def __init__(self,username,first_name,email,password,phone):
        self.username=username
        self.first_name=first_name
        self.email=email
        self.password=password
        self.phone=phone




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


