from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, LargeBinary
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_no = Column(String(100), nullable=False)
    employee_name = Column(String(100), nullable=False)
    emailid = Column(String(100), nullable=False)
    manager_id = Column(Integer, nullable=True)
    team_id = Column(Integer, nullable=False)
    grade_id = Column(Integer, nullable=True)
    discontinued = Column(Boolean, default=False, nullable=False)
    password = Column(String(100), nullable=True)
    training_team = Column(Boolean, default=False, nullable=False)

    registrations = relationship("TrainingRegistration", back_populates="employee")
    answers = relationship("Answer", back_populates="employee")


class Training(Base):
    __tablename__ = 'trainings'

    training_id = Column(Integer, primary_key=True, autoincrement=True)
    trainer = Column(String(50), nullable=False)
    topic = Column(String(255), nullable=False)
    training_datetime = Column(DateTime, nullable=False)
    traing_logo_bs64 = Column(LargeBinary, nullable=True)  # Accepts image bytes
    description = Column(Text, nullable=True)
    training_completed = Column(Boolean, default=False, nullable=True)
    training_reschule_reason = Column(String(1000), nullable=True)  # Renamed
    exam_inprogress = Column(Boolean, default=False, nullable=False)  # Changed from string to boolean

    registrations = relationship("TrainingRegistration", back_populates="training")
    tests = relationship("TrainingTest", back_populates="training")


class TrainingRegistration(Base):
    __tablename__ = 'training_registration'

    registration_id = Column(Integer, primary_key=True, autoincrement=True)
    training_id = Column(Integer, ForeignKey('trainings.training_id'), nullable=True)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=True)
    manager_id = Column(Integer, nullable=True)
    training_request = Column(Boolean, nullable=True)
    approval = Column(Boolean, nullable=True)
    registration_datetime = Column(DateTime, nullable=False)
    reject_reason = Column(String(100), nullable=True)

    training = relationship("Training", back_populates="registrations")
    employee = relationship("Employee", back_populates="registrations")


class TrainingTest(Base):
    __tablename__ = 'training_test'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    training_id = Column(Integer, ForeignKey('trainings.training_id'), nullable=True)
    question = Column(Text, nullable=False)
    option1 = Column(String(255), nullable=False)
    option2 = Column(String(255), nullable=False)
    option3 = Column(String(255), nullable=False)
    option4 = Column(String(255), nullable=False)
    answer = Column(String(255), nullable=False)

    training = relationship("Training", back_populates="tests")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = 'answers'

    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('training_test.question_id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=False)
    answer = Column(String(255), nullable=True)

    question = relationship("TrainingTest", back_populates="answers")
    employee = relationship("Employee", back_populates="answers")
