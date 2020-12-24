from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators,  IntegerField, ValidationError
from wtforms.validators import InputRequired, EqualTo, Email
import re

class BlogForm(Form):
    title = StringField('Title', validators=[InputRequired(message='*Required')])
    content = StringField('Title', validators=[InputRequired(message='*Required')])

class PassChange(Form):
    password = PasswordField('Password',validators=[InputRequired(message='*Required'), EqualTo('password_confirm', message="Passwords must match")])
    password_confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(Form):
    name = StringField('Name', validators=[InputRequired(message='*Required')])
    surname = StringField('Surname', validators=[InputRequired(message='*Required')])
    username = StringField('Username', validators=[InputRequired(message='*Required')])
    password = PasswordField('Password',validators=[InputRequired(message='*Required'), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')
    email = StringField('Email', validators=[InputRequired(message='*Required'), Email()])   
    phone = StringField('Phone', validators=[InputRequired(message='*Required')])

    def validate_phone(self, phone):
        print(phone.data)
        if not re.match(r"^\+994(77|70|50|51|55|99)[0-9]{7}$",phone.data):
            raise ValidationError("Not valid")
        print(phone)
        return phone.data