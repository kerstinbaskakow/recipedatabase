# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 16:52:47 2019

@author: FBASKKE-ADM
"""

from flask import Blueprint,render_template

errors = Blueprint('errors',__name__)

#for errors a different decorater is used. this is similiar to @routes
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html'),404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error/403.html'),403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error/500.html'),500


