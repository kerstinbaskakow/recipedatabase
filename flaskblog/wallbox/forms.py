from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SetCharginModeForm1(FlaskForm):
    #Email is used for login
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Mode')
    
    
    
class SetCharginModeForm2(FlaskForm):
    #Email is used for login
    submit1 = SubmitField('Mode1')
    submit2 = SubmitField('Mode2')
    submit3 = SubmitField('Mode3')