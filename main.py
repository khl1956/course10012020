import plotly
import plotly.graph_objs as go
import json

from flask import render_template, flash, request
from ORM import *
from WTForms import *

app = Flask(__name__)
app.secret_key = 'development key'
app.config['DATABASE_URI'] = 'postgres://jvehmagztyojdu:50a71e72bae8b4452ef0fc0f4b527617df7f199870aa772fdfb91f743cfdd0a2@ec2-54-228-207-163.eu-west-1.compute.amazonaws.com:5432/d2fqinb643acpv'

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/groups', methods=['GET', 'POST'])
def groups():

    select_result = Groups.query.filter_by().all()

    form = GroupsForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('groups.html', form=form)
        else:
            group = Groups(form.code.data)
            db.session.add(group)
            db.session.commit()

    return render_template('groups.html', data=select_result, form=form)


@app.route('/subjects', methods=['GET', 'POST'])
def subjects():

    select_result = Subjects.query.filter_by().all()

    form = SubjectsForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('subjects.html', form=form)
        else:
            subject = Subjects(form.name.data)
            db.session.add(subject)
            db.session.commit()

    return render_template('subjects.html', data=select_result, form=form)


@app.route('/students', methods=['GET', 'POST'])
def students():

    select_result = Students.query.filter_by().all()

    form = StudentsForm()

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('students.html', form=form)
        else:
            student = Students(form.first_name.data, form.last_name.data, form.study_book.data,
                           form.status.data, form.destiny.data, form.group_code.data)
            db.session.add(student)
            db.session.commit()

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