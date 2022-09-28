from app import db, bcrypt
import json

class Problem(db.Model):
    __tablename__ = "Problem"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    inputFormat = db.Column(db.String(500), nullable=False)
    outputFormat = db.Column(db.String(500), nullable=False)
    sampleInput = db.Column(db.String(500), nullable=False)
    sampleOutput = db.Column(db.String(500), nullable=False)
    hint = db.Column(db.String(500), nullable=False)
    testCasePaths = db.Column(db.String(500), nullable=False)
    answerCasePaths = db.Column(db.String(500), nullable=False)
    AC = db.Column(db.Integer, nullable=False)
    WA = db.Column(db.Integer, nullable=False)    

    def __repr__(self):
        return f"Problem('{self.title}', '{self.description}', '{self.inputFormat}', '{self.outputFormat}', '{self.sampleInput}', '{self.sampleOutput}', '{self.testCasePaths}', '{self.answerCasePaths}', '{self.AC}', '{self.WA}')"

    def insert(self, id: int, title: str, description: str, inputFormat: str, outputFormat: str, sampleInput: list, sampleOutput: list, hint: str, testCasePaths: list, answerCasePaths: list, AC: int, WA: int):
        sampleInputInJson = json.dumps(sampleInput)
        sampleOutputInJson = json.dumps(sampleOutput)
        testCasePathsInJson = json.dumps(testCasePaths)
        answerCasePathsInJson = json.dumps(answerCasePaths)

        problem = Problem(id=id, title=title, description=description, inputFormat=inputFormat, outputFormat=outputFormat,
                           sampleInput=sampleInputInJson, sampleOutput=sampleOutputInJson, hint=hint, testCasePaths=testCasePathsInJson, answerCasePaths=answerCasePathsInJson, AC=AC, WA=WA)
        db.session.add(problem)
        db.session.commit()

    def update(self, id: int, title: str = None, description: str = None, inputFormat: str = None, outputFormat: str = None, sampleInput: str = None, sampleOutput: str = None, testCasePaths: list = [], answerCasePaths: list = [], AC: int = None, WA: int = None):
        problem = Problem.query.filter_by(id=id).first()
        if title != None:
            problem.title = title
        if description != None:
            problem.description = description
        if inputFormat != None:
            problem.inputFormat = inputFormat
        if outputFormat != None:
            problem.outputFormat = outputFormat
        if sampleInput != None:
            problem.sampleInput = json.dumps(sampleInput)
        if sampleOutput != None:
            problem.sampleOutput = json.dumps(sampleOutput)
        if testCasePaths != []:
            problem.testCasePaths = json.dumps(testCasePaths)
        if answerCasePaths != []:
            problem.answerCasePaths = json.dumps(answerCasePaths)
        if AC != None:
            problem.AC = AC
        if WA != None:
            problem.WA = WA
        db.session.commit()

    def viewAll(self):
        problems = Problem.query.all()
        return problems

    def search(self, id: int):
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

    def search(self, id: int):
        problem = ProblemSet.query.filter_by(id=id).first()
        return problem

    def delete(self, id: int):
        problem = ProblemSet.query.filter_by(id=id).first()
        db.session.delete(problem)
        db.session.commit()


class Account(db.Model):
    __tablename__ = "Account"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=True)
    email = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    level = db.Column(db.String(20), nullable=True)
    passProblems = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"Account('{self.username}', '{self.level}', '{self.email}', '{self.password}', '{self.passProblems}')"

    def insert(self, username: str, email: str, password: str, level: str = 'User', problems: list = []):
        id = len(Account.query.all()) + 1
        passProblems = json.dumps(problems)
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
        user = Account(id=id, username=username, level=level, email=email, password=hashedPassword, passProblems=passProblems)
        db.session.add(user)
        db.session.commit()

    def update(self, id: int, username: str = None, level: str = None, email: str = None, password: str = None, problems: list = None):
        user = Account.query.filter_by(id=id).first()
        if username != None:
            user.username = username
        if level != None:
            user.level = level
        if email != None:
            user.email = email
        if password != None:
            hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashedPassword
        if problems != None:
            passProblems = json.dumps(problems)
            user.passProblems = passProblems
        db.session.commit()

    def viewAll(self):
        users = Account.query.all()
        return users

    def searchById(self, id: int):
        user = Account.query.filter_by(id=id).first()
        return user

    def searchByEmail(self, email: str):
        user = Account.query.filter_by(email=email).first()
        return user
    
    def searchByUsername(self, username: str):
        user = Account.query.filter_by(username=username).first()
        return user

    def delete(self, username: str):
        user = Account.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
