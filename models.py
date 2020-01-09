from app import db
from flask_login import UserMixin

groups_have_subjects_table = db.Table('groups_have_subjects',
                                db.Column('group_name', db.String(50),
                                          db.ForeignKey('group.group_name'), primary_key=True),
                                db.Column('subject_name', db.String(100),
                                          db.ForeignKey('subject.subject_name'), primary_key=True)
                                )

lections_have_labels_table = db.Table('lections_have_labels',
                                      db.Column('lection_name', db.String(500),
                                                db.ForeignKey('lection.lection_name'), primary_key=True),
                                      db.Column('label_name', db.String(100),
                                                db.ForeignKey('label.label_name'), primary_key=True)
                                      )

resources_have_labels_table = db.Table('resources_have_labels',
                                      db.Column('resource_name', db.String(500),
                                                db.ForeignKey('resource.resource_name'), primary_key=True),
                                      db.Column('label_name', db.String(100),
                                                db.ForeignKey('label.label_name'), primary_key=True)
                                      )


class Student(UserMixin, db.Model):
    student_email = db.Column(db.String(200), primary_key=True)
    student_password = db.Column(db.String(500), nullable=False)
    student_name = db.Column(db.String(500), nullable=False)
    group_name = db.Column(db.String(10), db.ForeignKey('group.group_name'), nullable=False)
    variant = db.Column(db.Integer, nullable=False)
    implementations = db.relationship('Implementation', backref='student')
    uploaded_resources = db.relationship('Resource', backref='student')

    def __init__(self, student_email, student_password, student_name, group_name, variant):
        self.student_email = student_email
        self.student_password = student_password
        self.student_name = student_name
        self.group_name = group_name
        self.variant = variant

    def get_id(self):
        return self.student_email


class Group(db.Model):
    group_name = db.Column(db.String(10), primary_key=True)
    students = db.relationship('Student', backref='group')
    subjects = db.relationship('Subject', secondary=groups_have_subjects_table)

    def __init__(self, group_name):
        self.group_name = group_name


class Subject(db.Model):
    subject_name = db.Column(db.String(100), primary_key=True)
    laboratory = db.relationship('Laboratory', backref='subject')
    lections = db.relationship('Lection', backref='subject')
    groups = db.relationship('Group', secondary=groups_have_subjects_table)

    def __init__(self, subject_name):
        self.subject_name = subject_name


class Lection(db.Model):
    lection_name = db.Column(db.String(500), primary_key=True)
    lection_author = db.Column(db.String(500))
    lection_content = db.Column(db.Text, nullable=False)
    subject_name = db.Column(db.String(100), db.ForeignKey('subject.subject_name'), nullable=False)
    resources = db.relationship('Resource', backref='lection')
    labels = db.relationship('Label', secondary=lections_have_labels_table)

    def __init__(self, lection_name, lection_author, lection_content, subject_name):
        self.lection_name = lection_name
        self.lection_author = lection_author
        self.lection_content = lection_content
        self.subject_name = subject_name


class Label(db.Model):
    label_name = db.Column(db.String(100), primary_key=True)
    label_number = db.Column(db.Integer, nullable=False)
    lections = db.relationship('Lection', secondary=lections_have_labels_table)
    resources = db.relationship('Resource', secondary=resources_have_labels_table)

    def __init__(self, label_name, label_number):
        self.label_name = label_name
        self.label_number = label_number


class Resource(db.Model):
    resource_name = db.Column(db.String(500), primary_key=True)
    resource_content = db.Column(db.Text, nullable=False)
    resource_source = db.Column(db.String(500), unique=True)
    rating = db.Column(db.Integer)
    lection_name = db.Column(db.String(500), db.ForeignKey('lection.lection_name'), nullable=False)
    student_email = db.Column(db.String(100), db.ForeignKey('student.student_email'), nullable=False)
    labels = db.relationship('Label', secondary=resources_have_labels_table)

    def __init__(self, resource_name, resource_content, resource_source, rating, lection_name, student_email):
        self.resource_name = resource_name
        self.resource_content = resource_content
        self.resource_source = resource_source
        self.rating = rating
        self.lection_name = lection_name
        self.student_email = student_email


class Test(db.Model):
    test_name = db.Column(db.String(500), primary_key=True)
    variant = db.Column(db.Integer, primary_key=True)
    laboratory_theme = db.Column(db.String(500), primary_key=True)
    input_data = db.Column(db.Text, nullable=False)
    expected_result = db.Column(db.Text, nullable=False)
    output_data = db.Column(db.Text)
    __table_args__ = (db.ForeignKeyConstraint(('variant', 'laboratory_theme'),
                                              ('task.variant', 'task.laboratory_theme')), {})

    def __init__(self, test_name, variant, laboratory_theme, input_data, expected_result, output_data):
        self.test_name = test_name
        self.variant = variant
        self.laboratory_theme = laboratory_theme
        self.input_data = input_data
        self.expected_result = expected_result
        self.output_data = output_data


class Task(db.Model):
    variant = db.Column(db.Integer, primary_key=True)
    laboratory_theme = db.Column(db.String(500), db.ForeignKey('laboratory.laboratory_theme'), primary_key=True)
    laboratory_task = db.Column(db.Text, nullable=False)
    tests = db.relationship('Test', backref='task')

    def __init__(self, variant, laboratory_theme, laboratory_task):
        self.variant = variant
        self.laboratory_theme = laboratory_theme
        self.laboratory_task = laboratory_task


class Laboratory(db.Model):
    laboratory_theme = db.Column(db.String(500), primary_key=True)
    laboratory_number = db.Column(db.Integer, nullable=False)
    laboratory_manual = db.Column(db.Text)
    subject_name = db.Column(db.String(100), db.ForeignKey('subject.subject_name'), nullable=False)
    tasks = db.relationship('Task', backref='laboratory')

    def __init__(self, laboratory_theme, laboratory_number, laboratory_manual, subject_name):
        self.laboratory_theme = laboratory_theme
        self.laboratory_number = laboratory_number
        self.laboratory_manual = laboratory_manual
        self.subject_name = subject_name


class Implementation(db.Model):
    attempt = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(500), db.ForeignKey('student.student_email'), primary_key=True)
    laboratory_theme = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    implementation_content = db.Column(db.Text, nullable=False)
    test_output = db.Column(db.Text)
    operator_sequence = db.Column(db.Text)
    plagiary = db.Column(db.Integer)

    def __init__(self, attempt, student_email, laboratory_theme, status,
                 implementation_content, test_output=None, operator_sequence=None, plagiary=None):
        self.attempt = attempt
        self.student_email = student_email
        self.laboratory_theme = laboratory_theme
        self.status = status
        self.implementation_content = implementation_content
        self.test_output = test_output
        self.operator_sequence = operator_sequence
        self.plagiary = plagiary
