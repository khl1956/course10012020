from flask import Blueprint, render_template, redirect, url_for, request
from forms import AuthForm, SolveLaboratoryForm, AddResourceForm
from flask_login import login_required, current_user
from models import Subject, Group, Lection, Implementation, Laboratory, Task, Resource
from app import db

main = Blueprint('main', __name__)


@main.route('/')
def hello_world():
    auth_form = AuthForm()
    return render_template('main.html', form=auth_form, user=current_user)


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user, implementations=current_user.implementations)


@main.route('/subjects')
@login_required
def subjects():
    all_subjects = Subject.query.all()
    group = Group.query.filter_by(group_name=current_user.group_name).first()
    return render_template('subjects.html', user=current_user, all_subjects=all_subjects, user_subjects=group.subjects)


@main.route('/subject/<name>')
@login_required
def subject(name):
    form = AddResourceForm()
    lectures = Lection.query.filter_by(subject_name=name).all()
    form.lection_name.choices = [(lecture.lection_name, lecture.lection_name) for lecture in lectures]
    group = Group.query.filter_by(group_name=current_user.group_name).first()
    group_subject_names = list(map(lambda subject: subject.subject_name, group.subjects))
    return render_template('subject.html', subject_name=name, lectures=lectures, user_subjects=group_subject_names, form=form)


@main.route('/subject/<name>/laboratory')
@login_required
def laboratory(name):
    subject_model = Subject.query.filter_by(subject_name=name).first()
    if current_user.group_name not in list(map(lambda group: group.group_name, subject_model.groups)):
        return redirect('/subject/{}'.format(name))
    return render_template('laboratory.html', user=current_user, laboratory=subject_model.laboratory, subject_name=name)


@main.route('/subject/<name>/laboratory/<num>')
@login_required
def separate_laboratory(name, num):
    form = SolveLaboratoryForm()
    subject_model = Subject.query.filter_by(subject_name=name).first()
    if current_user.group_name not in list(map(lambda group: group.group_name, subject_model.groups)):
        return redirect('/subject/{}'.format(name))
    lab = Laboratory.query.filter_by(subject_name=subject_model.subject_name, laboratory_number=num).first()
    existed_implementations = Implementation.query.filter_by(student_email=current_user.student_email, laboratory_theme=lab.laboratory_theme).all()
    user_task = Task.query.filter_by(laboratory_theme=lab.laboratory_theme, variant=current_user.variant).first()
    return render_template('separate_laboratory.html', user=current_user, laboratory=lab, subject_name=name,
                           implementations=existed_implementations, task=user_task, form=form)


@main.route('/implementation/add', methods=['POST'])
def add_implementation():
    form = SolveLaboratoryForm()
    new_implementation = Implementation(form.attempt.data, current_user.student_email,
                                        form.laboratory_theme.data, 'In queue', form.implementation_content.data)
    db.session.add(new_implementation)
    db.session.commit()
    current_laboratory = Laboratory.query.filter_by(laboratory_theme=form.laboratory_theme.data).first()
    return redirect(url_for('main.separate_laboratory', name=current_laboratory.subject_name,
                            num=current_laboratory.laboratory_number))


@main.route('/resource/add', methods=['POST'])
def add_resource():
    form = AddResourceForm()
    new_resource = Resource(form.resource_name.data, form.resource_content.data,
                            form.resource_source.data, 0, form.lection_name.data, current_user.student_email)
    db.session.add(new_resource)
    db.session.commit()
    return redirect(url_for('main.my_resources'))


@main.route('/resource/delete', methods=['POST'])
def remove_resource():
    resource_name = request.form.get('resource_name')
    resource = Resource.query.filter_by(resource_name=resource_name).first()
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for('main.my_resources'))


@main.route('/resource/update', methods=['POST'])
def update_resource():
    form = AddResourceForm()
    current_resource = Resource.query.filter_by(resource_name=form.resource_name.data).first()
    current_resource.resource_content = form.resource_content.data
    current_resource.resource_source = form.resource_source.data
    current_resource.lection_name = form.lection_name.data
    db.session.commit()
    return redirect(url_for('main.my_resources'))


@main.route('/my_resources')
@login_required
def my_resources():
    form = AddResourceForm()
    lectures = Lection.query.all()
    form.lection_name.choices = [(lecture.lection_name, lecture.lection_name) for lecture in lectures]
    resources = current_user.uploaded_resources
    return render_template('my_resources.html', form=form, resources=resources)
