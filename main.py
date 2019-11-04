import plotly
import plotly.graph_objs as go
import json

from flask import render_template, flash, request
from ORM import *
from WTForms import *

app = Flask(__name__)
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jvehmagztyojdu:50a71e72bae8b4452ef0fc0f4b527617df7f199870aa772fdfb91f743cfdd0a2@ec2-54-228-207-163.eu-west-1.compute.amazonaws.com:5432/d2fqinb643acpv'

db = SQLAlchemy(app)


@app.route('/get', methods=['GET'])
def insert_trio():

    row1 = Country('Ukraine', 35-000-000, 'парламентська', 1991)
    row2 = Country('Russia', 200-000-000, 'унітарна', 1991)
    row3 = Country('USSR', 200-000-000, 'унітарна', 1918)

    select_res1 = Country.query.filter_by(name=row1.name)
    if select_res1:
        print("There is already inserted country")
        return
    select_res2 = Country.query.filter_by(name=row2.name)
    if select_res2:
        print("There is already inserted country")
        return
    select_res3 = Country.query.filter_by(name=row3.name)
    if select_res3:
        print("There is already inserted country")
        return

    db.session.add(row1)
    db.session.add(row2)
    db.session.add(row3)

    db.session.commit()


@app.route('/show', methods=['GET'])
def show_countries():

    select_result = Country.query.filter_by().all()

    return render_template('country.html', data=select_result)


@app.route('/insert', methods=['GET', 'POST'])
def insert():

    form = CountryForm()

    if request.method == 'POST':
        if not form.validate():
            flash('Validation Error.')
            return render_template('country_insert.html', form=form)
        else:
            country = Country(form.name.data, form.population.data, form.gov.data, form.year_creation.data)
            db.session.add(country)
            db.session.commit()

    select_result = Country.query.filter_by().all()

    return render_template('country.html', data=select_result)


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/groups', methods=['GET', 'POST'])
def groups():

    form = GroupsForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('groups.html', form=form)
        else:
            group = Groups(form.code.data)
            db.session.add(group)
            db.session.commit()

    select_result = Groups.query.filter_by().all()

    return render_template('groups.html', data=select_result, form=form)


@app.route('/subjects', methods=['GET', 'POST'])
def subjects():

    form = SubjectsForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('subjects.html', form=form)
        else:
            subject = Subjects(form.name.data)
            db.session.add(subject)
            db.session.commit()

    select_result = Subjects.query.filter_by().all()

    return render_template('subjects.html', data=select_result, form=form)


@app.route('/students', methods=['GET', 'POST'])
def students():

    form = StudentsForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('students.html', form=form)
        else:
            student = Students(form.first_name.data, form.last_name.data, form.study_book.data, form.group_code.data)
            db.session.add(student)
            db.session.commit()

    select_result = Students.query.filter_by().all()

    return render_template('students.html', data=select_result, form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    select_result_raw = Groups.query.filter_by().all()
    select_result = [select_result_row.code for select_result_row in select_result_raw]

    codes_starts_result = list(map(lambda s: s[:2], select_result))
    codes = list(set(codes_starts_result))
    counting_stars = [0] * len(codes)

    for no_more_counting_dollars in codes_starts_result:
        counting_stars[codes.index(no_more_counting_dollars[:2])] += 1

    bar, pie = go.Bar(x=codes, y=counting_stars, marker=dict(color='rgb(122, 122, 122)')), go.Pie(labels=codes, values=counting_stars)

    data1, data2 = [bar], [pie]
    ids = ["1", "2"]

    graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html',
                           graphJSON1=graphJSON1, graphJSON2=graphJSON2, ids=ids)


if __name__ == '__main__':
    app.run(debug=True)