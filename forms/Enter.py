from flask_wtf import Form
from wtforms import StringField, SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators


class Enter(Form):

   user_name = StringField("Login: ",[
                                    validators.DataRequired("Please enter your Login."),
                                    validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                                 ])

   user_password = PasswordField("Password: ",[
                                    validators.DataRequired("Please enter your password."),
                                    validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                                 ])

   submit = SubmitField("Sign up")