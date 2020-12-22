from datetime import datetime

from flask import request, jsonify, flash, redirect, url_for, g

from werkzeug.security import generate_password_hash, check_password_hash

from app import app, auth, db, User, Med, Order

from functools import wraps
def required_params(required):

    def decorator(fn):



        @wraps(fn)

        def wrapper(*args, **kwargs):

            _json = request.get_json()

            missing = [r for r in required.keys()

                       if r not in _json]

            if missing:

                response = {

                    "status": "error",

                    "message": "Request JSON is missing some required params",

                    "missing": missing

                }

                return jsonify(response), 400

            wrong_types = [r for r in required.keys()

                           if not isinstance(_json[r], required[r])]

            if wrong_types:

                response = {

                    "status": "error",

                    "message": "Data types in the request JSON doesn't match the required format",

                    "param_types": {k: str(v) for k, v in required.items()}

                }

                return jsonify(response), 400

            return fn(*args, **kwargs)

        return wrapper

    return decorator



@app.route('/user/<id>', methods=['DELETE'])
@auth.login_required(role=['admin'])
def delete_user_form(id):
    try:
        User.query.filter_by(id = id).delete()
        db.session.commit()
        return "deleted", 200

    except Exception:
        db.session.rollback()
        return "invalid user id", 400

@app.route('/user', methods=['POST']) #GET requests will be blocked
@required_params({
    "username":str,
    "first_name":str,
    "email":str,
    "password":str,
    "phone":str,
    "roles":str
})
def add_user():
    req_data = request.get_json()

    username = req_data['username']
    first_name = req_data['first_name']
    email = req_data['email']#two keys are needed because of the nested object
    password = req_data['password'] #an index is needed because of the array
    phone = req_data['phone']
    roles=req_data['roles']
    user = User.query.filter_by(username=username).first()
    if user:
        return "this user already registered"
    else:
        user =User(username,first_name,email,generate_password_hash(password),phone,roles)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return "problem with database", 404
    return "registered"
@app.route('/user/<username>', methods=['GET'])
@auth.login_required(role=['user','admin'])
def get_user_by_name(username):
    try:
        user =User.query.filter_by(username=username).first()
        if user is None:
            return "user not found",404
        return jsonify(user.id,user.first_name,user.phone,user.email),200

    except Exception:
        return "invalid username",400

@app.route('/medicine', methods=['POST'])
@required_params({
    "name":str,
    "price":int,
    "number":int,
    "photo_url":str,
    "description":str

})
@auth.login_required(role=['admin'])
def add_med():
    try:
        req_data = request.get_json()
        med=Med.query.filter_by(name=req_data['name']).first()
        if med:
            return "this med already registered"
        else:

            med = Med(**req_data)
            try:
                db.session.add(med)
                db.session.commit()
            except Exception:
                db.session.rollback()
                return "problem with database", 404
    except Exception:
        return "invalid data",400

    return "added" ,200
@app.route('/medicine', methods=['PUT'])
@auth.login_required(role=['admin'])
def update_medicine():
    try:
        req_data = request.get_json()
        med = Med.query.filter_by(id=req_data['id']).first()
        if med is None:
            return "med not found", 404
        try:
            Med.query.filter_by(id=req_data['id']).update(dict(req_data['data']))
            db.session.commit()
        except Exception:
            db.session.rollback()
            return "invalid data",400
        return "updated",200
    except Exception:
        return "invalid data",400



@app.route('/medicine/<medicineId>', methods=['GET'])

def get_medicine_by_id(medicineId):
    try:
        med = Med.query.filter_by(id=medicineId).first()
        if med is None:
            return "med not found",404
        return jsonify(med.name,med.price,med.number,med.description),200

    except Exception:
        return "invalid medicine id",400

@app.route('/medicine/<medicineId>', methods=['DELETE'])
@auth.login_required(role=['admin'])
def delete_medicine_by_id(medicineId):
    try:
        Med.query.filter(Med.id==medicineId).delete()
        db.session.commit()
        return "deleted",200

    except Exception:
        db.session.rollback()
        return "invalid medicine id", 400


@app.route('/store/order', methods=['POST','GET'])
@auth.login_required(role=['user','admin'])
@required_params({
    "user_id":int,
    "medicine_id":int
})
def add_order():
    try:
        req_data = request.get_json()
        try:
            order=Order(**req_data,ship_date=datetime.today())
            db.session.add(order)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return "problem with database", 404
        return "added order",200
    except Exception:
        return "invalid data",400
"""""
@app.route('/user/login', methods=['POST','GET'])
def login():
    try:
        req_data = request.get_json()
        username = req_data['username']
        password=req_data['password']
        user=models.User.query.filter_by(username=username).first()
        if user is None:
            return "user,not found"
        else:
            if  check_password_hash(user.password,password):
                login_user(user)
                return "login",200
            else:
                return "wrong password"

    except Exception:
        return "invalid data", 400
"""""
@auth.get_user_roles
def get_user_roles(aut_user):
    user = User.query.filter_by(username=aut_user).first()
    return user.roles

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and \
            check_password_hash(user.password, password):
        return username

@app.route('/user/login')
@auth.login_required(role=['user','admin'])
def index():
    return "Hello, %s!" % auth.current_user()
@app.route('/logout')
@auth.login_required(role=['user','admin'])
def logout():

    return redirect("http://none:none@127.0.0.1:5000")





