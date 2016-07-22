from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class NewBookForm(Form):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    publisher = StringField('publisher', validators=[DataRequired()])
    gender = StringField('gender', validators=[DataRequired()])
