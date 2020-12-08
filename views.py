from flask import request, jsonify, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, login_manager
import models
@login_manager.user_loader
def load_user(user_id):
    return models.db.session.query(models.User).get(user_id)

@app.route('/user', methods=['GET', 'POST']) #allow both GET and POST requests
def register_form():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        username = request.form.get('username')
        first_name = request.form['first_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        user = models.User.query.filter_by(username=username).first()
        if user:
            return "this user already registered"
        else:
            user = models.User(username, first_name, email, generate_password_hash(password), phone)
            try:
                models.db.session.add(user)
                models.db.session.commit()
            except Exception:
                models.db.session.rollback()
                return "problem with database", 404
        return "registered"

    return '''<form method="POST">
                  username: <input type="text" name="username"><br>
                  first_name: <input type="text" name="first_name"><br>
                  email: <input type="text" name="email"><br>
                  password: <input type="text" name="password"><br>
                  phone: <input type="text" name="phone"><br>
                  <input type="submit" value="Submit"><br>
                    
              </form>'''
@app.route('/user/<username>', methods=['DELETE'])
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

@app.route('/medicine', methods=['POST'])
def add_med():
    try:
        req_data = request.get_json()
        name=req_data['name']
        price=int(req_data['price'])
        number=int(req_data['number'])
        photo_url=req_data['url']
        description=req_data['description']
        med=models.Med.query.filter_by(name=name).first()
        if med:
            return "this med already registered"
        else:
            med=models.Med(name,price,number,photo_url,description)
            try:
                models.db.session.add(med)
                models.db.session.commit()
            except Exception:
                models.db.session.rollback()
                return "problem with database", 404
    except Exception:
        return "invalid data",400

    return "added" ,200
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
def delete_medicine_by_id(medicineId):
    try:
        models.Med.query.filter(models.Med.id==medicineId).delete()
        models.db.session.commit()
        return "deleted",200

    except Exception:
        models.db.session.rollback()
        return "invalid medicine id", 400
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
                login_user(user, remember=req_data)
                return "login",200
            else:
                return "wrong password"

    except Exception:
        return "invalid data", 400

@app.route('/logout/')
#@login_required
def logout():
    logout_user()

    return redirect(url_for('login'))



