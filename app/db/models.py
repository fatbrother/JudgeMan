from flask_sqlalchemy import SQLAlchemy
from app import db
import json

class Problem(db.Model):
    __tablename__ = "Problem"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    taskDescription = db.Column(db.String(500), nullable=False)
    inputFormat = db.Column(db.String(500), nullable=False)
    outputFormat = db.Column(db.String(500), nullable=False)
    sampleInput = db.Column(db.String(500), nullable=False)
    sampleOutput = db.Column(db.String(500), nullable=False)
    testCaseNumber = db.Column(db.Integer, nullable=False)
    AC = db.Column(db.Integer, nullable=False)
    WA = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Problem('{self.title}', '{self.taskDescription}', '{self.inputFormat}', '{self.outputFormat}', '{self.sampleInput}', '{self.sampleOutput}', '{self.testCaseNumber}', '{self.AC}', '{self.WA}')"

    def insert(self, title: str, taskDescription: str, inputFormat: str, outputFormat: str, sampleInput: str, sampleOutput: str, testCaseNumber: int, AC: int, WA: int):
        problem = Problem(title=title, taskDescription=taskDescription, inputFormat=inputFormat, outputFormat=outputFormat,
                           sampleInput=sampleInput, sampleOutput=sampleOutput, testCaseNumber=testCaseNumber, AC=AC, WA=WA)
        db.session.add(problem)
        db.session.commit()

    def update(self, id: int, title: str = None, taskDescription: str = None, inputFormat: str = None, outputFormat: str = None, sampleInput: str = None, sampleOutput: str = None, testCaseNumber: int = None, AC: int = None, WA: int = None):
        problem = Problem.query.filter_by(id=id).first()
        if title != None:
            problem.title = title
        if taskDescription != None:
            problem.taskDescription = taskDescription
        if inputFormat != None:
            problem.inputFormat = inputFormat
        if outputFormat != None:
            problem.outputFormat = outputFormat
        if sampleInput != None:
            problem.sampleInput = sampleInput
        if sampleOutput != None:
            problem.sampleOutput = sampleOutput
        if testCaseNumber != None:
            problem.testCaseNumber = testCaseNumber
        if AC != None:
            problem.AC = AC
        if WA != None:
            problem.WA = WA
        db.session.commit()

    def viewAll(self):
        problems = Problem.query.all()
        return problems

    def query(self, id: int):
        problem = Problem.query.filter_by(id=id).first()
        return problem

    def delete(self, id: int):
        problem = Problem.query.filter_by(id=id).first()
        db.session.delete(problem)
        db.session.commit()


class ProblemSet(db.Model):
    __tablename__ = "ProblemSet"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    problems = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Problem('{self.title}', '{self.problems}')"

    def insert(self, id: int, title: str, problems: list):
        problemsId = json.dumps(problems)
        problem = ProblemSet(id=id, title=title, problems=problemsId)
        db.session.add(problem)
        db.session.commit()

    def update(self, id: int, title: str = None, problems: list = None):
        problemsId = json.dumps(problems)
        problem = ProblemSet.query.filter_by(id=id).first()
        if title != None:
            problem.title = title
        if problems != None:
            problem.problems = problemsId
        db.session.commit()

    def viewAll(self):
        problems = ProblemSet.query.all()
        return problems

    def query(self, id: int):
        problem = ProblemSet.query.filter_by(id=id).first()
        return problem

    def delete(self, id: int):
        problem = ProblemSet.query.filter_by(id=id).first()
        db.session.delete(problem)
        db.session.commit()


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    level = db.Column(db.String(20), nullable=True)
    passProblems = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.level}', '{self.email}', '{self.password}', '{self.passProblems}')"

    def insert(self, username: str, email: str, password: str, level: str = 'User', problems: list = None):
        passProblems = json.dumps(problems)
        user = User(username=username, level=level, email=email, password=password, passProblems=passProblems)
        db.session.add(user)
        db.session.commit()

    def update(self, username: str, level: str = None, email: str = None, password: str = None, problems: list = None):
        passProblems = json.dumps(problems)
        user = User.query.filter_by(username=username).first()
        if level != None:
            user.level = level
        if email != None:
            user.email = email
        if password != None:
            user.password = password
        if problems != None:
            user.passProblems = passProblems
        db.session.commit()

    def viewAll(self):
        users = User.query.all()
        return users

    def query(self, username: str):
        user = User.query.filter_by(username=username).first()
        return user

    def delete(self, username: str):
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
