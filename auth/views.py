from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from werkzeug.security import generate_password_hash

from . import auth
from ..models import User
from ..models import db
from .forms import  RegistrationForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    name = data['username']
    password = data['password']
    firstname=data['firstname']
    email=data['email']

    user = User.query.filter_by(username=name).first()
    if user:
        return "this user already registered"

    new_user = User(username=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return "this user already registered"

