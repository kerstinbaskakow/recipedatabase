from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired,Length,Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                           validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    #check if the user already exists
    def validate_username(self,username):
        #compare the current put in username to any username in the database
        #in case the user does not exist this gives back a None
        user = User.query.filter_by(username=username.data).first()
        #if anything else than none...
        if user:
            raise ValidationError('Username already used')
        #check if the user already exists
    def validate_email(self,email):
        #compare the current put in email to any email in the database
        #in case the email does not exist this gives back a None
        email = User.query.filter_by(email=email.data).first()
        #if anything else than none...
        if email:
            raise ValidationError('Email already used')
    
class LoginForm(FlaskForm):
    #Email is used for login
    email = StringField('Email',
                           validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =BooleanField('Remember me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                           validators=[DataRequired(),Email()])
    picture = FileField('Update Image Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    #check if the user already exists
    def validate_username(self,username):
        #in case of the account update we only have to check usernames different to our own
        if username.data != current_user.username:
            #compare the current put in username to any username in the database
            #in case the user does not exist this gives back a None
            user = User.query.filter_by(username=username.data).first()
            #if anything else than none...
            if user:
                raise ValidationError('Username already used')
    #check if the email already exists
    def validate_email(self,email):
        #in case of the account update we only have to check usernames different to our own
        if email.data != current_user.email:
            #compare the current put in email to any email in the database
            #in case the email does not exist this gives back a None
            email = User.query.filter_by(email=email.data).first()
            #if anything else than none...
            if email:
                raise ValidationError('Email already used')
                
class RequestResetForm(FlaskForm):
    #Email is used to geht the new pw by mail
    email = StringField('Email',
                           validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')
    #check if the user exists
    def validate_email(self,email):
        #compare the current put in email to any email in the database
        #in case the email does not exist this gives back a None
        user = User.query.filter_by(email=email.data).first()
        #if anything else than none...
        if user is None:
            raise ValidationError('There is no accout with that email. Register first!')
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')