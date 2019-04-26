from flask_wtf import FlaskForm
# from flask_wtf import Form
from wtforms import StringField, SelectField,IntegerField,DecimalField,validators,TextAreaField
from flask_wtf.file import FileField, FileRequired
from flask_wtf.file import FileField, FileAllowed



class AddProductForm(FlaskForm):
    category = SelectField('Category',choices=[('All','All'),('Men','Men'),('Women','Women'),
                                                ('Accesories','Accesories')] )
    name = StringField('Product Name',[validators.Length(min=5 , max=50)])
    code = StringField('Product Code',[validators.Length(min=1 , max=50)] )
    pro_type = SelectField('Type',choices=[('Dresses','Dresses'),('Watches','Watches'),
                                            ('Bags','Bags'),('Footwear','Footwear'),('Sunglasses','Sunglasses')])
    color = SelectField('Color',choices=[('Red','Red'),('Orange','Orange'),('Pink','Pink'),
                                             ('Black','Black')])
    size = StringField('Size' ,[validators.Length(min=1 , max=50)])
    price = DecimalField('Price')
    quantity = IntegerField('Quantity')
    description = TextAreaField('description',[validators.Length(min=10 )])
    image1 = FileField('Image 1',validators=[FileRequired()])
    image2 = FileField('Image 2')
    image3 = FileField('Image 3')


                                     
    # submit = SubmitField('Sign Up')
