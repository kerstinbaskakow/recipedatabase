# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 13:49:31 2019

@author: FBASKKE-ADM
"""
import os
class Config:
    #protects against attacs
    #this should be in an environment variable but guess due to client it does not work
    #SECRET_KEY=os.environ.get('SECRET_KEY')
    SECRET_KEY = '0c0fff2d6e4db8f143d8dc6093a07f11'
    #define the relative path for the sqlite datebase
    #this should be in an environment variable but guess due to client it does not work
    # SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    
    #config for mails
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_PASSWORD=os.environ.get('EMAIL_PASS')
    MAIL_USERNAME=os.environ.get('EMAIL_USER')