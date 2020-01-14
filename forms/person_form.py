from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from flask_wtf.file import FileField
from wtforms import validators


class PersonForm(Form):

    person_login = StringField("Login: ",[
                                    validators.DataRequired("Please enter your login."),
                                    validators.Length(3, 20, "Login should be from 3 to 20 symbols")
                                 ])

    person_password = PasswordField("Password: ",[
                                    validators.DataRequired("Please enter your password."),
                                    validators.Length(8, 20, "Password should be from 8 to 20 symbols")
                                 ])

    person_name = StringField("Name: ", [
                                   validators.DataRequired("Please enter your name."),
                                   validators.Length(3, 20, "Name should be from 3 to 20 symbols")
                               ])

    person_surname = StringField("Surname: ",[
                                       validators.DataRequired("Please enter your surname."),
                                       validators.Length(3, 20, "Surname should be from 3 to 20 symbols")
                                   ])


    person_email = StringField("Email: ",[
                                 validators.DataRequired("Please enter your email."),
                                 validators.Email("Wrong email format")
                                 ])




    person_birthday = DateField("Birthday: ", [validators.DataRequired("Please enter your birthday.")])


    person_status = HiddenField()


    submit = SubmitField("Save")
    


