from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, TextAreaField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    #Email is used for login
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Description',validators=[DataRequired()])
    ingredients= StringField('Ingredients',validators=[DataRequired()])
    submit = SubmitField('Post')