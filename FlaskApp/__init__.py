import os
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

mysql = MySQL(app)

app.config['UPLOAD_FOLDER'] = 'static/upload'

# Config MySQL
app.config['MYSQL_HOST'] = "us-cdbr-iron-east-02.cleardb.net"
app.config['MYSQL_USER'] = "beeb27dc4ba1c5"
app.config['MYSQL_PASSWORD'] = "d8a0ef01"
app.config['MYSQL_DB'] = "heroku_725bdcfeff15a40"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['MYSQL_PORT'] = 3306


from FlaskApp import routes