from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from forms.person_form import PersonForm
from forms.function_form import FunctionForm
from forms.tectcase_form import TestCaseForm
from forms.ban import BanForm
from flask_security import RoleMixin, SQLAlchemyUserDatastore, Security, UserMixin, login_required, current_user
from flask_security.utils import hash_password
from flask_security.decorators import roles_accepted, roles_accepted
import plotly
import json
import plotly.graph_objs as go
from random import randint
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from math import exp
from random import uniform

# from neupy import algorithms

app = Flask(__name__)
app.secret_key = 'key'

app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['USER_EMAIL_SENDER_EMAIL'] = "noreply@example.com"



ENV = 'devvv'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01200120@localhost/Lab_4'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://szmzlvhzrdaukh:296d273e5ce10e9637645d6fee54be067ed9f9b342877a87fa9fc3be23e30784@ec2-54-243-208-234.compute-1.amazonaws.com:5432/degcmpf6t5n46b'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

person_roles = db.Table('person_roles',
    db.Column("person_id", db.Integer(), db.ForeignKey('orm_person.id')),
    db.Column("role_id", db.Integer(), db.ForeignKey('role.id'))
)

ww = []

y = 0

class Neuron_I:
    def __init__(self, number):
        self.n = number

    def activation(self):
        self.y = self.y * 1

    def training(self, x):
        self.y = x[self.n]
        self.activation()
        return self.y


class Neuron_M:
    def __init__(self, counr, i):
        self.i = i
        # w = [[-0.1, 0.1, 0.2], [-0.2, 0.5, 0.3], [-0.1, 0.1, 0.2]]
        w = []
        for i in range(counr + 1):
            w.append(uniform(-1, 1))
        self.w = w


    def sumo(self):
        sums = 0
        for i in range(len(self.x)):
            sums += float(self.x[i]) * self.w[i]
        self.y = sums
        ww.append(self.w)

    def activation(self):
        self.y = 1 / (1 + exp(-1 * self.y))

    def correction(self):
        dop = neuron_3_1.beck()
        sigma = self.y * (1 - self.y) * dop[self.i]
        # sigma = sig
        delta_w = []
        for i in range(len(self.x)):
            delta_w.append(self.x[i] * sigma )
            self.w[i] = self.w[i] + delta_w[i]

    def training(self, x):
        self.x = x
        self.sumo()
        self.activation()
        return self.y


class Neuron_U:
    def __init__(self, counr):
        # w = [0.5, 0.1, -0.1, 0.2]
        w = []
        for i in range(counr + 1):
            w.append(uniform(-1, 1))
        self.w = w

    def sumo(self):
        sums = 0
        for i in range(len(self.x)):
            sums += float(self.x[i]) * self.w[i]
        self.y = sums
        ww.append(self.w)

    def activation(self):
        self.y = 1 / (1 + exp(-1 * self.y))

    def mistake(self):
        self.delta = abs((self.y - y) / y)
        return self.delta

    def correction(self):
        sigma = self.y * (1 - self.y) * (y - self.y)
        delta_w = []
        for i in range(len(self.x)):
            delta_w.append(self.x[i] * sigma )
            self.w[i] = self.w[i] + delta_w[i]

    def training(self, x):
        self.x = x
        self.sumo()
        self.activation()
        # self.mistake()
        print("Y - " + str(self.y))
        return self.y

    def beck(self):
        res = []
        sigma = self.y * (1 - self.y) * (y - self.y)
        for i in range(3):
            res.append(sigma * self.w[i])
        return res



class ormPersons(db.Model, UserMixin):
    __tablename__ = 'orm_person'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255), nullable=False)
    person_name = db.Column(db.String(50), nullable=False)
    person_surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    person_birthday = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean(), nullable=True)
    message = db.Column(db.String(100), nullable=True)

    roles = db.relationship("Role", secondary=person_roles, backref=db.backref('persons', lazy='dynamic'))

    Persons_Function = db.relationship("ormFunction")


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)





class ormFunction(db.Model):
    __tablename__ = 'orm_function'

    function_name = db.Column(db.String(100), primary_key=True)
    function_text = db.Column(db.String(1000), nullable=False)
    counter_of_tests = db.Column(db.Integer, nullable=False)
    counter_of_params = db.Column(db.Integer, nullable=False)

    person_login_fk = db.Column(db.String(50), db.ForeignKey('orm_person.username'))

    Function_TescCase = db.relationship("ormTestCase")
    TestCase_Analiz = db.relationship("ormAnaliz")


class ormTestCase(db.Model):
    __tablename__ = 'orm_testcase'

    testcase_id = db.Column(db.Integer, db.Sequence('testcase_id_seq', start=6, increment=1), primary_key=True)

    function_name_fk = db.Column(db.String(100), db.ForeignKey('orm_function.function_name'))

    TestCase_Parameters = db.relationship("ormParameters")
    TestCase_Result = db.relationship("ormResult")


class ormParameters(db.Model):
    __tablename__ = 'orm_parameters'

    parameters_index = db.Column(db.Integer, primary_key=True)
    testcase_iteration = db.Column(db.Integer, primary_key=True)
    parameters_value = db.Column(db.String(100), nullable=False)
    testcase_type = db.Column(db.String(20), primary_key=True)

    testcase_id = db.Column(db.Integer, db.ForeignKey('orm_testcase.testcase_id'), primary_key=True)


class ormResult(db.Model):
    __tablename__ = 'orm_result'

    result_value = db.Column(db.Integer, nullable=False)
    testcase_iteration = db.Column(db.Integer, primary_key=True)

    testcase_id = db.Column(db.Integer, db.ForeignKey('orm_testcase.testcase_id'), primary_key=True)


class ormAnaliz(db.Model):
    __tablename__ = 'orm_analiz'
    couunt_of_itereration = db.Column(db.Integer, primary_key=True)
    true_data = db.Column(db.Integer, nullable=False)
    false_data = db.Column(db.Integer, nullable=False)

    function_name_fk = db.Column(db.String(100), db.ForeignKey('orm_function.function_name'), primary_key=True)


user_datastore = SQLAlchemyUserDatastore(db, ormPersons, Role)
security = Security(app, user_datastore)
# user_manager = UserManager(app, db, ormPersons)


# db.session.query(ormResult).delete()
# db.session.query(ormParameters).delete()
# db.session.query(ormTestCase).delete()
# db.session.query(ormFunction).delete()
# db.session.query(ormPersons).delete()

@app.route('/new', methods=['GET', 'POST'])
def new():
    db.create_all()

    Dima = user_datastore.create_user(username="Dima",
                      password="0000",
                      person_name="Dima",
                      person_surname="Koltsov",
                      email="dik19994@gmail.com",
                      person_birthday="1999-01-01")

    # Adm = user_datastore.create_role(
    #     name = "Admin"
    # )

    # Dima.roles.append(Role(name="Admin"))

    # Dima = ormPersons(id=1,
    #                   username="Dima",
    #                   password="0000",
    #                   person_name="Dima",
    #                   person_surname="Koltsov",
    #                   email="dik19994@gmail.com",
    #                   person_birthday="1999-01-01",
    #                   person_status="user",
    #                   person_photo=None
    # )

    Vlad = user_datastore.create_user(
                      username="Vlad",
                      password="0000",
                      person_name="Vlad",
                      person_surname="Kanevckyi",
                      email="vladkaneve@gmail.com",
                      person_birthday="1999-02-04"
                      )


    Vadim = user_datastore.create_user(
                       username="Vadim",
                       password="0000",
                       person_name="Vadim",
                       person_surname="Pits",
                       email="vadim@ukr.net",
                       person_birthday="1998-10-29"
                       )

    Yarik = user_datastore.create_user(
                       username="Yarik",
                       password="0000",
                       person_name="Yarik",
                       person_surname="Artemenko",
                       email="yarik@ukr.net",
                       person_birthday="1999-08-11"
                       )

    Srhey = user_datastore.create_user(
                       username="Srhey",
                       password="0000",
                       person_name="Srhey",
                       person_surname="Gorodnuk",
                       email="srhey@ukr.net",
                       person_birthday="1999-10-02"
                       )

    Adm = Role(
        name="Admin"
    )


    Us = Role(
        name="User"
    )

    Ban = Role(
        name="Ban"
    )

    add = ormFunction(function_name="add",
                      function_text="def add(a, b):\n\treturn a+b",
                      counter_of_tests=10,
                      counter_of_params = 2)

    sub = ormFunction(function_name="sub",
                      function_text="def sub(a, b):\n\treturn a-b",
                      counter_of_tests=10,
                      counter_of_params = 2)

    mult = ormFunction(function_name="mult",
                       function_text="def mult(a, b):\n\treturn a*b",
                       counter_of_tests=10,
                       counter_of_params = 2)

    div = ormFunction(function_name="div",
                      function_text="def div(a, b):\n\treturn a/b",
                      counter_of_tests=10,
                      counter_of_params = 2)

    abs = ormFunction(function_name="abs",
                      function_text="def abs(a):\n\treturn abs(a)",
                      counter_of_tests=10,
                      counter_of_params = 1)

    Vlad.Persons_Function.append(add)
    Vlad.Persons_Function.append(sub)
    Vadim.Persons_Function.append(mult)
    Yarik.Persons_Function.append(div)
    Srhey.Persons_Function.append(abs)

    Dima.roles.append(Adm)
    Vlad.roles.append(Us)
    Vadim.roles.append(Us)
    Yarik.roles.append(Us)
    Srhey.roles.append(Us)


    i_1 = ormTestCase(testcase_id=1)
    i_2 = ormTestCase(testcase_id=2)
    i_3 = ormTestCase(testcase_id=3)
    i_4 = ormTestCase(testcase_id=4)
    i_5 = ormTestCase(testcase_id=5)

    add.Function_TescCase.append(i_1)
    add.Function_TescCase.append(i_1)
    add.Function_TescCase.append(i_1)
    add.Function_TescCase.append(i_1)
    add.Function_TescCase.append(i_1)
    sub.Function_TescCase.append(i_2)
    mult.Function_TescCase.append(i_3)
    div.Function_TescCase.append(i_4)
    abs.Function_TescCase.append(i_5)

    p_0i_1_1 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=2)

    p_1i_1_1 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=3)

    p_0i_2_1 = ormParameters(parameters_index=0,
                             testcase_iteration=2,
                             testcase_type='int',
                             parameters_value=4)

    p_1i_2_1 = ormParameters(parameters_index=1,
                             testcase_iteration=2,
                             testcase_type='int',
                             parameters_value=5)

    p_0i_3_1 = ormParameters(parameters_index=0,
                             testcase_iteration=3,
                             testcase_type='int',
                             parameters_value=10)

    p_1i_3_1 = ormParameters(parameters_index=1,
                             testcase_iteration=3,
                             testcase_type='int',
                             parameters_value=31)

    p_0i_4_1 = ormParameters(parameters_index=0,
                             testcase_iteration=4,
                             testcase_type='int',
                             parameters_value=44)

    p_1i_4_1 = ormParameters(parameters_index=1,
                             testcase_iteration=4,
                             testcase_type='int',
                             parameters_value=-5)

    p_0i_5_1 = ormParameters(parameters_index=0,
                             testcase_iteration=5,
                             testcase_type='int',
                             parameters_value=8)

    p_1i_5_1 = ormParameters(parameters_index=1,
                             testcase_iteration=5,
                             testcase_type='int',
                             parameters_value=12)

    p_0i_1_2 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=4)

    p_1i_1_2 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=5)

    p_0i_1_3 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=2)

    p_1i_1_3 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=5)

    p_0i_1_4 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=100)

    p_1i_1_4 = ormParameters(parameters_index=1,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=50)

    p_0i_1_5 = ormParameters(parameters_index=0,
                             testcase_iteration=1,
                             testcase_type='int',
                             parameters_value=-7)

    i_1.TestCase_Parameters.append(p_0i_1_1)
    i_1.TestCase_Parameters.append(p_1i_1_1)
    i_1.TestCase_Parameters.append(p_0i_2_1)
    i_1.TestCase_Parameters.append(p_1i_2_1)
    i_1.TestCase_Parameters.append(p_0i_3_1)
    i_1.TestCase_Parameters.append(p_1i_3_1)
    i_1.TestCase_Parameters.append(p_0i_4_1)
    i_1.TestCase_Parameters.append(p_1i_4_1)
    i_1.TestCase_Parameters.append(p_0i_5_1)
    i_1.TestCase_Parameters.append(p_1i_5_1)

    i_2.TestCase_Parameters.append(p_0i_1_2)
    i_2.TestCase_Parameters.append(p_1i_1_2)

    i_3.TestCase_Parameters.append(p_0i_1_3)
    i_3.TestCase_Parameters.append(p_1i_1_3)

    i_4.TestCase_Parameters.append(p_0i_1_4)
    i_4.TestCase_Parameters.append(p_1i_1_4)

    i_5.TestCase_Parameters.append(p_0i_1_5)

    iter_1_1 = ormResult(result_value=5,
                         testcase_iteration=1)

    iter_1_2 = ormResult(result_value=9,
                         testcase_iteration=2)

    iter_1_3 = ormResult(result_value=41,
                         testcase_iteration=3)

    iter_1_4 = ormResult(result_value=49,
                         testcase_iteration=4)

    iter_1_5 = ormResult(result_value=20,
                         testcase_iteration=5)

    iter_2_1 = ormResult(result_value=-1,
                         testcase_iteration=-1)

    iter_3_1 = ormResult(result_value=20,
                         testcase_iteration=1)

    iter_4_1 = ormResult(result_value=2,
                         testcase_iteration=1)

    iter_5_1 = ormResult(result_value=7,
                         testcase_iteration=1)

    i_1.TestCase_Result.append(iter_1_1)
    i_1.TestCase_Result.append(iter_1_2)
    i_1.TestCase_Result.append(iter_1_3)
    i_1.TestCase_Result.append(iter_1_4)
    i_1.TestCase_Result.append(iter_1_5)
    i_2.TestCase_Result.append(iter_2_1)
    i_3.TestCase_Result.append(iter_3_1)
    i_4.TestCase_Result.append(iter_4_1)
    i_5.TestCase_Result.append(iter_5_1)

    db.session.add_all([Dima, Vlad, Vadim, Yarik, Srhey, add, sub, mult, div, abs, i_1, i_1, i_1, i_1, i_1,
                        i_2, i_3, i_4, i_5, p_0i_1_1, p_1i_1_1, p_0i_2_1, p_1i_2_1, p_0i_3_1, p_1i_3_1, p_0i_4_1,
                        p_1i_4_1, p_0i_5_1,p_1i_5_1, p_0i_1_2, p_1i_1_2, p_0i_1_3, p_1i_1_3, p_0i_1_4, p_1i_1_4,
                        p_0i_1_5, iter_1_1, iter_1_2, iter_1_3, iter_1_4, iter_1_5, iter_2_1, iter_3_1, iter_4_1,
                        iter_5_1, Ban])

    db.session.commit()

    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    db.create_all()

    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/person', methods=['GET'])
@login_required
@roles_accepted('Admin', 'User')
def person():
    if current_user.has_role('Admin'):
        result = db.session.query(ormPersons).all()
    else:
        result = db.session.query(ormPersons).filter(ormPersons.id == current_user.id).all()

    return render_template('person.html', persons=result)


@app.route('/new_person', methods=['GET', 'POST'])
def new_person():
    form = PersonForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('person_form.html', form=form, form_name="New person", action="new_person")
        else:
            new_person = user_datastore.create_user(
                username=form.person_login.data,
                password=form.person_password.data,
                person_name=form.person_name.data,
                person_surname=form.person_surname.data,
                email=form.person_email.data,
                person_birthday=form.person_birthday.data.strftime("%d-%b-%y")
            )

            role = db.session.query(Role).filter(Role.name == "User").one()

            new_person.roles.append(role)

            db.session.add(new_person)
            db.session.commit()

            return redirect(url_for('person'))

    return render_template('person_form.html', form=form, form_name="New person", action="new_person")


@app.route('/edit_person', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', "User")
def edit_person():
    form = PersonForm()

    if request.method == 'GET':

        person_login = request.args.get('person_login')
        person = db.session.query(ormPersons).filter(ormPersons.username == person_login).one()

        # fill form and send to user
        form.person_login.data = person.username
        form.person_password.data = person.password
        form.person_name.data = person.person_name
        form.person_surname.data = person.person_surname
        form.person_email.data = person.email
        form.person_birthday.data = person.person_birthday

        return render_template('person_form.html', form=form, form_name="Edit person", action="edit_person")


    else:

        if not form.validate():
            return render_template('person_form.html', form=form, form_name="Edit person", action="edit_person")
        else:
            # find user
            person = db.session.query(ormPersons).filter(ormPersons.username == form.person_login.data).one()

            # update fields from form data
            person.username = form.person_login.data
            person.password = hash_password(form.person_password.data)
            person.person_name = form.person_name.data
            person.person_surname = form.person_surname.data
            person.email = form.person_email.data
            person.person_birthday = form.person_birthday.data.strftime("%d-%b-%y")

            db.session.commit()

            return redirect(url_for('person'))


@app.route('/delete_person', methods=['POST'])
@login_required
@roles_accepted('Admin')
def delete_person():
    person_login = request.form['person_login']

    result = db.session.query(ormPersons).filter(ormPersons.username == person_login).one()

    db.session.delete(result)
    db.session.commit()

    return person_login


@app.route('/function', methods=['GET'])
@login_required
@roles_accepted('Admin', 'User')
def function():
    if current_user.has_role('Admin'):
        result = db.session.query(ormFunction).all()
    else:
        result = db.session.query(ormFunction).filter(ormFunction.person_login_fk == current_user.username).all()

    return render_template('function.html', functions=result)


@app.route('/new_function/<person_login>', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'User')
def new_function(person_login):
    form = FunctionForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('function_form.html', form=form, form_name="New function", action="new_function")
        else:
            new_function = ormFunction(
                function_name=form.function_name.data,
                function_text=form.function_text.data,
                counter_of_tests=form.counter_of_tests.data,
                counter_of_params=form.counter_of_params.data,
                person_login_fk=person_login
            )

            db.session.add(new_function)
            db.session.commit()

            # new_testcase = ormTestCase(
            #     function_name_fk=form.function_name.data,
            # )
            # db.session.add(new_testcase)
            # db.session.commit()
            # id = db.session.query(ormTestCase.testcase_id).filter(
            #     ormTestCase.function_name_fk == form.function_name.data).one()[0]
            #
            #
            # for i in range(form.counter_of_tests.data):
            #     for j in range(form.counter_of_params.data):
            #         new_parameters = ormParameters(
            #             parameters_index=j,
            #             testcase_iteration=i,
            #             parameters_value=randint(1, 150),
            #             testcase_type="int",
            #             testcase_id=id
            #         )
            #         db.session.add(new_parameters)
            #         db.session.commit()
            #
            # params = db.session.query(ormParameters).filter(
            #     ormParameters.testcase_id == id).all()
            #
            # count = db.session.query(ormFunction.counter_of_params).filter(ormFunction.function_name == form.function_name.data).one()[0]
            #
            # for i in range(int(len(list(params)) / count)):
            #     lists = []
            #     for j in range(count):
            #         lists.append(int(list(params)[count * i + j].parameters_value))
            #     a = db.session.query(ormFunction.function_text).filter(ormFunction.function_name == form.function_name.data).one()[0]
            #     b = a.split(" ")[1]
            #     b = b.split("(")[0]
            #     exec(a)
            #     call = b + "("
            #     for k in range(count - 1):
            #         call += str(lists[k]) + ", "
            #     call += str(lists[-1]) + ")"
            #     res = eval(call)
            #
            #     new_result = ormResult(
            #         testcase_id= id,
            #         testcase_iteration= params[i].testcase_iteration,
            #         result_value=res
            #     )
            #     db.session.add(new_result)
            #     db.session.commit()
            #
            #
            #     print(lists)
            #     print(res)


            return redirect(url_for('function'))

    return render_template('function_form.html', form=form, form_name="New function",
                           action="new_function/" + person_login)


@app.route('/edit_function', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'User')
def edit_function():
    form = FunctionForm()

    if request.method == 'GET':

        function_name = request.args.get('function_name')
        function = db.session.query(ormFunction).filter(ormFunction.function_name == function_name).one()

        # fill form and send to user
        form.function_name.data = function.function_name
        form.function_text.data = function.function_text
        form.counter_of_tests.data = function.counter_of_tests
        form.counter_of_params.data = function.counter_of_params
        form.person_login_fk.data = function.person_login_fk

        return render_template('function_form.html', form=form, form_name="Edit function", action="edit_function")


    else:

        if not form.validate():
            return render_template('function_form.html', form=form, form_name="Edit function", action="edit_function")
        else:
            # find user
            function = db.session.query(ormFunction).filter(ormFunction.function_name == form.function_name.data).one()

            # update fields from form data
            function.function_name = form.function_name.data
            function.function_text = form.function_text.data
            function.counter_of_tests = form.counter_of_tests.data
            function.counter_of_params = form.counter_of_params.data

            function.person_login_fk = form.person_login_fk.data

            db.session.commit()

            return redirect(url_for('function'))


@app.route('/delete_function', methods=['POST'])
@login_required
@roles_accepted('Admin', 'User')
def delete_function():
    function_name = request.form['function_name']

    result = db.session.query(ormFunction).filter(ormFunction.function_name == function_name).one()
    analiz = db.session.query(ormAnaliz).filter(ormAnaliz.function_name_fk == function_name).all()

    for i in analiz:
        db.session.delete(i)

    id_list = db.session.query(ormTestCase.testcase_id).filter(ormTestCase.function_name_fk == function_name).all()

    for i in id_list:
        result3 = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == i[0]).one()
        result2 = db.session.query(ormResult).filter(ormResult.testcase_id == i[0]).all()
        result1 = db.session.query(ormParameters).filter(ormParameters.testcase_id == i[0]).all()

        for i in result1:
            db.session.delete(i)
        for i in result2:
            db.session.delete(i)
        db.session.delete(result3)
        db.session.commit()

    db.session.delete(result)
    db.session.commit()

    return function_name


@app.route('/parameters', methods=['GET'])
@login_required
@roles_accepted('Admin', 'User')
def parameters():
    result = db.session.query(ormParameters).all()

    return render_template('parameters.html', parameters=result)



@app.route('/result', methods=['GET'])
@login_required
@roles_accepted('Admin', 'User')
def result():
    result = db.session.query(ormResult).all()

    return render_template('result.html', results=result)



@app.route('/testcase', methods=['GET'])
@app.route('/testcase/<function_name>', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def testcase(function_name = None):
    if current_user.has_role('Admin'):
        result = db.session.query(ormTestCase).all()
    else:
        result = db.session.query(ormTestCase).filter(ormTestCase.function_name_fk == function_name)

    # result = db.session.query(ormTestCase).all()

    return render_template('testcase.html', testcases=result)


@app.route('/new_testcase/<function_name>', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def new_testcase(function_name):
    form = TestCaseForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('testcase_form.html', form=form, form_name="New testcase", action="new_testcase")
        else:
            new_testcase = ormTestCase(
                testcase_id=form.testcase_id.data,
                function_name_fk=function_name,
            )

            db.session.add(new_testcase)
            db.session.commit()

            return redirect(url_for('testcase'))

    return render_template('testcase_form.html', form=form, form_name="New testcase",
                           action="new_testcase/" + function_name)


@app.route('/edit_testcase', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def edit_testcase():
    form = TestCaseForm()

    if request.method == 'GET':

        testcase_id = request.args.get('testcase_id')
        testcase = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == testcase_id).one()

        # fill form and send to user
        form.testcase_id.data = testcase.testcase_id
        form.function_name_fk.data = testcase.function_name_fk

        return render_template('testcase_form.html', form=form, form_name="Edit testcase", action="edit_testcase")


    else:

        if not form.validate():
            return render_template('testcase_form.html', form=form, form_name="Edit testcase", action="edit_testcase")
        else:
            # find user
            testcase = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == form.testcase_id.data).one()

            # update fields from form data
            testcase.testcase_id = form.testcase_id.data
            testcase.function_name_fk = form.function_name_fk.data

            db.session.commit()

            return redirect(url_for('testcase'))


@app.route('/delete_testcase', methods=['POST'])
@login_required
@roles_accepted("User", "Admin")
def delete_testcase():
    testcase_id = request.form['testcase_id']

    result3 = db.session.query(ormTestCase).filter(ormTestCase.testcase_id == testcase_id).one()
    result2 = db.session.query(ormResult).filter(ormResult.testcase_id == testcase_id).all()
    result1 = db.session.query(ormParameters).filter(ormParameters.testcase_id == testcase_id).all()

    for i in result1:
        db.session.delete(i)
    for i in result2:
        db.session.delete(i)
    db.session.delete(result3)
    db.session.commit()

    return testcase_id


# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     query1 = (
#         db.session.query(
#             ormPersons.person_login,
#             func.count(ormFunction.function_name).label('function_count')
#         ).
#             outerjoin(ormFunction).
#             group_by(ormPersons.person_login)
#     ).all()
#
#     query2 = (
#         db.session.query(
#             ormFunction.function_name,
#             func.count(ormTestCase.testcase_id).label('testcase_count')
#         ).
#             outerjoin(ormTestCase).
#             group_by(ormFunction.function_name)
#     ).all()
#
#     login, function_count = zip(*query1)
#     bar = go.Bar(
#         x=login,
#         y=function_count
#     )
#
#     name, testcase_count = zip(*query2)
#     pie = go.Pie(
#         labels=name,
#         values=testcase_count
#     )
#
#     data = {
#         "bar": [bar],
#         "pie": [pie]
#     }
#     graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#
#     return render_template('dashboard.html', graphsJSON=graphsJSON)


# @app.route('/login_2', methods=['GET', 'POST'])
# def login():
#     form = Login()
#
#     if request.method == 'POST':
#         if not form.validate():
#             return render_template('login.html', form=form, form_name="Sign up", action="login")
#
#         else:
#             try:
#                 result = db.session.query(ormPersons).filter(ormPersons.person_login == form.person_login.data).one()
#             except:
#                 return render_template('login.html', form=form, form_name="Sign up", action="login",
#                                        login="Неправельный логин или пароль")
#
#             if result.person_password == form.person_password.data:
#                 session["login"] = form.person_login.data
#                 # role = Role(name='secret')
#                 return render_template("index.html")
#             else:
#                 return render_template('login.html', form=form, form_name="Sign up", action="login", login="Неправельный логин или пароль")
#
#     return render_template('login.html', form=form, form_name="Sign up", action="login")
#
#
# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#
#     return render_template('login.html', form=form, form_name="Sign up", action="login")


@app.route('/func/<function_name>/<id>', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def func(function_name, id):
    # res = db.session.query(ormFunction).join(ormTestCase).join(
    #     ormParameters).join(ormResult).all()

    res = db.session.query(ormFunction.function_name, ormTestCase.testcase_id, ormResult.result_value, ormParameters.testcase_iteration)
    res = res.filter(ormFunction.function_name == ormTestCase.function_name_fk)
    res = res.filter(ormTestCase.testcase_id == ormResult.testcase_id)
    res = res.filter(ormTestCase.testcase_id == ormParameters.testcase_id)
    res = res.filter(ormParameters.testcase_iteration == ormResult.testcase_iteration).filter(ormTestCase.testcase_id == id).filter(ormTestCase.function_name_fk==function_name).group_by(ormFunction.function_name,
                ormTestCase.testcase_id, ormResult.result_value, ormParameters.testcase_iteration).all()


    res_data = []
    for i in range(len(res)):
        res2 = db.session.query(ormParameters.parameters_value).filter(
            ormParameters.testcase_iteration == res[i].testcase_iteration).filter(ormParameters.testcase_id == res[i].testcase_id).all()

        res_data.append([res[i].function_name, res[i].result_value, res2])



    return render_template('func.html', form=res_data)


@app.route('/function_details/<function_name>', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def function_details(function_name):
    res = db.session.query(ormTestCase).filter(ormTestCase.function_name_fk == function_name)

    # res = db.session.query(ormFunction.function_name, ormTestCase.testcase_id, ormResult.result_value, ormParameters.testcase_iteration)
    # res = res.filter(ormFunction.function_name == ormTestCase.function_name_fk)
    # res = res.filter(ormTestCase.testcase_id == ormResult.testcase_id)
    # res = res.filter(ormTestCase.testcase_id == ormParameters.testcase_id)
    # res = res.filter(ormParameters.testcase_iteration == ormResult.testcase_iteration).group_by(ormFunction.function_name,
    #             ormTestCase.testcase_id, ormResult.result_value, ormParameters.testcase_iteration).all()
    #
    #
    # res_data = []
    # for i in range(len(res)):
    #     res2 = db.session.query(ormParameters.parameters_value).filter(
    #         ormParameters.testcase_iteration == res[i].testcase_iteration).filter(ormParameters.testcase_id == res[i].testcase_id).all()
    #
    #     res_data.append([res[i].function_name, res[i].result_value, res2])



    return render_template('function_details.html', form=res)



@app.route('/correlation/<function_name>', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def correlation(function_name):
    res = db.session.query(ormAnaliz).filter(ormAnaliz.function_name_fk == function_name).all()

    liste = []
    for i in range(len(res)):
        liste.append([])
        liste[i].append(res[i].false_data)
        liste[i].append(res[i].true_data)
        liste[i].append(i)
    db.session.close()
    matrix_data = np.matrix(liste)
    df = pd.DataFrame(matrix_data, columns=('par1', 'par2', 'result'))

    print(df)

    scaler = StandardScaler()
    scaler.fit(df[['par1', 'par2']])
    train_X = scaler.transform(df[['par1', 'par2']])
    # print(train_X, df[["count_files"]])
    reg = LinearRegression().fit(train_X, df[["result"]])

    test_array = [[liste[-1][0], liste[-1][1]]]
    test = scaler.transform(test_array)
    result = reg.predict(test)


    return render_template('regretion.html', row=int(round(result[0, 0])), test_data=test_array[0],
                           coef=reg.coef_[0],
                           coef1=reg.intercept_)


@app.route('/ban/<person_login>', methods=['GET', 'POST'])
@login_required
@roles_accepted("Admin")
def ban(person_login):
    form = BanForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('person_form.html', form=form, form_name="New person", action="new_person")
        else:

            per = db.session.query(ormPersons).filter(ormPersons.username == person_login).one()

            id = per.roles[0].id

            rol = db.session.query(Role).filter(Role.id == id).one()
            ban = db.session.query(Role).filter(Role.id == 3).one()

            per.roles.remove(rol)
            per.roles.append(ban)


            per.message = form.text.data
            db.session.add(per)
            db.session.commit()

            return redirect(url_for('root'))

    return render_template('ban_form.html', form=form, form_name="Ban", action="ban/"+person_login)


@app.route('/unban/<person_login>', methods=['GET', 'POST'])
@login_required
@roles_accepted("Admin")
def unban(person_login):

    per = db.session.query(ormPersons).filter(ormPersons.username == person_login).one()

    # id = per.roles[0].id

    # rol = db.session.query(Role).filter(Role.id == id).one()
    us = db.session.query(Role).filter(Role.id == 2).one()
    bun = db.session.query(Role).filter(Role.id == 3).one()

    per.roles.remove(bun)
    per.roles.append(us)


    per.message = None
    db.session.add(per)
    db.session.commit()

    return redirect(url_for('person'))


neuron_3_1 = Neuron_U(3)

@app.route('/clustering/<function_name>', methods=['GET', 'POST'])
@app.route('/clustering/<function_name>/<id>', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def claster(function_name, id=None):
    if id == None:
        id = db.session.query(ormTestCase.testcase_id).filter(
        ormTestCase.function_name_fk == function_name).all()[-1][0]

    res1 = db.session.query(ormParameters.parameters_value).filter(ormParameters.parameters_index == 0).filter(ormParameters.testcase_id == id).all()
    res2 = db.session.query(ormParameters.parameters_value).filter(ormParameters.parameters_index == 1).filter(ormParameters.testcase_id == id).all()
    res3 = db.session.query(ormResult.result_value).filter(ormResult.testcase_id == id).all()

    liste = []

    ii_teach_data_x = []
    ii_teach_data_y = []
    ii_test_data_x = []
    ii_test_data_y = []
    ii_res_data_y = []
    # if len(res2) == 0:
    #     for i in range(len(res1)):
    #         res2.append((0,))

    # liste.append(list(res1))
    # liste.append(list(res2))
    # liste.append(list(res3))

    for i in range(len(res1)):
        liste.append([])
        liste[i].append(int(res1[i][0]))
        if len(res2) != 0:
            liste[i].append(int(res2[i][0]))
        liste[i].append(int(res3[i][0]))
    matrix_data = np.matrix(liste)
    if len(res2) == 0:
        df = pd.DataFrame(matrix_data, columns=('par1', 'result'))
    else:
        df = pd.DataFrame(matrix_data, columns=('par1', 'par2', 'result'))
    print(df)
    X = df
    print(X)
    count_clasters = 2
    print(count_clasters)
    kmeans = KMeans(n_clusters=count_clasters, random_state=0).fit(X)
    # print(kmeans)
    count_columns = len(X.columns)
    # test_list = [0] * count_columns
    # test_list[0] = 1
    # test_list[1] = 1
    # test_list[2] = 1
    # print(test_list)
    iter = 0
    count_elements = [0, 0]
    for i in matrix_data:
        if kmeans.predict(i)[0] == 0:
            count_elements[0] += 1
            if len(res2) == 0:
                ii_teach_data_x.append([int(liste[iter][0])])
                ii_teach_data_y.append([int(liste[iter][1])])
            else:
                ii_teach_data_x.append([int(liste[iter][0]), int(liste[iter][1])])
                ii_teach_data_y.append([int(liste[iter][2])])
        else:
            count_elements[1] += 1
            if len(res2) == 0:
                ii_test_data_x.append([int(liste[iter][0])])
                ii_test_data_y.append([int(liste[iter][1])])
            else:
                ii_test_data_x.append([int(liste[iter][0]), int(liste[iter][1])])
                ii_test_data_y.append([int(liste[iter][2])])
        iter += 1
    # print(kmeans.labels_)
    # print(kmeans.predict(np.array([test_list])))

    neuron_1_1 = Neuron_I(0)
    if len(res2) != 0:
        neuron_1_2 = Neuron_I(1)
    neuron_2_1 = Neuron_M(2, 0)
    neuron_2_2 = Neuron_M(2, 1)
    neuron_2_3 = Neuron_M(2, 2)


    # x = [[3, 4], [9, 11], [21, 29], [25, 35]]
    # x = [[90, 0, 8100], [62, 0, 3844], [90, 0, 8100], [42, 0, 1764], [52, 0, 2704], [16, 0, 256], [25, 0, 625],
    #      [136, 0, 18496], [58, 0, 3364], [95, 0, 9025], [11, 0, 121], [49, 0, 2401], [91, 0, 8281], [68, 0, 4624],
    #      [103, 0, 10609], [143, 0, 20449], [13, 0, 169], [112, 0, 12544], [51, 0, 2601], [137, 0, 18769]]

    x = ii_teach_data_x

    for i in range(500):
        ww = []
        print("Епоха " + str(i + 1))
        for j in range(len(x)):
            y1 = [1]
            y2 = [1]
            y3 = []
            # y = (x[j][0] + x[j][1]) / 100
            y = (ii_teach_data_y[j][0])/1000
            print("Итерация " + str(j + 1))
            y1.append(neuron_1_1.training(x[j]))
            if len(res2) != 0:
                y1.append(neuron_1_2.training(x[j]))
            y2.append(neuron_2_1.training(y1))
            y2.append(neuron_2_2.training(y1))
            y2.append(neuron_2_3.training(y1))
            y3.append(neuron_3_1.training(y2))
            neuron_3_1.correction()
            neuron_2_1.correction()
            neuron_2_2.correction()
            neuron_2_3.correction()

    print("\n\nТестування")
    for i in ii_test_data_x:
        x = [i][0]
        y1 = [1]
        y2 = [1]
        y3 = []
        ww = []
        y1.append(neuron_1_1.training(i))
        if len(res2) != 0:
            y1.append(neuron_1_2.training(i))
        y2.append(neuron_2_1.training(y1))
        y2.append(neuron_2_2.training(y1))
        y2.append(neuron_2_3.training(y1))
        y3.append(neuron_3_1.training(y2))
        ii_res_data_y.append(y3[0]*1000)



    check = db.session.query(ormAnaliz.couunt_of_itereration).filter(
        ormAnaliz.couunt_of_itereration == id).all()

    if len(check) == 0:
        new_analiz = ormAnaliz(
            couunt_of_itereration=id,
            true_data=count_elements[0],
            false_data=count_elements[1],
            function_name_fk=function_name
        )
        db.session.add(new_analiz)
        db.session.commit()


    pie = go.Pie(
        values=np.array(count_elements),
        labels=np.array(['True', 'False'])
    )
    data = {
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('clasteresation.html',count_claster=count_clasters, graphsJSON=graphsJSON,
                           train_x= ii_teach_data_x, train_y = ii_teach_data_y, test_x = ii_test_data_x, test_y = ii_test_data_y, res_y = ii_res_data_y)


# @app.route('/artificial_intelligence', methods=['GET', 'POST'])
# @login_required
# @roles_accepted("User", "Admin")
# def artificial_intelligence():
#     neuron_1_1 = Neuron_I(0)
#     # neuron_1_2 = Neuron_I(1)
#     neuron_2_1 = Neuron_M(2, 0)
#     neuron_2_2 = Neuron_M(2, 1)
#     neuron_2_3 = Neuron_M(2, 2)
#     neuron_3_1 = Neuron_U(3)
#
#     x = [[3, 4], [9, 11], [21, 29], [25, 35]]
#     x = [[90, 0, 8100], [62, 0, 3844], [90, 0, 8100], [42, 0, 1764], [52, 0, 2704], [16, 0, 256], [25, 0, 625],
#          [136, 0, 18496], [58, 0, 3364], [95, 0, 9025], [11, 0, 121], [49, 0, 2401], [91, 0, 8281], [68, 0, 4624],
#          [103, 0, 10609], [143, 0, 20449], [13, 0, 169], [112, 0, 12544], [51, 0, 2601], [137, 0, 18769]]
#
#     for i in range(300000):
#         ww = []
#         print("Епоха " + str(i + 1))
#         for j in range(len(x)):
#             y1 = [1]
#             y2 = [1]
#             y3 = []
#             # y = (x[j][0] + x[j][1]) / 100
#             y = (x[j][2]) / 100000
#             print("Итерация " + str(j + 1))
#             y1.append(neuron_1_1.training(x[j]))
#             # y1.append(neuron_1_2.training(x[j]))
#             y2.append(neuron_2_1.training(y1))
#             y2.append(neuron_2_2.training(y1))
#             y2.append(neuron_2_3.training(y1))
#             y3.append(neuron_3_1.training(y2))
#             neuron_3_1.correction()
#             neuron_2_1.correction()
#             neuron_2_2.correction()
#             neuron_2_3.correction()
#
#     print("\n\nТестування")
#     x = [[23, 0]]
#     y1 = [1]
#     y2 = [1]
#     y3 = []
#     ww = []
#     y1.append(neuron_1_1.training(x[0]))
#     # y1.append(neuron_1_2.training(x[0]))
#     y2.append(neuron_2_1.training(y1))
#     y2.append(neuron_2_2.training(y1))
#     y2.append(neuron_2_3.training(y1))
#     y3.append(neuron_3_1.training(y2))
#
#
#     return render_template('index.html')



@app.route('/testing/<function_name>', methods=['GET', 'POST'])
def testing(function_name):
    function = db.session.query(ormFunction).filter(
        ormFunction.function_name == function_name).one()

    # try:
    #     db.session.query(ormTestCase).filter(
    #     ormTestCase.function_name_fk == function_name).one()
    # except:
    new_testcase = ormTestCase(
        function_name_fk=function.function_name,
    )
    db.session.add(new_testcase)
    db.session.commit()




    id = db.session.query(ormTestCase.testcase_id).filter(
        ormTestCase.function_name_fk == function.function_name).all()[-1][0]


    for i in range(function.counter_of_tests):
        for j in range(function.counter_of_params):
            new_parameters = ormParameters(
                parameters_index=j,
                testcase_iteration=i,
                parameters_value=randint(1, 150),
                testcase_type="int",
                testcase_id=id
            )
            db.session.add(new_parameters)
            db.session.commit()

    params = db.session.query(ormParameters).filter(
        ormParameters.testcase_id == id).all()

    count = db.session.query(ormFunction.counter_of_params).filter(ormFunction.function_name == function_name).one()[0]

    for i in range(int(len(list(params)) / count)):
        lists = []
        for j in range(count):
            lists.append(int(list(params)[count * i + j].parameters_value))
        a = db.session.query(ormFunction.function_text).filter(ormFunction.function_name == function_name).one()[0]
        b = a.split(" ")[1]
        b = b.split("(")[0]
        exec(a)
        call = b + "("
        for k in range(count - 1):
            call += str(lists[k]) + ", "
        call += str(lists[-1]) + ")"
        res = eval(call)

        new_result = ormResult(
            testcase_id= id,
            testcase_iteration= params[count*i].testcase_iteration,
            result_value=res
        )
        db.session.add(new_result)
        db.session.commit()


        print(lists)
        print(res)

    # return render_template('function.html')
    return redirect(url_for("function"))

if __name__ == "__main__":
    app.debug = True
    app.run()
