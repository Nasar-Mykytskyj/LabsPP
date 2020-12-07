from flask import Flask, request, flash, redirect, url_for, render_template
import os
from flask_login import LoginManager
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='nemo',pw='nasar58n',url='127.0.0.1:5432',db='labpp')

app.config['SQLALCHEMY_DATABASE_URI']=DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'




@app.route('/api/v1/hello-world-15')
def hello_world():
    return 'Hello World!'







if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
import views