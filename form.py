from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, EqualTo, Email

class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(Form):
    name = StringField('Name', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')
    email = StringField('Email', validators=[InputRequired(), Email()])   
    phone = StringField('Phone', validators=[InputRequired()])
