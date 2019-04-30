import os
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from forms import AddProductForm
from werkzeug.utils import secure_filename
# import cx_Oracle
import secrets
from PIL import Image

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

# app.config['MYSQL_HOST'] = "localhost"
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = ""
# app.config['MYSQL_DB'] = "myflaskapp"
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"

def visitedUser(ip,link):
    currentDT = datetime.datetime.now()
    currentTime=currentDT.strftime("%I:%M:%S %p")
    currentDate=currentDT.strftime("%b %d, %Y")
    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO visitedusers(ip , link , timee , datee ) VALUES( %s , %s , %s , %s)",(ip , link, currentTime , currentDate))
    mysql.connection.commit()
    cur.close()







# # Config Oracle
# connection = cx_Oracle.connect('admin/admin@127.0.0.1/storedb')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if check_ext(form_picture.filename):
        picture_path = os.path.join(app.root_path, 'static/upload', picture_fn)
        # output_size = (200, 350)
        i = Image.open(form_picture).convert('RGB')
        # i.thumbnail(output_size)
        i.save(picture_path)
        return picture_fn
    else:
        return None
        # return redirect(url_for('add_product'))   

def check_ext(filename, allowed=['png','jpg','jpeg']):
    ex = filename.split('.')[-1]
    if ex.lower() in allowed:
        return True
    return False


# def checkImg(file):
#     if request.files.get(file, None):
#         if check_ext(request.files[file].filename) != False:
#             filename = secure_filename(request.files[file].filename)
#             request.files[file].save(os.path.join(
#                 app.config['UPLOAD_FOLDER'], filename))
#             return filename
#         else:
#             flash("Select Valid Image", "danger")
#             return render_template('add_product.html', title='title')
#     else:
#         filename = ''
#         return filename

@app.errorhandler(404)
def not_found(error):
    return render_template('notfound.html' ,title='404'), 404
    
@app.route('/')
def home():
    # visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip=request.environ['REMOTE_ADDR']
    else:
        ip=request.environ['HTTP_X_FORWARDED_FOR'] 
    visitedUser(ip,request.url)

    imagesPath=[]
    cur = mysql.connection.cursor()
    cur.execute("SELECT name,code,price,pic1,category FROM PRODUCTS")
    products=cur.fetchall()
    cur.close()
    for image in products:
        # imagesPath.append(url_for('static',filename=f'upload/{image[10]}'))
        imagesPath.append(url_for('static',filename=f"upload/{image['pic1']}"))
    return render_template('index.html',products=zip(imagesPath,products))

@app.route('/<type>/')
def showtype(type):
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    imagesPath=[]
    # cur =connection.cursor()
    cur =mysql.connection.cursor()
    # prepare='SELECT * FROM PRODUCTS WHERE TYPE = :type'
    # cur.execute(prepare,{'type':type.title()})
    if type.lower() =='all':
        cur.execute("SELECT * FROM PRODUCTS")    
    cur.execute("SELECT * FROM PRODUCTS WHERE TYPE = %s",[type.lower()])
    products=cur.fetchall()
    if len (products) > 0:
        for image in products:
        # imagesPath.append(url_for('static',filename=f'upload/{image[10]}'))
            imagesPath.append(url_for('static',filename=f"upload/{image['pic1']}"))
        return render_template('type.html', products=zip(imagesPath,products),title=type)
    return render_template('notfound.html',title='404') , 404

@app.route('/shop/', methods=['GET', 'POST'])
def shop():
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    imagesPath=[]
    # cur=connection.cursor()
    cur=mysql.connection.cursor()
    # prepare ="SELECT * from products order by uploaddate desc"
    # cur.execute(prepare)
    cur.execute("SELECT * from products order by uploaddate desc")
    products=cur.fetchall()
    cur.close()
    for image in products:
        # imagesPath.append(url_for('static',filename=f'upload/{image[10]}'))
        imagesPath.append(url_for('static',filename=f"upload/{image['pic1']}"))
    return render_template('product.html', products=zip(imagesPath,products),title='All')


@app.route('/blog/')
def blog():
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    return render_template('blog.html')


@app.route('/about/')
def about():
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    return render_template('about.html')


@app.route('/contact/')
def contact():
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    return render_template('contact.html')



@app.route('/shop/<category>/')
def showcategory(category):
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    imagesPath=[]
    # cur=connection.cursor()
    cur=mysql.connection.cursor()
    # prepare ="SELECT * from products where category=:category"
    # cur.execute(prepare,{'category':category.title()})
    if category.lower() =='all':
        cur.execute("SELECT * FROM PRODUCTS")
    else:       
        cur.execute("SELECT * from products where category= %s",[category.lower()])
    products=cur.fetchall()
    cur.close()
    if len(products) > 0:     
        for image in products:
            # imagesPath.append(url_for('static',filename=f'upload/{image[10]}'))
            imagesPath.append(url_for('static',filename=f"upload/{image['pic1']}"))
        return render_template('product.html', products=zip(imagesPath,products),title=category)
    return render_template('notfound.html',title='404') , 404

@app.route('/shop/<category>/<productcode>/')
def showproduct(category,productcode):
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    imagesPath=[]
    relatedImagesPath=[]
    # cur=connection.cursor()
    cur=mysql.connection.cursor()
    # prepare='SELECT * FROM PRODUCTS WHERE CODE= :code'
    # cur.execute(prepare,{'code':productcode})
    cur.execute("SELECT * FROM PRODUCTS WHERE CODE= %s",[productcode])
    product=cur.fetchone()
    if product is not None:     
        if product['pic1'] == '':
            imagesPath.append(url_for('static',filename="upload/default.jpg"))
        else:
             imagesPath.append(url_for('static',filename=f"upload/{product['pic1']}"))
        if product['pic2'] == '':
            imagesPath.append(url_for('static',filename="upload/default.jpg"))
        else:
             imagesPath.append(url_for('static',filename=f"upload/{product['pic2']}"))    
        if product['pic3'] == '':
            imagesPath.append(url_for('static',filename="upload/default.jpg"))
        else:
             imagesPath.append(url_for('static',filename=f"upload/{product['pic3']}"))

        if product['sizee'] != '':
            sizes=product['sizee'].split(',')
        else:
            sizes='Not Available' 
        if product['color'] != '':
            colors=product['color'].split(',')
        else:
            colors='Not Available'
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("SELECT name,code,price,pic1,category FROM PRODUCTS WHERE category = %s AND type = %s",(category,product['type']))
        relatedProducts=cur.fetchall()
        cur.close()
        for image in relatedProducts:
            relatedImagesPath.append(url_for('static',filename=f"upload/{image['pic1']}"))
        return render_template('product-detail.html',product=product,imagesPath=imagesPath,sizes=sizes,colors=colors ,relatedProducts=zip(relatedProducts,relatedImagesPath))
    return render_template('notfound.html',title='404') , 404


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    if request.method == 'POST':
        # GET FORM FIELDS
        username = request.form['username']
        password_candid = request.form['password']

        # CREATE CURSOR

        # cur = connection.cursor()
        cur=mysql.connection.cursor()
        # GET USER BY USERNAME
        # prepare = "SELECT * FROM users WHERE username = :username"
        # cur.execute(prepare, {'username': username})
        cur.execute("SELECT * FROM users WHERE username = %s",[username])
        # if result > 0:
        #     #GET STORED HASH
        data = cur.fetchone()
        if data is not None:
            password = data['password']
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
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    return render_template('dashboard.html')
# @app.route('/dashboard/<category>')
# def categorys():
#     return

@app.route('/addproduct/', methods=['POST', 'GET'])
def add_product():
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    form =  AddProductForm()
    if request.method == 'POST' and form.validate_on_submit():
        category = form.category.data
        name = form.name.data
        code = form.code.data
        ptype = form.pro_type.data
        color = form.color.data
        size = form.size.data
        price = int(form.price.data)
        quantity = int(form.quantity.data)
        description = form.description.data
        if form.image1.data:
            image1=save_picture(form.image1.data)
            if image1 is None:
                flash("Select Valid Image 1", "danger")
                return render_template('add_product.html', title='title',form=form)
        else: image1=''    
        if form.image2.data:
            image2=save_picture(form.image2.data)
            if image2 is None:
                flash("Select Valid Image 2", "danger")
                return render_template('add_product.html', title='title',form=form)
        else: image2=''    
        if form.image3.data:
            image3=save_picture(form.image3.data)
            if image3 is None:
                flash("Select Valid Image 3", "danger")
                return render_template('add_product.html', title='title',form=form)
        else: image3=''          
        # check if the post request has the file part
        # image1 = checkImg('file1')
        # image2 = checkImg('file2')
        # image3 = checkImg('file3')

        # cur = connection.cursor()
        cur = mysql.connection.cursor()

        cur.execute("SELECT CODE FROM PRODUCTS")
        availablecodes=cur.fetchall()
        
        # cur.close()
        for precode in availablecodes:
            if precode['CODE'] == code:
                flash('Product code already assigned to another product','danger')
                return render_template('add_product.html', title='title',form=form)
        data = (
            category, name,  code, ptype, color, size,  price,
            quantity, description, image1,  image2, image3
        )
        sql = """INSERT INTO products(category , name , code , type, color,
         sizee , price , quantity , description , pic1 , pic2 , pic3 ) 
         VALUES(:1 , :2 , :3 , :4, :5,
        :6 , :7 , :8 , :9, :10 , :11 , :12)"""
        # cur = connection.cursor()
        cur = mysql.connection.cursor()
        # cur.execute(sql, data)
        cur.execute("""INSERT INTO products(category , name , code , type, color,
         sizee , price , quantity , description , pic1 , pic2 , pic3 ) 
         VALUES( %s, %s,  %s, %s, %s, %s, %s,
            %s, %s, %s,  %s, %s)""",(
            category, name,  code, ptype, color, size,  price,
            quantity, description, image1,  image2, image3
        ))
        mysql.connection.commit()
        cur.close()
        flash(f'{name} Added !', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_product.html', title='title',form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    visitedUser(request.environ.get('HTTP_X_REAL_IP', request.remote_addr),request.url)
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password']))
        # cur = connection.cursor()
        cur = mysql.connection.cursor()
        # prepare = "INSERT INTO users(name , username , password) VALUES(:name,  :username , :password)"
        # cur.execute(
        #     prepare, {'name': name,  'username': username, 'password': password})
        # connection.commit()
        # cur.execute(f"INSERT INTO users(name , username , password) VALUES({name},{username},{password})")
        cur.execute("INSERT INTO users(name , username , password) VALUES(%s, %s , %s)" ,
        (name , username , password))
        mysql.connection.commit()
        cur.close()
        flash("You are now registered and can login", "success")
        return redirect(url_for('home'))
    return render_template("register.html")


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
