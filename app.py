import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from forms import AddProductForm
# from forms import RegisterForm
from werkzeug.utils import secure_filename
import cx_Oracle

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'

# # Config Oracle
connection = cx_Oracle.connect('admin/admin@127.0.0.1/storedb')


def check_ext(filename, allowed=['png', 'jpg', 'jpeg']):
    if filename != '':
        ex = filename.split('.')[-1]
        if ex.lower() in allowed:
            return True
        return False
    return True


def checkImg(file):
    if request.files.get(file, None):
        if check_ext(request.files[file].filename) != False:
            filename = secure_filename(request.files[file].filename)
            request.files[file].save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            return filename
        else:
            flash("Select Valid Image", "danger")
            return render_template('add_product.html', title='title')
    else:
        filename = ''
        return filename


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shop/', methods=['GET', 'POST'])
def shop():
    imagesPath=[]
    cur=connection.cursor()
    prepare ="SELECT * from products order by uploaddate desc";
    cur.execute(prepare)
    products=cur.fetchall()
    for image in products:
        imagesPath.append(url_for('static',filename=f'upload/{image[10]}'))
    return render_template('product.html', products=zip(imagesPath,products))


@app.route('/blog/')
def blog():
    return render_template('blog.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/shop/<product>/')
def productlist(product):
    return product


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # GET FORM FIELDS
        username = request.form['username']
        password_candid = request.form['password']

        # CREATE CURSOR
        cur = connection.cursor()
        # GET USER BY USERNAME
        prepare = "SELECT * FROM users WHERE username = :username"
        cur.execute(prepare, {'username': username})

        # if result > 0:
        #     #GET STORED HASH
        data = cur.fetchone()
        if data is not None:
            password = data[2]
            if sha256_crypt.verify(password_candid, password):
                # passed
                session['logged_in'] = True
                session['username'] = username
                cur.close()
                flash("You are now logged in ", 'primary')
                return redirect(url_for('dashboard'))
                # return 'log in'
            else:
                error = "Invalid Passowrd"
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = "Username not found"
            cur.close()
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


# @app.route('/dashboard/<category>')
# def categorys():
#     return

@app.route('/add_product/', methods=['POST', 'GET'])
def add_product():
    form =  AddProductForm(request.form)
    if request.method == 'POST' and form.validate():
        category = form.category.data
        name = form.name.data
        code = form.code.data
        ptype = form.pro_type.data
        color = form.color.data
        size = form.size.data
        price = int(form.price.data)
        quantity = int(form.quantity.data)
        description = form.description.data

        # check if the post request has the file part
        image1 = checkImg('file1')
        image2 = checkImg('file2')
        image3 = checkImg('file3')

        cur = connection.cursor()

        data = (
            category, name,  code, ptype, color, size,  price,
            quantity, description, image1,  image2, image3
        )

        sql = """INSERT INTO products(category , name , code , type, color,
         sizee , price , quantity , description , pic1 , pic2 , pic3 ) 
         VALUES(:1 , :2 , :3 , :4, :5,
        :6 , :7 , :8 , :9, :10 , :11 , :12)"""

        cur.execute(sql, data)
        connection.commit()
        cur.close()
        flash('Product Added', 'success')
        return redirect(url_for('dashboard'))
    # else:
    #     return 'not valid'    
    return render_template('add_product.html', title='title',form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password']))
        cur = connection.cursor()
        prepare = "INSERT INTO users(name , username , password) VALUES(:name,  :username , :password)"
        cur.execute(
            prepare, {'name': name,  'username': username, 'password': password})
        connection.commit()
        cur.close()
        flash("You are now registered and can login", "success")
        return redirect(url_for('home'))
    return render_template("register.html")


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, port=5000)
