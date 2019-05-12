import os
from flask import Flask,session
# from flask_session.__init__ import Session
from flask_mysqldb import MySQL

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# sess = Session()

mysql = MySQL(app)

app.config['UPLOAD_FOLDER'] = 'static/upload'

# Config MySQL
app.config['MYSQL_HOST'] = "us-cdbr-iron-east-02.cleardb.net"
app.config['MYSQL_USER'] = "b10f7d5e54fb9f"
app.config['MYSQL_PASSWORD'] = "15302639"
app.config['MYSQL_DB'] = "heroku_4cecaa710a0e256"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['MYSQL_PORT'] = 3306


from FlaskApp import routes