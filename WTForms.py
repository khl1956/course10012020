from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, Label
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


class HotelForm(Form):

    name = StringField("Name: ", [validators.data_required("Please, enter a name of the hotel."), validators.Length(min=1)])
    avg_price = IntegerField("Average Price: ", [validators.data_required("Please, enter an average price of the hotel."), validators.number_range(min=0)])
    addr = StringField("Address: ", [validators.data_required("Please, enter an address of the hotel.")])
    star_count = IntegerField("Star Count: ", [validators.data_required("Please, enter a star count of the hotel.")])

    submit = SubmitField("Enter")