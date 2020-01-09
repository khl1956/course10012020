
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
import re

from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,MinMaxScaler
from sklearn.compose import ColumnTransformer

from forms.user_form import StudentForm, DisciplineForm, PostForm, DisciplineForm1, StudentForm1, PostForm1, TeacherForm, TeacherForm1, AIForm

import plotly.graph_objs as go
import plotly
import json

import plotly
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/postgres'
ENV = 'prod'
#if ENV == 'dev':
   #app.debug = True
   #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/postgres'


#else:
#    app.debug = False
#    app.config[
#        'SQLALCHEMY_DATABASE_URI'] = 'postgres://begwxbtyhdbniq:107942c1202f0965d273fbb2b60cf1064d76cfd541cc723ff85e5fa139893cdf@ec2-54-235-86-101.compute-1.amazonaws.com:5432/d7dufup6hfpmhn'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class ormStudent_new(db.Model):
    __tablename__ = 'Student_new'
    student_id = db.Column(db.Integer, primary_key=True)
    student_mark = db.Column(db.Integer)
    student_stup = db.Column(db.String)
    student_live = db.Column(db.String(20))
    student_age = db.Column(db.Integer)
    post_type = db.Column(db.String)

    #student_ = db.relationship('ormStudent')


class ormStudent(db.Model):
    __tablename__ = 'Student'

    student_id = db.Column(db.Integer,  primary_key=True)
    student_name = db.Column(db.String(20))
    student_surname = db.Column(db.String(20), nullable=False)
    student_group = db.Column(db.String(20))
    student_mark = db.Column(db.Integer)
    student_stup = db.Column(db.String)
    student_live =  db.Column(db.String(20))
    student_age = db.Column(db.Integer)


    student_ = db.relationship('ormPost')


class ormPost(db.Model):
    __tablename__ = 'Post'
    post_id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String(100) , nullable=False)
    post_text = db.Column(db.String(1000),nullable=False)
    stud_id= db.Column(db.Integer, db.ForeignKey('Student.student_id'), nullable=False)
    disc_id = db.Column(db.Integer, db.ForeignKey('Discipline.disc_id'), nullable=False)

    #student_ = db.relationship('ormStudent')




class ormDiscipline(db.Model):
    __tablename__ = 'Discipline'

    disc_id = db.Column(db.Integer, primary_key=True, nullable=False)
    disc_name = db.Column(db.String(30))
    disc_type = db.Column(db.String(30))
    teacher_fullname = db.Column(db.String(30), db.ForeignKey('Teacher.teacher_fullname'), nullable=False)
    student_ = db.relationship('ormPost')


class ormTeacher(db.Model):
    __tablename__ = 'Teacher'
    disc_id = db.Column(db.Integer)
    teacher_fullname = db.Column(db.String(50), primary_key=True)
    teacher_phone = db.Column(db.String(30))

    student_ = db.relationship('ormDiscipline')


db.create_all()


db.session.query(ormPost).delete()
db.session.query(ormDiscipline).delete()
db.session.query(ormStudent).delete()
db.session.query(ormStudent_new).delete()
db.session.query(ormTeacher).delete()


Student1 = ormStudent(student_id=113001, student_name='Катерина', student_surname='Бучинська', student_group='КМ63', student_mark = 87, student_stup = 'так' , student_live = 'з батьками', student_age = 20)
Student2 = ormStudent(student_id=113002, student_name='Остап', student_surname='Вандьо', student_group='ВЛ52', student_mark = 67, student_stup = 'ні' , student_live = 'знімаю квартиру', student_age = 21)
Student3 = ormStudent(student_id=113003, student_name='Саша', student_surname='Буц', student_group='КМ63', student_mark = 90, student_stup = 'так' , student_live = 'в гуртожитку', student_age = 22)
Student4 = ormStudent(student_id=113004, student_name='Ваня', student_surname='Вовченко', student_group='КВ82', student_mark = 71, student_stup = 'ні' , student_live = 'знімаю квартиру', student_age = 18)
Student5 = ormStudent(student_id=113005, student_name='Оля', student_surname='Мілевська', student_group='ВЛ52', student_mark = 85, student_stup = 'так' , student_live = 'знімаю квартиру', student_age = 19)
Student6 = ormStudent(student_id=113006, student_name='Ігор', student_surname='Рясик', student_group='ВЛ52', student_mark = 83, student_stup = 'так' , student_live = 'знімаю квартиру', student_age = 20)



Discipline1 = ormDiscipline(disc_id=1, disc_name='Математичний аналіз', disc_type='математична', teacher_fullname='Ліскін Вячеслав Олегович')
Discipline2 = ormDiscipline(disc_id=2, disc_name='Лінійна алгебра', disc_type='математична', teacher_fullname='Мальчиков Володимир Вікторович')
Discipline3 = ormDiscipline(disc_id=3, disc_name='Англійська мова', disc_type='гуманітарна', teacher_fullname='Білоніжка Інна Сергіївна')
Discipline4 = ormDiscipline(disc_id=4, disc_name='Украінська мова', disc_type='гуманітарна', teacher_fullname='Степанько Галина Юліанівна')
Discipline5 = ormDiscipline(disc_id=5, disc_name='Бази даних', disc_type='технічна', teacher_fullname='Терещенко Ігор Олександрович')
Discipline6 = ormDiscipline(disc_id=6, disc_name='ООП', disc_type='технічна', teacher_fullname='Громова Вікторія Вікторівна')



Post1 = ormPost(post_id=1, post_type='пропозиція', post_text='хочу більше практики', stud_id=113001, disc_id=1)
Post2 = ormPost(post_id=2, post_type='пропозиція', post_text='дуже мало прктики', stud_id=113002, disc_id=2)
Post3 = ormPost(post_id=3, post_type='скарга', post_text='чому не можна користуватись калькулятором?', stud_id=113003, disc_id=2)
Post4 = ormPost(post_id=4, post_type='скарга', post_text='дисципліна не вписується в загальну програму курсу', stud_id=113004, disc_id=2)
Post5 = ormPost(post_id=5, post_type='скарга', post_text='навіщо???', stud_id=113005, disc_id=4)
Post6 = ormPost(post_id=6, post_type='пропозиція', post_text='хотілось би більше розмовної англійської', stud_id=113006, disc_id=3)



Teacher1 = ormTeacher(teacher_fullname='Ліскін Вячеслав Олегович', teacher_phone='+380676728558', disc_id=1)
Teacher2 = ormTeacher(teacher_fullname='Мальчиков Володимир Вікторович', teacher_phone='+380686758933', disc_id=2)
Teacher3 = ormTeacher(teacher_fullname='Білоніжка Інна Сергіївна', teacher_phone='+380688738933', disc_id=3)
Teacher4 = ormTeacher(teacher_fullname='Громова Вікторія Вікторівна', teacher_phone='+380688768933', disc_id=6)
Teacher5 = ormTeacher(teacher_fullname='Терещенко Ігор Олександрович', teacher_phone='+380688738933', disc_id=5)
Teacher6 = ormTeacher(teacher_fullname='Степанько Галина Юліанівна', teacher_phone='+380688768933', disc_id=4)


Student1.student_.append(Post1)
Student2.student_.append(Post2)
Student3.student_.append(Post3)
Student4.student_.append(Post4)
Student5.student_.append(Post5)
Student6.student_.append(Post6)

Discipline1.student_.append(Post1)
Discipline2.student_.append(Post2)
Discipline2.student_.append(Post3)
Discipline2.student_.append(Post4)
Discipline4.student_.append(Post5)
Discipline4.student_.append(Post6)

Teacher1.student_.append(Discipline1)
Teacher2.student_.append(Discipline2)
Teacher3.student_.append(Discipline3)
Teacher4.student_.append(Discipline6)
Teacher5.student_.append(Discipline5)
Teacher6.student_.append(Discipline4)





db.session.add_all([Student1, Student2, Student3, Student4, Student5, Student6])
db.session.add_all([Post1, Post2, Post3,Post4,Post5,Post6])
db.session.add_all([Discipline1, Discipline2, Discipline2,Discipline3,Discipline4,Discipline5, Discipline6])
db.session.add_all([Teacher1, Teacher2, Teacher3,Teacher4,Teacher5,Teacher6])
db.session.commit()



Sample = db.session.query(ormStudent.student_mark,ormStudent.student_live, ormStudent.student_age, ormStudent.student_stup,ormPost.post_type).outerjoin(ormPost).all()
X = []
y = []
for i in Sample:
    X.append([i.student_mark,i.student_live,i.student_age,i.student_stup])
    y.append(i.post_type)

Coder1 = ColumnTransformer(transformers=[('code1', OneHotEncoder(),[1,3])])
Coder2 = MinMaxScaler(feature_range=(-1,1))

Model = MLPClassifier(hidden_layer_sizes=(5,))

Model = Pipeline(steps=[('code1',Coder1),('code2',Coder2),('neur',Model)])
Model.fit(X,y)





#AIfunc
@app.route('/AIform', methods=['GET', 'POST'])
def AIform_():
    form = AIForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('AIform.html', form=form)

        new_user = [[form.student_mark.data, form.student_live.data, form.student_age.data, form.student_stup.data]]
        y_ = Model.predict(new_user)
        print(y_)
        return render_template('OKO.html', result=y_[0])
    elif request.method == 'GET':
        return render_template('AIform.html', form=form)


#main page
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


#hilday pages
@app.route('/student', methods=['GET'])
def student():

    result = db.session.query(ormStudent).all()
    return render_template('student.html', student = result)

@app.route('/student_f_t', methods=['GET'])
def student2():

    result = db.session.query(ormStudent).all()
    return render_template('student_f_t.html', student = result)


@app.route('/new_student', methods=['GET','POST'])
def new_student():

    form = StudentForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            new_user= ormStudent(
                student_id=form. student_id.data,
                student_name=form.student_name.data,
                student_surname=form.student_surname.data,
                student_group=form.student_group.data,
                student_live=form.student_live.data,
                student_mark=form.student_mark.data,
                student_stup = form.student_stup.data,
                student_age = form.student_age.data
                            )


            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student/<int:x>', methods=['GET','POST'])
def edit_student(x):

    form = StudentForm1()
    user = db.session.query(ormStudent).filter(ormStudent.student_id == x).one()

    if request.method == 'GET':



        # fill form and send to user

        form.student_name.data = user.student_name
        form.student_surname.data = user.student_surname
        form.student_group.data = user.student_group
        form.student_live.data = user.student_live
        form.student_stup.data = user.student_stup
        form.student_mark.data = user.student_mark
        form.student_age.data = user.student_age
        return render_template('student_form1.html', form=form, form_name="Edit student")

    else:

        if form.validate() == False:
            return render_template('student_form1.html', form=form, form_name="Edit student")
        else:
            user.student_name = form.student_name.data
            user.student_surname = form.student_surname.data
            user.student_group = form.student_group.data
            student_live = form.student_live.data
            student_mark = form.student_mark.data
            student_stup = form.student_stup.data
            student_age = form.student_age.data

            db.session.commit()

            return redirect(url_for('student'))

@app.route('/delete_student/<int:x>', methods=['GET'])
def delete_student(x):
    result = db.session.query(ormStudent).filter(ormStudent.student_id == x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('succ.html')

@app.route('/for_students', methods=['GET'])
def no():
    return render_template('for_students.html')

@app.route('/for_teachers', methods=['GET'])
def nono():
    return render_template('for_teachers.html')

@app.route('/student', methods=['GET'])
def no1():
    return render_template('student_for_s.html')

@app.route('/post_for_s', methods=['GET'])
def no2():
    return render_template('post_for_s.html')

@app.route('/discipline_for_s', methods=['GET'])
def no3():
    return render_template('discipline_for_s.html')

@app.route('/discipline_view', methods=['GET'])
def discipline_5():

    result = db.session.query(ormDiscipline).all()

    return render_template('discipline_view.html', discipline = result)

@app.route('/teacher_view', methods=['GET'])
def no5():
    result = db.session.query(ormTeacher).all()
    return render_template('teacher_view.html', teacher = result)

#client
@app.route('/post', methods=['GET'])
def post():

    result = db.session.query(ormPost).all()

    return render_template('post.html', post = result)

@app.route('/post_f_s', methods=['GET'])
def post2():

    result = db.session.query(ormPost).all()

    return render_template('post_f_s.html', post = result)

@app.route('/post_f_t', methods=['GET'])
def post7():

    result = db.session.query(ormPost).all()

    return render_template('post_f_t.html', post = result)


@app.route('/new_post', methods=['GET','POST'])
def new_post():

    form = PostForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('post_form.html', form=form, form_name="New post", action="new_post")
        else:
            new_user = ormPost(
                post_id=form.post_id.data,
                post_type=form.post_type.data,
                post_text=form.post_text.data,
                stud_id=form.stud_id.data,
                disc_id=form.disc_id.data,

                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('post'))

    return render_template('post_form.html', form=form, form_name="New post", action="new_post")

@app.route('/edit_post/<int:x>', methods=['GET','POST'])
def edit_post(x):

    form = PostForm1()

    user = db.session.query(ormPost).filter(ormPost.post_id == x).one()

    if request.method == 'GET':

        #user_id =request.args.get('post_id')


        # fill form and send to user

        form.post_text.data = user.post_text
        form.post_type.data =user.post_type
        form.stud_id.data = user.stud_id
        form.disc_id.data = user.disc_id

        return render_template('post_form1.html', form=form, form_name="Edit post")


    else:

        if form.validate() == False:
            return render_template('post_form1.html', form=form, form_name="Edit post")
        else:

            # find user

            # update fields from form data
            user.post_text = form.post_text.data
            user.post_type = form.post_type.data
            user.stud_id = form.stud_id.data
            user.disc_id = form.disc_id.data

            db.session.commit()

            return redirect(url_for('post'))


@app.route('/delete_post/<int:x>', methods=['GET'])
def delete_post(x):

    #user_id = request.form['post_id']


    result = db.session.query(ormPost).filter(ormPost.post_id ==x).one()

    db.session.delete(result)
    db.session.commit()


    return render_template('succ.html')


#presents pages
@app.route('/discipline', methods=['GET'])
def discipline():

    result = db.session.query(ormDiscipline).all()

    return render_template('discipline.html', discipline = result)


@app.route('/new_discipline', methods=['GET','POST'])
def new_discipline():

    form = DisciplineForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")
        else:
            new_user = ormDiscipline(
                disc_id=form.disc_id.data,
                disc_type=form.disc_type.data,
                disc_name=form.disc_name.data,
                teacher_fullname=form.teacher_fullname.data

                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('discipline'))

    return render_template('discipline_form.html', form=form, form_name="New discipline", action="new_discipline")

@app.route('/edit_discipline/<int:x>', methods=['GET','POST'])
def edit_discipline(x):

    form = DisciplineForm1()

    user = db.session.query(ormDiscipline).filter(ormDiscipline.disc_id == x).one()

    if request.method == 'GET':



        form.disc_name.data = user.disc_name
        form.disc_type.data =user.disc_type
        form.teacher_fullname.data = user.teacher_fullname


        return render_template('discipline_form1.html', form=form, form_name="Edit disc")


    else:

        if form.validate() == False:
            return render_template('discipline_form1.html', form=form, form_name="Edit disc")
        else:

            # find user

            # update fields from form data
            user.disc_name = form.disc_name.data
            user.disc_type = form.disc_type.data


            db.session.commit()

            return redirect(url_for('discipline'))


@app.route('/delete_discipline/<int:x>', methods=['GET'])
def delete_discipline(x):

    result = db.session.query(ormDiscipline).filter(ormDiscipline.disc_id == x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('succ.html')
#
@app.route('/teacher', methods=['GET'])
def teacher():

    result = db.session.query(ormTeacher).all()
    return render_template('teacher.html', teacher = result)


@app.route('/new_teacher', methods=['GET','POST'])
def new_teacher():

    form = TeacherForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")
        else:
            new_user = ormDiscipline(
                teacher_fullname=form.teacher_fullname.data,
                teacher_phone=form.teacher_phone.data,
                disc_id=form.disc_id.data,

                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('teacher'))

    return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")

@app.route('/edit_teacher/<string:x>', methods=['GET','POST'])
def edit_teacher(x):

    form = TeacherForm1()
    user = db.session.query(ormTeacher).filter(ormTeacher.teacher_fullname == x).one()

    if request.method == 'GET':



        # fill form and send to user

        form.teacher_phone.data = user.teacher_phone
        form.disc_id.data = user.disc_id
        return render_template('teacher_form1.html', form=form, form_name="Edit teacher")

    else:

        if form.validate() == False:
            return render_template('teacher_form1.html', form=form, form_name="Edit teacher")
        else:
            user.teacher_phone = form.teacher_phone.data
            user.disc_id = form.disc_id.data

            db.session.commit()

            return redirect(url_for('teacher'))

@app.route('/delete_teacher/<string:x>', methods=['GET'])
def delete_teacher(x):
    result = db.session.query(ormTeacher).filter(ormTeacher.teacher_fullname == x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('succ.html')



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    query1 = (
        db.session.query(
            ormDiscipline.disc_type,
            func.count(ormPost.post_id).label('post')
        ).
            outerjoin(ormPost).
            group_by(ormDiscipline.disc_type)
    ).all()

    query2 = (
        db.session.query(
            ormStudent.student_group,
            func.count(ormPost.post_id).label('...')
        ).
            outerjoin(ormPost).
            group_by(ormStudent.student_group)
    ).all()


    names, skill_counts = zip(*query1)
    bar = go.Bar(
        x=names,
        y=skill_counts
    )

    skills, user_count = zip(*query2)
    pie = go.Pie(
        labels=skills,
        values=user_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]

    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', graphsJSON=graphsJSON)

if __name__ == '__main__':
    app.run(debug=True)