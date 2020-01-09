from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, ForeignKeyConstraint, update, func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_login = Column(String(255), nullable=False)
    user_url = Column(String(255), nullable=False)

    user_lectures = relationship("Lecture")

class Subject(Base):
    __tablename__ = 'Subjects'

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(255), nullable=False)
    subject_description = Column(String(255), nullable=False)


class Lecture(Base):
    __tablename__ = 'Lectures'

    lecture_id = Column(Integer, primary_key = True, autoincrement=True)
    lecture_name = Column(String(255), nullable=False)
    gitgist_id = Column(String(255), nullable=False)
    user_id_fk = Column(Integer, ForeignKey('Users.user_id'))
    subject_id_fk = Column(Integer, ForeignKey('Subjects.subject_id'))

