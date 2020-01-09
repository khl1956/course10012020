from models import Student, Group, Subject, Lection, Label, Resource, Test, Task, Laboratory, Implementation
from app import db


def populate():
    python = Subject('Python')
    web = Subject('Web')
    oop = Subject('OOP')
    art = Subject('Art')

    db.session.add(python)
    db.session.add(web)
    db.session.add(oop)
    db.session.add(art)

    km61 = Group('KM-61')
    km62 = Group('KM-62')
    km63 = Group('LA-73')

    km62.subjects.append(web)
    km62.subjects.append(oop)
    km62.subjects.append(python)

    km63.subjects.append(art)

    db.session.add(km61)
    db.session.add(km62)
    db.session.add(km63)

    richmound = Student('rtizard1@arstechnica.com', '123456', 'Richmound Tizard', 'KM-62', 1)
    torrie = Student('tchinge2@gov.uk', '123456', 'Torrie Chinge', 'KM-62', 2)
    becca = Student('bparell3@yandex.ru', '123456', 'Becca Parell', 'LA-73', 3)

    db.session.add(richmound)
    db.session.add(torrie)
    db.session.add(becca)

    python_intro = Lection('Introduction to python', 'Den Mitchel', 'Introduction to python blah blah blah', 'Python')
    js_intro = Lection('Introduction to JS', 'Dan Abramov', 'Introduction to JS blah blah blah', 'Web')
    js_object = Lection('Objects in JS', 'Dan Abramov', 'Objects in JS blah blah blah', 'Web')

    db.session.add(python_intro)
    db.session.add(js_intro)
    db.session.add(js_object)

    python_beginner = Label('Python language for beginners', 0)
    js_beginner = Label('JS for beginners', 1)
    js_intermediate = Label('JS for intermediate', 2)

    db.session.add(python_beginner)
    db.session.add(js_beginner)
    db.session.add(js_intermediate)

    python_docs = Resource('Official doc for python', 'lalala', 'https://docs.python.org/3/', 0, 'Introduction to python', 'rtizard1@arstechnica.com')
    js_docs = Resource('Official doc for JS', 'lalala JS', 'https://developer.mozilla.org/ru/docs/Web/JavaScript', 0, 'Introduction to JS', 'rtizard1@arstechnica.com')
    abramov_blog = Resource('Dan`s Abramov blog', 'lalala blog', 'https://overreacted.io/', 0, 'Objects in JS', 'rtizard1@arstechnica.com')

    db.session.add(python_docs)
    db.session.add(js_docs)
    db.session.add(abramov_blog)

    js_lab_1 = Laboratory('Arithmetical operations in JS', 1, 'Manual is here', 'Web')
    js_lab_2 = Laboratory('Conditions in JS', 2, 'Manual is here', 'Web')
    js_lab_3 = Laboratory('Loops in JS', 3, 'Manual is here', 'Web')

    db.session.add(js_lab_1)
    db.session.add(js_lab_2)
    db.session.add(js_lab_3)

    js_lab_1_v1 = Task(1, 'Arithmetical operations in JS', 'Please, add two numbers')
    js_lab_1_v2 = Task(2, 'Arithmetical operations in JS', 'Please, multiple two numbers')
    js_lab_1_v3 = Task(3, 'Arithmetical operations in JS', 'Please, divide two numbers')

    db.session.add(js_lab_1_v1)
    db.session.add(js_lab_1_v2)
    db.session.add(js_lab_1_v3)

    richmound_attempt_1 = Implementation(1, 'rtizard1@arstechnica.com',
                                         'Arithmetical operations in JS', 'Tests passed', 'code',
                                         'Data validation failed!', 'IFFOIIFOFDFIO', 20)
    richmound_attempt_2 = Implementation(2, 'rtizard1@arstechnica.com',
                                         'Arithmetical operations in JS', 'Tests passed', 'code',
                                         'Stack overflow!', 'IFFOIIFFFIO', 36)
    richmound_attempt_3 = Implementation(3, 'rtizard1@arstechnica.com',
                                         'Arithmetical operations in JS', 'Tests passed', 'code',
                                         'Success!', 'IOIIIIIFOFDFIO', 15)

    db.session.add(richmound_attempt_1)
    db.session.add(richmound_attempt_2)
    db.session.add(richmound_attempt_3)

    first_lab_test_1 = Test('Check functionality', 1, 'Arithmetical operations in JS', '{a: 2, b: 2}',
                            '{return: 4}', 'Arithmetical error!')
    first_lab_test_2 = Test('Check validation', 1, 'Arithmetical operations in JS', '{a: "c", b: 2}',
                            '{return: "Not a number"}', 'Data validation failed!')

    first_lab_test_3 = Test('Check small numbers', 1, 'Arithmetical operations in JS', '{a: 0.333333333, b: 0.2222222222}',
                            '{return: 0.555555555}', 'Data validation failed!')

    db.session.add(first_lab_test_1)
    db.session.add(first_lab_test_2)
    db.session.add(first_lab_test_3)
    db.session.commit()