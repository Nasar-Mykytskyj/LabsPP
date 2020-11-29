from flask import Flask
import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='nemo',pw='nasar58n',url='127.0.0.1:5432',db='labpp')

#app.config['SQLALCHEMY_DATABASE_URI']=\
#    'postgresql://nemo:nasar58n@localhost/labpp'
app.config['SQLALCHEMY_DATABASE_URI']=DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)

@app.route('/api/v1/hello-world-15')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
