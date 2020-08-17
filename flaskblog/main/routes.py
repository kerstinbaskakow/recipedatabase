from flask import render_template,request,Blueprint
from flaskblog.models import Post,Recipe


main = Blueprint('main',__name__)

#routes are what we type into our browser to go to different pages
# =================================home =======================================
@main.route("/")
@main.route("/home")
def home():
    #default page is 1
    page = request.args.get('page',1,type=int)
    #amount of posts per page: per_page=5 and sort the results by date posted
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html',posts=posts)

@main.route("/recipe")
def home_recipe():
    #default page is 1
    page = request.args.get('page',1,type=int)
    #amount of posts per page: per_page=5 and sort the results by date posted
    recipes = Recipe.query.order_by(Recipe.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home_recipe.html',recipes=recipes)

# =================================about ======================================
@main.route("/about")
def about():
    return render_template('about.html',title='About')