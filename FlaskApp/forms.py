from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,IntegerField,DecimalField,validators,TextAreaField,PasswordField
from flask_wtf.file import FileField, FileRequired

class AddProductForm(FlaskForm):
    category = SelectField('Category',choices=[('Men','Men'),('Women','Women'),('Kids','Kids')] )
    name = StringField('Product Name',[validators.Length(min=5 , max=50)])
    code = StringField('Product Code',[validators.Length(min=1 , max=50)] )
    pro_type = SelectField('Type',choices=[('Dresses','Dresses'),('Watches','Watches'),
                                            ('Wallets','Wallets'),('Footerwear','Footerwear'),('Sunglasses','Sunglasses')])
    color = StringField("Colors(Separated by ' , ' )",[validators.Length(min=3 , max=100)])
    size = StringField("Sizes(Separated by ' , ' )" )
    price = DecimalField('Price')
    quantity = IntegerField('Quantity')
    description = TextAreaField('Description',[validators.Length(min=10 )])
    image1 = FileField('Image 1',validators=[FileRequired()])
    image2 = FileField('Image 2')
    image3 = FileField('Image 3')

class Register(FlaskForm):
    name = StringField("Name",[validators.Length(min=3 , max=30)])
    email = StringField('Email',
                        [validators.Email(),validators.Length(min=5 , max=30)])
    username = StringField("Username",[validators.Length(min=3 , max=30)])
    password = PasswordField("Password",[validators.Length(min=3 , max=30)])
                    
class Login(FlaskForm):
    username = StringField("Username",[validators.Length(min=3 , max=30)])
    password = PasswordField("Password",[validators.Length(min=3 , max=30)])