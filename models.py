from app import db

class User( db.Model ):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(45))
    first_name = db.Column(db.VARCHAR(45))
    email = db.Column(db.VARCHAR(45))
    password = db.Column(db.VARCHAR(45))
    phone = db.Column(db.VARCHAR(45))
    orders=db.relationship('Order', backref='user', lazy=True)
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

    def __repr__(self):
        return  '<Med %s %s %s %s %s>' % (self.name,self.price,self.number,self.photo_url,self.description)
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    ship_date=db.Column(db.DATE)
    user_id=db.Column(db.Integer , db.ForeignKey('users.id'),nullable=False)
    medicine_id=db.Column(db.Integer,db.ForeignKey('medicine.id'),nullable=False)

    def __repr__(self):
        return '<Order %s %s %s >' % (self.ship_date,self.user_id,self.medicine_id)


