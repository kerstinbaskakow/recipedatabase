from flask_login import login_user,current_user,logout_user,login_required
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flaskblog.users.forms import (RegistrationForm,LoginForm,UpdateAccountForm,
                             RequestResetForm,ResetPasswordForm)
from flaskblog import bcrypt,db
from flaskblog.models import Post,User
from flaskblog.users.utils import save_picture,send_reset_email

users = Blueprint('users',__name__)

#XXXXXXXXXXXXXXXXXXXXXXX User information and handling XXXXXXXXXXXXXXXXXXXXXXXX
# =================================register ===================================

@users.route("/register",methods=['GET','POST'])
def register():
    # --------------------this is what happens if already loged in ------------
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # ------------------ do the registration stuff ----------------------------
    form = RegistrationForm()
    if form.validate_on_submit():
        #gnerate a hashed password form the input data form form, decode UTF makes a string in intead of bytes
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        #generate a user from the form data with the hashed password
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        #add the user to the database
        db.session.add(user)
        #commit the changes of the database
        db.session.commit()
        #flash message pops up once
        #bootstrap has different allertstyles for succeses and warnings and errors
        #the flash function accepts a second argument which is the bootstrap name that the alert should have
        #dont forget to update the template to show the flash message
        flash(f'Your account has been created! Now you are able to login!','success')
        #after succesfull submit the user should be be redirected automatically to login
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)

# =================================login =====================================
@users.route("/login",methods=['GET','POST'])
def login():
    # --------------------this is what happens if already loged in ------------
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    # ------------------ do the login stuff -----------------------------------
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #if the user exists and the password is correct the user will be loged in
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            #for the login we use the extension of the loginmanager the login_user method
            #this is were we log in the user
            login_user(user,remember=form.remember.data)
            #next query
            # args is a dictionary which is accessed by the get method. 
            #if there is nothing the get method gives back a none
            #if it exists it is equal to the route
            next_page = request.args.get('next')
            #if succesfull redirect to the homepage
            return redirect (next_page) if next_page else redirect(url_for('main.home'))
        else:
            #flash message pops up once
            #bootstrap style <!-- Categories: success (green), info (blue), warning (yellow), danger (red) -->
            #bootstrap has different allertstyles for succeses and warnings and errors
            #the flash function accepts a second argument which is the bootstrap name that the alert should have
            #dont forget to update the template to show the flash message
            flash('Unsuccessfull login. Please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

# =================================logout =====================================
@users.route("/logout")
def logout():
    #this logs the user out
    #this does not take any arguments because it already knows that the user is loged in
    logout_user()
    # and redirects to the home page
    return redirect(url_for('main.home'))

# =================================account ====================================

#create a route for the user's account
@users.route("/account",methods=['GET','POST'])
#this extension makes sure the page is only displayed if the user is loged in
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # ---------------- update the picture ---------------------------------
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #-----------------update the user and the email -----------------------
        current_user.username = form.username.data
        current_user.email = form.email.data
        #commit the changes to the database
        db.session.commit()
        # send a flash messge that the username or email was changed
        flash('Your account has been updated','success')
        #go back to account
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

#=========================== sort post by user ================================   
@users.route("/user/<string:username>")
def user_posts(username):
    #default page is 1
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username = username).first_or_404()
    #amount of posts per page: per_page=5 and sort the results by date posted
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts=posts,user=user)

#====================== reset request =========================================
@users.route("/reset_password",methods=['GET','POST'])
def reset_request():   
    # --------------------this is what happens if already loged in --------
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user =User.query.filter_by(email=form.email.data).first()
        #now send the user a email
        send_reset_email(user)
        return redirect(url_for("users.login"))
        
    return render_template('reset_request.html',title='Reset Password',form=form)

#====================== reset token ===========================================
@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):   
    # --------------------this is what happens if already loged in ------------
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.verifiy_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #gnerate a hashed password form the input data form form, decode UTF makes a string in intead of bytes
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user.password=hashed_password
        #commit the changes of the database
        db.session.commit()
        flash('Your password has been changed!','success')
        return redirect(url_for("users.login"))
    return render_template('reset_token.html',title='Reset Password',form=form)