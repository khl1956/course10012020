from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://obrgjrhdxuelfg:269e0c279d54c845b22eff49ebb0d5e4c29ddfe006bc0785ab36c4ed140a9c5c@ec2-54-195-252-243.eu-west-1.compute.amazonaws.com:5432/ddab9iht6olobl'
    app.config['SECRET_KEY'] = 'secret'

    db.init_app(app)

    from auth import auth as auth_blueprint
    __package__ = 'coursework.auth'
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    __package__ = 'coursework.main'
    app.register_blueprint(main_blueprint)

    @click.command(name='create-tables')
    @with_appcontext
    def create_tables():
        db.drop_all()
        db.create_all(app=app)

    @click.command(name='populate-tables')
    @with_appcontext
    def populate_tables():
        from populate import populate
        populate()

    app.cli.add_command(create_tables)
    app.cli.add_command(populate_tables)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.hello_world'

    from models import Student, Group, Subject, Lection, Label, Resource, Test, Task, Laboratory, Implementation
    __package__ = 'coursework.models'

    @login_manager.user_loader
    def load_user(id):
        return Student.query.get(id)

    return app

app = create_app()
