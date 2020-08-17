# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:09:26 2019

@author: fbaskke
"""

#flaskblog is now a package
# if working with packages then that is going to import this from the __init__ file in the package
from flaskblog import create_app

app = create_app()

if __name__ == "__main__":
    
    app.run(debug=False, host='192.168.2.118')


#start the webserver for the first time
    #start the command line,
    #go to Flask_Blog folder
    # and set an environment variable
    #type in export FLASK_APP=flaskblog.py für linux and mac
    #type in sst FLASK_APP=flaskblog.py for windows
#stop the webserver