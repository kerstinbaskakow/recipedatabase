# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:19:54 2019

@author: FBASKKE-ADM

"""

#Neuinitialisieren der Datenbank:
#Achtung! Alles wird gelöscht falls das nicht passieren soll darf nicht neuinitialisiert werden
#1. start python from this directory
#2. from flaskblog import db
#3. from flaskblog import create_app
#4. app = create_app()
#5. from flaskblog.models import User,Post,BZD_FZG,BZD_Nutz,FK_Nutzungsintensitaet
#6. with app.app_context():db.create_all()
#now site.db should show in the directory


from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db,login_manager
#handles all the usersessions in the backround
from flask_login import UserMixin
from flask import current_app

#reloading the user from the user_id stored in the session
#the extension has to know how to find the user by id
@login_manager.user_loader
def load_user(user_id):
    #gets the user from the table User by 'user_id'
    return User.query.get(int(user_id))

#----------------------- db models --------------------------------------------
# the extension above expects the user models to have certain attributes and methods
# (in this case 4,isAuthenticated,isActive,isAnonymous,getId) 
# this is provided by a class we can inherit from UserMixin
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),unique=False,nullable=False,default='default.jpg')
    password = db.Column(db.String(20),nullable=False)
    #posts has a relatinship to Post model, 
    #backref is similar to adding annother columns to the Post Model, the 
    #backref allowes us to when there is a post we use the author attribute to get the post
    #lazy  defines when sqlalchemy loads the data of the database
    post = db.relationship('Post',backref='author',lazy=True)
    recipe = db.relationship('Recipe',backref='author',lazy=True)
    
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    #die folgende methode ist keine auf die klasse bezogenen sonder geht immer, also kein self dafür @staticmethod
    @staticmethod
    def verifiy_reset_token(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None 
        return User.query.get(user_id)
        
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    #be carefull! utcnow is passed as function not the value, no parenthesis!!!
    date_posted = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    #the foreignkey references the tablename, this is automatically set to lowercase, therefore 'user.id'
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
    
class Recipe(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    #be carefull! utcnow is passed as function not the value, no parenthesis!!!
    date_posted = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    #the foreignkey references the tablename, this is automatically set to lowercase, therefore 'user.id'
    recipe_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f"Recipe('{self.title}','{self.date_posted}')"