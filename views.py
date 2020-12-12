from datetime import datetime

from flask import request, jsonify, flash, redirect, url_for, g
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, login_manager, auth
import models
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
@login_manager.user_loader
def load_user(user_id):
    return models.db.session.query(models.User).get(user_id)


@app.route('/user/<username>', methods=['DELETE'])
@auth.login_required(role=['admin'])
def delete_user_form(username):
    try:
        user=models.User.query.filter_by(username=username).first()
        if user is None:
            return "user,not found",404
        else:
            models.db.session.commit(user)
            models.db.session.commit()
    except Exception :
        models.db.session.rollback()
        return "invalid username",400
    return "deleted",200

@app.route('/user', methods=['POST']) #GET requests will be blocked
@required_params({
    "username":str,
    "first_name":str,
    "email":str,
    "password":str,
    "phone":str
})
def add_user():
    req_data = request.get_json()

    username = req_data['username']
    first_name = req_data['first_name']
    email = req_data['email']#two keys are needed because of the nested object
    password = req_data['password'] #an index is needed because of the array
    phone = req_data['phone']
    user = models.User.query.filter_by(username=username).first()
    if user:
        return "this user already registered"
    else:
        user =models.User(username,first_name,email,generate_password_hash(password),phone)
        try:
            models.db.session.add(user)
            models.db.session.commit()
        except Exception:
            models.db.session.rollback()
            return "problem with database", 404
    return "registered"
@app.route('/user/<username>', methods=['GET'])
def get_user_by_name(username):
    try:
        user = models.User.query.filter_by(username=username).first()
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
def add_med():
    try:
        req_data = request.get_json()
        med=models.Med.query.filter_by(name=req_data['name']).first()
        if med:
            return "this med already registered"
        else:

            med = models.Med(**req_data)
            try:
                models.db.session.add(med)
                models.db.session.commit()
            except Exception:
                models.db.session.rollback()
                return "problem with database", 404
    except Exception:
        return "invalid data",400

    return "added" ,200
@app.route('/medicine', methods=['PUT'])
def update_medicine():
    try:
        req_data = request.get_json()
        med = models.Med.query.filter_by(id=req_data['id']).first()
        if med is None:
            return "med not found", 404
        try:
            models.Med.query.filter_by(id=req_data['id']).update(dict(req_data['data']))
            models.db.session.commit()
        except Exception:
            models.db.session.rollback()
            return "invalid data",400
        return "updated",200
    except Exception:
        return "invalid data",400



@app.route('/medicine/<medicineId>', methods=['GET'])
def get_medicine_by_id(medicineId):
    try:
        med = models.Med.query.filter_by(id=medicineId).first()
        if med is None:
            return "med not found",404
        return jsonify(med),200

    except Exception:
        return "invalid medicine id",400

@app.route('/medicine/<medicineId>', methods=['DELETE'])
@auth.login_required(role=['admin'])
def delete_medicine_by_id(medicineId):
    try:
        models.Med.query.filter(models.Med.id==medicineId).delete()
        models.db.session.commit()
        return "deleted",200

    except Exception:
        models.db.session.rollback()
        return "invalid medicine id", 400


@app.route('/store/order', methods=['POST','GET'])
@required_params({
    "user_id":int,
    "medicine_id":int
})
def add_order():
    try:
        req_data = request.get_json()
        try:
            order=models.Order(**req_data,ship_date=datetime.today())
            models.db.session.add(order)
            models.db.session.commit()
        except Exception:
            models.db.session.rollback()
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
    user = models.User.query.filter_by(username=aut_user).first()
    return user.roles

@auth.verify_password
def verify_password(username, password):
    user = models.User.query.filter_by(username=username).first()
    if user and \
            check_password_hash(user.password, password):
        return username

@app.route('/')
@auth.login_required(role=['user'])
def index():
    return "Hello, %s!" % auth.current_user()
@app.route('/logout')
def logout():

    return redirect("http://none:none@127.0.0.1:5000")

if __name__ == '__main__':
    app.run()




