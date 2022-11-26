from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, DateField, DateTimeField, 
DateTimeLocalField, TimeField, MonthField, FloatField, IntegerField, DecimalRangeField, IntegerRangeField,
EmailField, URLField, TelField, FileField, RadioField, SelectField, SelectMultipleField, TextAreaField,
SearchField, StringField, PasswordField, BooleanField, SubmitField, validators )
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    user_name = StringField('username', [validators.DataRequired(), validators.Length(min=3, max=15) ])
    password = PasswordField('password',[validators.DataRequired(), validators.Length(min=4, max=35) ])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    user_name = StringField('Username', [
    validators.DataRequired(), validators.Length(min=4, max=15) ])
    email = EmailField('Email', [validators.Length(min=4, max=35)])
    first_name = StringField('First Name',[validators.DataRequired(), validators.Length(min=2, max=15) ])
    last_name = StringField('Last Name')
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=4, max=35) ])
    submit = SubmitField('Register')


class ResetEmailForm(FlaskForm):
    email = EmailField('Type  your email', [validators.DataRequired(),validators.Length(min=4, max=35)])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Type your new Password', [validators.DataRequired(), validators.Length(min=4, max=35) ])



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