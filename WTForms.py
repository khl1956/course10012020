from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms import validators


class GroupsForm(Form):

    code = StringField("Code: ", [validators.data_required("Please, enter a code of the group.")])

    submit = SubmitField("Enter")


class SubjectsForm(Form):

    name = StringField("Name: ", [validators.data_required("Please, enter a name of the subject.")])

    submit = SubmitField("Enter")


class StudentsForm(Form):

    first_name = StringField("First name: ", [validators.data_required("Please, enter a first name of the student.")])
    last_name = StringField("Last name: ", [validators.data_required("Please, enter a last name of the student.")])
    study_book = StringField("Study book: ", [validators.data_required("Please, enter a study book of the student.")])
    group_code = StringField("Group code: ", [validators.data_required("Please, enter a group code of the student.")])

    submit = SubmitField("Enter")


class CountryForm(Form):

    name = StringField("Country name: ", [validators.data_required("Please, enter a country name.")])
    population = IntegerField("Population: ", [validators.number_range(0, )])
    gov = StringField("Government type (унітарна, парламентська): ", [validators.any_of('унітарна', 'парламентська')])
    year_creation = IntegerField("Year of creation: ")

    submit = SubmitField("Enter")