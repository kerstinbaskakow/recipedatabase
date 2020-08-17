# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:19:33 2019

@author: FBASKKE-ADM
"""
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from pathlib import Path

#from flask_caching import Cache
#timer to store vpl data periodically
#from threading import Timer
#create a database instance
#dont forget in the terminal from flaskblog import db, db.create_all()
db = SQLAlchemy()
#create an instance for initialize password hashing
bcrypt = Bcrypt()
#generate the instance of the LoginManager
#in this way we add some functionallity to our database models to handel the user sessions
login_manager = LoginManager()
# this leads back to the login page in case that the account page will be accessed without loged in user
login_manager.login_view = 'users.login'
#set the category of the flash message of login_view
login_manager.login_message_category= 'info'
#
mail=Mail()
#
#cache = Cache()

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# #do the multiprocessing on the pipeline, result should be 2 dataframes
# def storeVPLData():
    # #get data, wrangle it, enrich it and caluculate the proportion of nutzungsintensität for each vehicle
    # df_Fzg,_,df_meta = pipeline()
    # #to save space get rid of the not not calculated values. this is roundabout 300000 datasets vs. 5000
    # df_Fzg = df_Fzg[df_Fzg['AUSWERTEINFO']=="Success"]
    # now = datetime.utcnow()
    # df_Fzg['STORING_TIME'] = now
    # df_Fzg.to_sql(name='Fahrzeuge', con=db.engine, index=False,if_exists='append') 
    # df_meta.to_sql(name='Meta', con=db.engine, index=False,if_exists='replace') 
    # #missing:
    # #automatic storage is not yet implemented, therefore automated delete is also not implemented
    # #as only values from the past tbd month are neccessary data older than tb can be deleted.
    # print('Storing executed! You can start the app now')
    

def create_app(config_class=Config):
    #--------------- configuration ------------------------------------------------
    #where to look for templates and static files
    # app is created from __init__
    app = Flask(__name__)
    app.config.from_object(Config)
    #
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    #generate the db if not yet existst
    my_file = Path("site.db")
    if my_file.is_file():
        pass
    # file exists
    else:
        with app.app_context():db.create_all()
    
    return app


