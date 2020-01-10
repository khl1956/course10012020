from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, TextAreaField, IntegerField
from wtforms import validators


class FunctionForm(Form):
   # function_name = HiddenField()

   function_name = StringField("Name: ",[
                                    validators.DataRequired("Please enter your name."),
                                    validators.Length(3, 100, "Name should be from 3 to 100 symbols")
                                 ])

   function_text = TextAreaField("Text: ", [
                                   validators.DataRequired("Please enter your function text."),
                                   validators.Length(3, 500, "Text should be from 3 to 500 symbols")
                               ])

   counter_of_tests = IntegerField("Count of tests: ", [
                                   validators.DataRequired("Please enter counter of tests."),
                                   validators.NumberRange(5, 100, "Counter of tests should be from 5 to 100")
                               ])

   counter_of_params = IntegerField("Count of parameters: ", [
                                   validators.DataRequired("Please enter counter of params."),
                                   validators.NumberRange(1, 2, "Counter of params should be from 1 to 2 symbols")
   ])

   # person_login_fk = StringField("Person login: ", [
   #                                 validators.DataRequired("Please enter your surname."),
   #                                 validators.Length(3, 20, "Name should be from 3 to 20 symbols")
   #                             ])

   person_login_fk = HiddenField()

   submit = SubmitField("Save")


