from flask import render_template, request, flash, redirect, url_for, session
from functools import wraps
from passlib.hash import sha256_crypt
from functools import wraps
from FlaskApp import app , mysql
from FlaskApp.forms import AddProductForm , Register , Login
from FlaskApp.otherFunctions import visitedUser, save_picture, check_ext,user_login_required,admin_login_required


## error handler for page not found ##
@app.errorhandler(404)
def not_found(error):
    return render_template('notfound.html' ,title='404'), 404

#####client side routes #####

@app.route('/')  # home route
def home():
    visitedUser(request,request.url)
    imagesPath=[]
    cur = mysql.connection.cursor()
    cur.execute("SELECT name,code,price,pic1,category FROM PRODUCTS")
    products=cur.fetchall()
    cur.close()
    for image in products:
        # imagesPath.append(url_for('static',filename=f'upload/{image[10]}'))
        imagesPath.append(url_for('static',filename=f"upload/{image['pic1']}"))
    return render_template('index.html',products=zip(imagesPath,products),title='Home')

@app.route('/<type>/') # type route watches, dress etc
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
        return render_template('type.html', products=zip(imagesPath,products),title=type.title())
    return render_template('notfound.html',title='404') , 404

@app.route('/shop/', methods=['GET', 'POST']) # shop route show all Products
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
    return render_template('blog.html',title='Blog')


@app.route('/about/')
def about():
    visitedUser(request,request.url)
    return render_template('about.html', title='About')


@app.route('/contact/')
def contact():
    visitedUser(request,request.url)
    return render_template('contact.html',title='Contact')



@app.route('/shop/<category>/') ##category route show all products cateory wise
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

@app.route('/shop/<category>/<productcode>/',methods=['GET','POST']) ## show product details route
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
                for addedproducts in session['cart']:
                    if product == addedproducts['product']:
                        flash(f"{product['name']} is already added to Cart ! ","danger")
                        return redirect(url_for("showcategory",category=category))  
                session['cart'].append({
                'product'  : product ,
                'quantity' : quantity ,
                'size'     :  size ,
                'color'    : color,
                })
                session['total']+=(int(product['price']) * int(quantity))
            else:
                session['total']=0
                session['cart']=[{
                'product'  : product ,
                'quantity' : quantity ,
                'size'     :  size ,
                'color'    : color,
            },] 
                session['total']=(int(product['price']) * int(quantity)) 
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
        return render_template('product-detail.html',product=product,imagesPath=imagesPath,sizes=sizes,colors=colors ,relatedProducts=zip(relatedProducts,relatedImagesPath),title='Product')
    return render_template('notfound.html',title='404') , 404

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
                session['name'] = data['name']
                session['user_id'] =data['id']
                cur.close()
                flash("You are now logged in ", 'primary')
                return render_template('index.html')
                # return 'log in'
            else:
                error = "Invalid Password"
                return render_template('login.html',form=form, error=error,title='User Log in')
            cur.close()
        else:
            error = "Username not found"
            cur.close()
            return render_template('login.html',form=form ,error=error,title='User Log in')
    return render_template('login.html',form=form,user='user',title='User Log in')

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
                return render_template("register.html",form=form,user='user',title='User Registration')

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
        return redirect(url_for('userlogin'))
    return render_template('register.html',form=form,user='user',title='User Registration')


@app.route('/cart/',methods=['GET','POST'])
def cart():
    if request.method == "POST":
        if 'update' in request.form:
           session.pop('cart', None)
        if 'checkout' in request.form:
            if 'user_logged_in' in session:
                city=request.form['city']
                address=request.form['address']
                # postcode=request.form['postcode']
                customerid=session['user_id']
                total=session['total']
                deliverystatus='pending'
                cur = mysql.connection.cursor()
                cur.execute("SELECT max(orderid) as neworderid FROM invoice")
                orderid=cur.fetchone()
                cur.close()
                if orderid['neworderid'] is None:
                    orderid=1
                else:
                    orderid=orderid['neworderid']+1
                cur=mysql.connection.cursor()
                cur.execute(""" INSERT INTO invoice(orderid , customerid , city , address , totalamount , deliverystatus)
                 VALUES( %s , %s , %s , %s , %s , %s)""",
                 (orderid , customerid , city , address , total , deliverystatus))
                
                for item in session['cart']:
                    productid=item['product']['code']
                    sellingprice=item['product']['price']
                    costprice=item['product']['price']
                    quantity=item['quantity']
                    color=item['color']
                    size=item['size']
                    sql="""INSERT INTO orders(orderid , productid , quantity , sellingprice , costprice, color,size)
                    VALUES(%s , %s , %s , %s , %s , %s , %s) """
                    values=(orderid , productid , quantity , sellingprice , costprice , color , size)
                    cur.execute(sql,values)
                mysql.connection.commit()    
                cur.close()
                flash(f"Order Confirmed , order id : {orderid}" , "danger")
                session.pop('cart', None)
                return redirect(url_for('home'))
            else:
                flash(" Please login first " , "danger")
                return redirect(url_for('userlogin'))









    return render_template('cart.html',title='Cart')

@app.route('/logout/')
@user_login_required
def userlogout():
    session.clear()
    flash("You are now logged out" , "success")
    return redirect(url_for('home'))
#### Admin routes ###

@app.route('/admin/', methods=['GET', 'POST']) ## route for admin login
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
                session['admin_name'] = data['name']
                cur.close()
                flash("You are now logged in ", 'primary')
                return redirect(url_for('admin_dashboard'))
                # return 'log in'
            else:
                error = "Invalid Password"
                return render_template('login.html',form=form, error=error,user='admin')
            cur.close()
        else:
            error = "Username not found"
            cur.close()
            return render_template('login.html',form=form ,error=error,user='admin')
    return render_template('login.html',form=form,user='admin',title='Admin Log in')


@app.route('/admin/dashboard/')  ## admin dashboard
@admin_login_required
def admin_dashboard():
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
    return render_template('admindashboard.html', products=zip(imagesPath,products),title='Admin Dashboard')
    
@app.route('/admin/dashboard/<category>') ##show all products on admin dashboard category wise
@admin_login_required
def dashboard_categorys(category): 
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
        return render_template('admindashboard.html', products=zip(imagesPath,products),title=category)
    return render_template('notfound.html',title='404') , 404

@app.route('/admin/dashboard/<category>/<productcode>/',methods=['GET','POST']) ## products details to update product
@admin_login_required
def dashboard_products(category,productcode): 
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

        if product['sizee'] == '':
            sizes='Not Available'
        else:sizes=product['sizee']     
        if product['color'] == '':
            colors='Not Available'
        else: colors=product['color']
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute("SELECT name,code,price,pic1,category FROM PRODUCTS WHERE category = %s AND type = %s",(category,product['type']))
        relatedProducts=cur.fetchall()
        cur.close()
        for image in relatedProducts:
            relatedImagesPath.append(url_for('static',filename=f"upload/{image['pic1']}"))
        return render_template('dashboardproduct.html',product=product,imagesPath=imagesPath,sizes=sizes,colors=colors ,relatedProducts=zip(relatedProducts,relatedImagesPath),title='Product')
    return render_template('notfound.html',title='404') , 404


@app.route('/admin/dashboard/<category>/<productcode>/update' ,methods=['GET','POST']) ## update product for admin
@admin_login_required
def update_product(category,productcode):
    form=AddProductForm()
    cur=mysql.connection.cursor()
    # prepare='SELECT * FROM PRODUCTS WHERE CODE= :code'
    # cur.execute(prepare,{'code':productcode})
    cur.execute("SELECT * FROM PRODUCTS WHERE CODE= %s",[productcode])
    product=cur.fetchone()
    if product is not None:
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
                    return render_template('updateproduct.html', title='Update Product',form=form)
            else: image1=''    
            if form.image2.data:
                image2=save_picture(form.image2.data)
                if image2 is None:
                    flash("Select Valid Image 2", "danger")
                    return render_template('updateproduct.html', title='Update Product',form=form)
            else: image2=''    
            if form.image3.data:
                image3=save_picture(form.image3.data)
                if image3 is None:
                    flash("Select Valid Image 3", "danger")
                    return render_template('updateproduct.html', title='Update Product',form=form)
            else: image3=''          
        # check if the post request has the file part
        # image1 = checkImg('file1')
        # image2 = checkImg('file2')
        # image3 = checkImg('file3')

        # cur = connection.cursor()

            data = (
                category, name,  code, ptype, color, size,  price,
                quantity, description, image1,  image2, image3
            )
            
        # cur.close()
            sql = """INSERT INTO products(category , name , code , type, color,
            sizee , price , quantity , description , pic1 , pic2 , pic3 ) 
            VALUES(:1 , :2 , :3 , :4, :5,
            :6 , :7 , :8 , :9, :10 , :11 , :12)"""
        # cur = connection.cursor()
            cur = mysql.connection.cursor()
        # cur.execute(sql, data)
            sql="""UPDATE products set category = %s , name = %s, type= %s, color= %s,
            sizee = %s, price = %s, quantity= %s , description = %s, pic1= %s , pic2= %s , pic3= %s WHERE code = %s"""
            val=(
                category, name, ptype, color, size,  price,
                quantity, description, image1,  image2, image3,int(product['code'])
            )
            cur.execute(sql,val)
            mysql.connection.commit()
            cur.close()
            flash(f'{name} Updated !', 'success')
            return redirect(url_for('admin_dashboard'))
    
        
        return render_template('updateproduct.html',form=form,product=product,update='Update', title='Update Product')
    return render_template('notfound.html',title='404') , 404
    
@app.route('/admin/pendingorders/')
@admin_login_required
def pending_orders():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM INVOICE WHERE DELIVERYSTATUS = %s",['pending'])
    records=cur.fetchall()
    cur.close()
    return render_template('pendingorder.html',title='Pending Orders',records=records)

@app.route('/admin/pendingorders/<orderid>/')
@admin_login_required
def update_orders(orderid):
    cur=mysql.connection.cursor()
    cur.execute("UPDATE INVOICE SET DELIVERYSTATUS=%s WHERE ORDERID=%s",('delivered',int(orderid)))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('pending_orders'))


@app.route('/admin/salesrecord/')
@admin_login_required
def sales_record():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM INVOICE")
    records=cur.fetchall()
    cur.close()
    return render_template('salesrecord.html',title='Sales Record',records=records)

@app.route('/admin/findcustomer/')
@admin_login_required
def find_customer():
    pass

@app.route('/admin/others/')
@admin_login_required
def others():
    pass


@app.route('/admin/addproduct/', methods=['POST', 'GET'])
@admin_login_required
def add_product():
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
                return render_template('add_product.html', title='Add Product',form=form)
        else: image1=''    
        if form.image2.data:
            image2=save_picture(form.image2.data)
            if image2 is None:
                flash("Select Valid Image 2", "danger")
                return render_template('add_product.html', title='Add Product',form=form)
        else: image2=''    
        if form.image3.data:
            image3=save_picture(form.image3.data)
            if image3 is None:
                flash("Select Valid Image 3", "danger")
                return render_template('add_product.html', title='Add Product',form=form)
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
                return render_template('add_product.html', title='Add Product',form=form)
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
        return redirect(url_for('admin_dashboard'))
    return render_template('add_product.html', title='Add Product',form=form)


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
                return render_template("register.html",form=form,user='admin',title='Admin Registration')

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
    return render_template("register.html",form=form,user='admin',title='Admin Registration')

@app.route('/logout/')
@admin_login_required
def adminlogout():
    session.clear()
    flash("You are now logged out" , "success")
    return redirect(url_for('home'))