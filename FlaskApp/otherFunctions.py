import os
import datetime
from FlaskApp import app, mysql
import secrets
import ipinfo
from PIL import Image

def visitedUser(request,link):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip=request.environ['REMOTE_ADDR']
    else:
        ip=request.environ['HTTP_X_FORWARDED_FOR']
    currentDT = datetime.datetime.now()
    currentTime=currentDT.strftime("%I:%M:%S %p")
    currentDate=currentDT.strftime("%b %d, %Y")

    #for more info of visited user

    # handler = ipinfo.getHandler(access_token)
    # ip_address = ip
    # details = handler.getDetails(ip_address)
    # cur=mysql.connection.cursor()
    # cur.execute("""INSERT INTO visitedusers(ip , link , city , region , country ,
    #  loc , isp , timee , datee )
    #  VALUES( %s , %s , %s , %s, %s, %s, %s, %s,, %s)"""
    #  ,(ip , link , details.city   , details.region , details.country , details.loc ,
    #   details.isp , currentTime , currentDate))

    cur=mysql.connection.cursor()
    cur.execute("""INSERT INTO visitedusers(ip , link , timee , datee )
     VALUES( %s , %s , %s , %s)"""
     ,(ip , link , currentTime , currentDate))
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
