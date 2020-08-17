from flaskblog import mail
import os
import secrets
from PIL import Image
from flask_mail import Message
from flask import url_for,flash,current_app

#method for picture update
def save_picture(form_picture):
    #dont keep the name of the image that is uploaded, it could collide with an already uploaded filename
    #so randomize the name of the image, the random_hex is the base of the filename
    random_hex = secrets.token_hex(8)
    #keep the extension of the uploaded file
    _,f_ext = os.path.splitext(form_picture.filename)
    #concatenate filename and extension
    picture_fn = random_hex+f_ext
    #generate a whole path to store the file
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    #resize the picture
    output_size = (400,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #store the file
    i.save(picture_path)
    return picture_fn


#XXXXXXXXXXXXXXXXXXX Password XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password reset request',
                sender='noreply@demo.com',
                recipients=[user.email])
    msg.body=f'''To reset your password visit the following link:
{url_for('users.reset_token',token=token,_external=True)}
    
If you did not make this request, ignore it. No changes will be done!
'''
    try:
        mail.send(msg)
        flash(f'Email has been sent to {user.email}!','info')
    except:
        flash('Uuuups! Sending Email did not work! Probably you are on an Audi client..','danger')