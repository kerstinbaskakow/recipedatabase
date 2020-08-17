from flask import render_template,request,Blueprint,flash,abort,url_for,redirect
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flask_login import login_required,current_user

posts = Blueprint('posts',__name__)

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Posts XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#=================== new post =================================================
@posts.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #for auther the backref is used
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        #add the post to the database
        db.session.add(post)
        #commit the changes of the database
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form,legend='New Post')

#=========================== post =============================================
@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    #get by id or give back a 404
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post,title=post.title)

#======================== update post =========================================
@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    #get by id or give back a 404
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        #403 is the http for forbidden route
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        #-----------------update the title and the content -----------------------
        post.title = form.title.data
        post.content = form.content.data
        #commit the changes to the database
        db.session.commit()
        # send a flash messge that the username or email was changed
        flash('Your post has been updated','success')
        #go back to account
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')

#====================== delete post ===========================================
@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    #get by id or give back a 404
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        #403 is the http for forbidden route
        abort(403)
    else:
        #-----------------delete the post -----------------------
        db.session.delete(post)
        #commit the changes to the database
        db.session.commit()
        # send a flash messge that the post was deleted
        flash('Your post has been deleted','success')
        #go back to account
        return redirect(url_for('main.home'))