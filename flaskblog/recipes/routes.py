from flask import render_template,request,Blueprint,flash,abort,url_for,redirect
from flaskblog import db
from flaskblog.models import Recipe
from flaskblog.recipes.forms import RecipeForm
from flask_login import login_required,current_user

recipes = Blueprint('recipes',__name__)

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Recipes XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#=================== new recipe =================================================
@recipes.route("/recipe/new",methods=['GET','POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        #for auther the backref is used
        recipe = Recipe(title=form.title.data,content=form.content.data,author=current_user)
        #add the post to the database
        db.session.add(recipe)
        #commit the changes of the database
        db.session.commit()
        flash('Your recipe has been created!','success')
        print("das hier geht noch")
        return redirect(url_for('main.home_recipe'))
    return render_template('create_recipe.html',title='New Recipe',form=form,legend='New Recipe')

#=========================== recipe =============================================
@recipes.route("/recipe/<int:recipe_id>")
@login_required
def recipe(recipe_id):
    #get by id or give back a 404
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html',recipe=recipe,title=recipe.title)

#======================== update recipe =========================================
@recipes.route("/recipe/<int:recipe_id>/update",methods=['GET','POST'])
@login_required
def update_recipe(recipe_id):
    #get by id or give back a 404
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        #403 is the http for forbidden route
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        #-----------------update the title and the content -----------------------
        recipe.title = form.title.data
        recipe.content = form.content.data
        #commit the changes to the database
        db.session.commit()
        # send a flash messge that the username or email was changed
        flash('Your recipe has been updated','success')
        #go back to account
        return redirect(url_for('recipes.recipe',recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.content.data = recipe.content
    return render_template('create_recipe.html',title='Update Recipe',form=form,legend='Update Recipe')

#====================== delete recipe ===========================================
@recipes.route("/recipe/<int:recipe_id>/delete",methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    #get by id or give back a 404
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        #403 is the http for forbidden route
        abort(403)
    else:
        #-----------------delete the recipe -----------------------
        db.session.delete(recipe)
        #commit the changes to the database
        db.session.commit()
        # send a flash messge that the recipe was deleted
        flash('Your recipe has been deleted','success')
        #go back to account
        return redirect(url_for('main.home_recipe'))