from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import Email, regexp, Length, Required


class AuthForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    password = StringField('password', validators=[Length(6, 20)])


class SolveLaboratoryForm(FlaskForm):
    attempt = IntegerField('Attempt')
    laboratory_theme = StringField('Laboratory theme')
    implementation_content = TextAreaField('Implementation content')


class AddResourceForm(FlaskForm):
    resource_name = StringField('Resource name', validators=[Required])
    resource_content = StringField('Resource content', validators=[Required])
    resource_source = StringField('Resource source', validators=[Required])
    lection_name = SelectField('Lecture name', validators=[Required])
