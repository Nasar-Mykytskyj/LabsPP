from flask import Flask, request, flash, redirect, url_for, render_template
import os
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='nemo',pw='nasar58n',url='127.0.0.1:5432',db='labpp')
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI']=DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
login_manager=LoginManager()
migrate=Migrate(app,db)






@app.route('/api/v1/hello-world-15')
@auth.login_required(role=['admin'])
def hello_world():
    return 'Hello World!'







if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
import views