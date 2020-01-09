from flask import Blueprint, request, flash, url_for, redirect
from app import db
from flask_login import login_user, logout_user
from models import Student


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    student = Student.query.filter_by(student_email=email).first()

    if not student or password != student.student_password:
        flash('Please check your login details and try again.')

        return redirect(url_for('main.hello_world'))
    login_user(student)
    return redirect(url_for('main.dashboard'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.hello_world'))
