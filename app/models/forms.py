from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SelectField,\
                    DateField, DecimalField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from book import Book


class LoginForm(Form):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember')


class RegisterForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])


class EditUserForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    cpf = StringField('cpf')
    gender = SelectField('gender',
                         choices=[(0, 'Feminino'), (1, 'Masculino')],
                         coerce=int,
                         validators=[Optional()])
    birthday = DateField('birthday',
                         format="%d/%m/%Y",
                         validators=[Optional()])


class ChangePasswordForm(Form):
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password = PasswordField('new_password', validators=[DataRequired()])
    new_password_repeat = PasswordField('new_password_repeat',
                                        validators=[DataRequired()])


class NewBookForm(Form):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    publisher = StringField('publisher', validators=[DataRequired()])
    gender = StringField('gender', validators=[DataRequired()])

class NewCollectionForm(Form):
    book = QuerySelectField(query_factory=lambda: Book.query.all())
    quality = StringField('quality', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])

class EditCollectionForm(Form):
    book = QuerySelectField(query_factory=lambda: Book.query.all())
    quality = StringField('quality', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])

class NewSaleForm(Form):
    action_id = HiddenField('action')
    book = StringField('book')
    price = DecimalField('pricing', validators=[DataRequired()])
    shipping = DecimalField('shipping', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])

