from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, DateField, DateTimeField, 
DateTimeLocalField, TimeField, MonthField, FloatField, IntegerField, DecimalRangeField, IntegerRangeField,
EmailField, URLField, TelField, FileField, RadioField, SelectField, SelectMultipleField, TextAreaField,
SearchField, StringField, PasswordField, BooleanField, SubmitField)
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_name = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password')
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')



class BSFormField(FlaskForm):
    date = DateField(description="We'll never share your email with anyone else.")  # add help text with `description`
    datetime = DateTimeField(render_kw={'placeholder': 'this is a placeholder'})  # add HTML attribute with `render_kw`
    datetimelocal = DateTimeLocalField()
    time = TimeField('Time')
    month = MonthField('Month')
    floating = FloatField('A decimal number')
    integer = IntegerField()
    decimalslider = DecimalRangeField()
    integerslider = IntegerRangeField(render_kw={'min': '0', 'max': '4'})
    email = EmailField('A valid email address')
    url = URLField()
    telephone = TelField()
    image = FileField(render_kw={'class': 'my-class'})  # add your class
    option = RadioField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select = SelectField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    selectmulti = SelectMultipleField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    bio = TextAreaField('Short write-up')
    search = SearchField() # will autocapitalize on mobile
    title = StringField() # will not autocapitalize on mobile
    secret = PasswordField('Password')
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')