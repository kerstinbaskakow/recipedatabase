from flask import render_template,Blueprint,request,flash,abort,url_for,redirect
#from flaskblog import db
#from flaskblog.models import Post
from flaskblog.wallbox.forms import SetCharginModeForm1,SetCharginModeForm2
from flask_login import login_required,current_user
from flaskblog import influxclient




wallbox = Blueprint('wallbox',__name__)

AllOW_CHARGINGMODES = [1,2,3]


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Posts XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#=================== new post =================================================
@wallbox.route("/setChargingMode",methods=['GET','POST'])
@login_required
def setChargingMode():
    form = SetCharginModeForm1()
    
    
    if form.validate_on_submit():
        #for auther the backref is used
        chargingMode = int(form.content.data)
        if chargingMode in AllOW_CHARGINGMODES:
            body = [{
                    "measurement": 'button',
                    "fields":
                        {"value": chargingMode}
                    }]
            influxclient.write_points(body, database='iobroker', time_precision='s', batch_size=10000, protocol='json')
            flash('Your charging mode has been set to {} by {}'.format(chargingMode,current_user),'success')
        else:
            flash('Mode {} is not allowed'.format(chargingMode,current_user),'danger')
    
        #return redirect(url_for('main.home'))
    return render_template('setChargingMode.html',form=form,legend='SetChargingMode')

