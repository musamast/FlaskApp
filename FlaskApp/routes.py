from flask import render_template, request, flash, redirect, url_for, session
from functools import wraps
from passlib.hash import sha256_crypt
from functools import wraps
from FlaskApp import app , mysql
from FlaskApp.forms import AddProductForm , Register , Login
from FlaskApp.otherFunctions import visitedUser, save_picture, check_ext


@app.errorhandler(404)
def not_found(error):
    return render_template('notfound.html' ,title='404'), 404

def user_login_required(g):
    @wraps(g)
    def wrap(*args , **kwargs):
        if 'user_logged_in' in session:
            return g(*args , **kwargs)
        else:
            flash(" Please login first " , "danger")
            return redirect(url_for('userlogin'))
    return wrap


def admin_login_required(g):
    @wraps(g)
    def wrap(*args , **kwargs):
        if 'admin_logged_in' in session:
            return g(*args , **kwargs)
        else:
            flash(" Please login first " , "danger")
            return redirect(url_for('admin'))
    return wrap



@app.route('/')
def home():
    # visitedUser(request,request.url)
     
    visitedUser(request,request.url)

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
    visitedUser(request,request.url)
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
    visitedUser(request,request.url)
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
    visitedUser(request,request.url)
    return render_template('blog.html')


@app.route('/about/')
def about():
    visitedUser(request,request.url)
    return render_template('about.html')


@app.route('/contact/')
def contact():
    visitedUser(request,request.url)
    return render_template('contact.html')



@app.route('/shop/<category>/')
def showcategory(category):
    visitedUser(request,request.url)
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

@app.route('/shop/<category>/<productcode>/',methods=['GET','POST'])
def showproduct(category,productcode):
    visitedUser(request,request.url)
    imagesPath=[]
    relatedImagesPath=[]
    # cur=connection.cursor()
    cur=mysql.connection.cursor()
    # prepare='SELECT * FROM PRODUCTS WHERE CODE= :code'
    # cur.execute(prepare,{'code':productcode})
    cur.execute("SELECT * FROM PRODUCTS WHERE CODE= %s",[productcode])
    product=cur.fetchone()
    if product is not None:
        if request.method == 'POST':
            quantity= request.form['quantity']
            color= request.form['color']
            size= request.form['size']
            if 'cart' in session:
                session['cart'].append({
                    'product'  : product ,
                    'quantity' : quantity ,
                    'size'     :  size ,
                    'color'    : color,
                })
            else:
                session['cart']=[{
                    'product'  : product ,
                    'quantity' : quantity ,
                    'size'     :  size ,
                    'color'    : color,
                },]
            flash(f"{product['name']} is added to Cart ! ","success")
            return redirect(url_for("showcategory",category=category))
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
    visitedUser(request,request.url)
    form=Login()
    if request.method == 'POST' and form.validate_on_submit():
        # GET FORM FIELDS
        username = form.username.data
        password_candid = form.password.data

        # CREATE CURSOR

        # cur = connection.cursor()
        cur=mysql.connection.cursor()
        # GET USER BY USERNAME
        # prepare = "SELECT * FROM users WHERE username = :username"
        # cur.execute(prepare, {'username': username})
        cur.execute("SELECT * FROM admins WHERE username = %s",[username])
        # if result > 0:
        #     #GET STORED HASH
        data = cur.fetchone()
        if data is not None:
            password = data['password']
            if sha256_crypt.verify(password_candid, password):
                # passed
                session['admin_logged_in'] = True
                session['admin_username'] = username
                cur.close()
                flash("You are now logged in ", 'primary')
                return redirect(url_for('dashboard'))
                # return 'log in'
            else:
                error = "Invalid Password"
                return render_template('login.html',form=form, error=error,user='admin')
            cur.close()
        else:
            error = "Username not found"
            cur.close()
            return render_template('login.html',form=form ,error=error,user='admin')
    return render_template('login.html',form=form,user='admin')


@app.route('/dashboard/')
@admin_login_required
def dashboard():
    visitedUser(request,request.url)
    return render_template('dashboard.html')
# @app.route('/dashboard/<category>')
# def categorys():
#     return

@app.route('/addproduct/', methods=['POST', 'GET'])
@admin_login_required
def add_product():
    visitedUser(request,request.url)
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
    visitedUser(request,request.url)
    form=Register()
    if request.method == 'POST'and form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(request.form['password']))
        # cur = connection.cursor()
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM admins")
        admins=cur.fetchall()
        # cur.close()
        for admin in admins:
            if admin['username'] == username:
                flash('Username already assigned to another user','danger')
                return render_template("register.html",form=form,user='admin')

        # prepare = "INSERT INTO users(name , username , password) VALUES(:name,  :username , :password)"
        # cur.execute(
        #     prepare, {'name': name,  'username': username, 'password': password})
        # connection.commit()
        # cur.execute(f"INSERT INTO users(name , username , password) VALUES({name},{username},{password})")
        cur.execute("INSERT INTO admins(name , username , email , password) VALUES(%s, % s, %s , %s)" ,
        (name , username , email , password))
        mysql.connection.commit()
        cur.close()
        flash("You are now registered and can login", "success")
        return redirect(url_for('home'))
    return render_template("register.html",form=form,user='admin')

@app.route('/login',methods=['GET','POST'])
def userlogin():
    form=Login()
    if request.method== 'POST' and form.validate_on_submit():
        # GET FORM FIELDS
        username = form.username.data
        password_candid = form.password.data

        # CREATE CURSOR

        # cur = connection.cursor()
        cur=mysql.connection.cursor()
        # GET USER BY USERNAME
        # prepare = "SELECT * FROM users WHERE username = :username"
        # cur.execute(prepare, {'username': username})
        cur.execute("SELECT * FROM customers WHERE username = %s",[username])
        # if result > 0:
        #     #GET STORED HASH
        data = cur.fetchone()
        if data is not None:
            password = data['password']
            if sha256_crypt.verify(password_candid, password):
                # passed
                session['user_logged_in'] = True
                session['username'] = username
                cur.close()
                flash("You are now logged in ", 'primary')
                return redirect(url_for('dashboard'))
                # return 'log in'
            else:
                error = "Invalid Password"
                return render_template('login.html',form=form, error=error)
            cur.close()
        else:
            error = "Username not found"
            cur.close()
            return render_template('login.html',form=form ,error=error)
    return render_template('login.html',form=form,user='user')

@app.route('/newuser',methods=['GET','POST'])
def userreg():
    form=Register()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(request.form['password']))
        # cur = connection.cursor()
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM customers")
        customers=cur.fetchall()
        # cur.close()
        for customer in customers:
            if customer['username'] == username:
                flash('Username already assigned to another user','danger')
                return render_template("register.html",form=form,user='user')

        # prepare = "INSERT INTO users(name , username , password) VALUES(:name,  :username , :password)"
        # cur.execute(
        #     prepare, {'name': name,  'username': username, 'password': password})
        # connection.commit()
        # cur.execute(f"INSERT INTO users(name , username , password) VALUES({name},{username},{password})")
        cur.execute("INSERT INTO customers(name , username , email , password) VALUES(%s, % s, %s , %s)" ,
        (name , username , email , password))
        mysql.connection.commit()
        cur.close()
        flash("You are now registered and can login", "success")
        return redirect(url_for('home'))
    return render_template('register.html',form=form,user='user')


@app.route('/cart/',methods=['GET','POST'])
@user_login_required
def cart():
    if request.method == "POST":
        if 'update' in request.form:
           session.pop('cart', None)
    return render_template('cart.html',title='Cart')
