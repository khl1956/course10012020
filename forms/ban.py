from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, TextAreaField, IntegerField
from wtforms import validators


class BanForm(Form):
   # function_name = HiddenField()

   person_login = HiddenField()

   text = TextAreaField("Description: ", [
                                   validators.DataRequired("Please enter bdn description."),
                                   validators.Length(3, 100, "Description should be from 3 to 500 symbols")
                               ])

   # person_login_fk = StringField("Person login: ", [
   #                                 validators.DataRequired("Please enter your surname."),
   #                                 validators.Length(3, 20, "Name should be from 3 to 20 symbols")
   #                             ])



   submit = SubmitField("Save")


