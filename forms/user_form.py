from flask_wtf import Form
from wtforms import StringField,SubmitField,  PasswordField, DateField, HiddenField,IntegerField
from wtforms import validators
import re


class StudentForm(Form):

    student_id = StringField('Номер заліковки (в форматі 113ХХХ): ', [validators.Regexp(regex='^[1][1][3][0-9][0-9][0-9]$')])

    student_name = StringField('Імя (тільки українські букви): ', [validators.Regexp(regex=r'[а-яА-Я]')])

    student_surname = StringField('Імя (тільки українські букви): ', [validators.Regexp(regex=r'[а-яА-Я]')])

    student_group = StringField('Група (в форматі ХХММ, де ХХ - букви, ММ - цифри): ' , [validators.Regexp(regex='^[а-яА-Я][а-яА-Я][1-9][1-9]$')])
    student_live = StringField('Проживання (вибрати один варіант - з батьками, знімаю квартиру, в гуртожитку): ', [validators.Regexp(regex='з батьками|знімаю квартиру|в гуртожитку')])
    student_stup = StringField ('Наявність стипендії (так - є, ні - нема):', [validators.Regexp(regex='так|ні')])
    student_age = IntegerField('Вік', [validators.NumberRange(min=16)])
    student_mark = IntegerField('Середній бал (ціле число)', [validators.NumberRange(min=60, max=100)])
    submit = SubmitField("Save")


class StudentForm1(Form):
    student_name = StringField('Імя (тільки українські букви): ')

    student_surname = StringField('Прізвище (тільки українські букви): ')
    student_group = StringField('Група (в форматі ХХММ, де ХХ - букви, ММ - цифри): ' , [validators.Regexp(regex='^[а-яА-Я][а-яА-Я][1-9][1-9]$')])
    student_live = StringField('Проживання (вибрати один варіант - з батьками, знімаю квартиру, в гуртожитку): ',
                               [validators.Regexp(regex='з батьками|знімаю квартиру|в гуртожитку')])
    student_stup = StringField('Наявність стипендії (так - є, ні - нема):', [validators.Regexp(regex='так|ні')])
    student_mark = IntegerField('Середній бал (ціле число)', [validators.NumberRange(min=60, max=100)])
    student_age = IntegerField('Вік', [validators.NumberRange(min=16)])

    submit = SubmitField("Save")


class PostForm(Form):


    post_id = IntegerField('Номер допису: ')

    post_type = StringField('Тип допису (скарга чи пропозиція): ', [validators.Regexp(regex='скарга|пропозиція')])

    post_text = StringField("Текст допису: ", [
                                 validators.DataRequired("Текст допису (від 3 до 1000 символів)"),
                                 validators.Length(3, 1000, "Текст допису (від 3 до 1000 символів)")])
    stud_id = StringField('Номер заліковки (в форматі 113ХХХ): ', [validators.Regexp(regex='^[1][1][3][0-9][0-9][0-9]$')])

    disc_id = IntegerField("Номер дисципліни: ", [
        validators.DataRequired("Введіть номер дисципліни"),

    ])

    submit = SubmitField("Save")


class PostForm1(Form):


    post_type = StringField('Тип допису (скарга чи пропозиція): ', [validators.Regexp(regex=r'скарга|пропозиція')])

    post_text = StringField("Текст допису: ", [
                                 validators.DataRequired("Текст допису (від 3 до 1000 символів)"),
                                 validators.Length(3, 1000, "Текст допису (від 3 до 1000 символів)")])
    stud_id = StringField('Номер заліковки (в форматі 113ХХХ): ', [validators.Regexp(regex='^[1][1][3][0-9][0-9][0-9]$')])

    disc_id = IntegerField("Номер дисципліни: ", [
        validators.DataRequired("Введіть номер дисципліни"),

    ])

    submit = SubmitField("Save")

class DisciplineForm(Form):
    disc_id = IntegerField("Номер дисципліни: ", [
        validators.DataRequired("Введіть номер дисципліни"),

    ])

    disc_type = StringField('Вид дисципліни (математична, технічна, гуманітарна): ', [validators.Regexp(regex='математична|технічна|гуманітарна')])

    disc_name = StringField("disc_name: ",[
                                 validators.DataRequired("Please enter disc_name.")
                                           ])

    teacher_fullname = StringField("teacher_name: ", [
        validators.DataRequired("Please enter teacher_name.")
    ])
    submit = SubmitField("Save")


class DisciplineForm1(Form):
    disc_type = StringField('Вид дисципліни (математична, технічна, гуманітарна): ',
                            [validators.Regexp(regex='математична|технічна|гуманітарна')])

    teacher_fullname = StringField("teacher_name: ", [
        validators.DataRequired("Please enter teacher_name.")
    ])

    disc_name = StringField("disc_name: ", [
        validators.DataRequired("Please enter disc_name.")
    ])

    submit = SubmitField("Save")

#

class TeacherForm(Form):
    disc_id = IntegerField("disc_id: ",[
                                    validators.DataRequired("Please enter disc_id."),

                                 ])


    teacher_fullname = StringField("teacher_name: ",[
                                 validators.DataRequired("Please enter teacher_name.")
                                           ])

    teacher_phone = StringField('Номер викладача (в форматі +380ХХХХХХХХХ): ',
                          [validators.Regexp(regex='^[+][3][8][0][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$')])




    submit = SubmitField("Save")


class TeacherForm1(Form):
    disc_id = IntegerField("disc_id: ", [
        validators.DataRequired("Please enter disc_id."),

    ])

    teacher_phone = StringField('Номер викладача (в форматі +380ХХХХХХХХХ): ',
                                [validators.Regexp(
                                    regex='^[+][3][8][0][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$')])

    submit = SubmitField("Save")




class AIForm(Form):


    student_live = StringField('Проживання (вибрати один варіант - з батьками, знімаю квартиру, в гуртожитку): ', [validators.Regexp(regex='з батьками|знімаю квартиру|в гуртожитку')])
    student_stup = StringField ('Наявність стипендії (так - є, ні - нема):', [validators.Regexp(regex=r'так|ні')])
    student_age = IntegerField('Вік', [validators.NumberRange(min=16)])
    student_mark = IntegerField('Середній бал (ціле число)', [validators.NumberRange(min=60, max=100)])
    submit = SubmitField("Check")

