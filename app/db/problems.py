from app import app, db

class Problems(db.Model):
    __tablename__ = "problem"
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
        problem = Problems(title=title, taskDescription=taskDescription, inputFormat=inputFormat, outputFormat=outputFormat, sampleInput=sampleInput, sampleOutput=sampleOutput, testCaseNumber=testCaseNumber, AC=AC, WA=WA)
        db.session.add(problem)
        db.session.commit()

    def update(self, id:int, title: str = None, taskDescription: str = None, inputFormat: str = None, outputFormat: str = None, sampleInput: str = None, sampleOutput: str = None, testCaseNumber: int = None, AC: int = None, WA: int = None):
        problem = Problems.query.filter_by(id=id).first()
        if title != None:           problem.title = title
        if taskDescription != None: problem.taskDescription = taskDescription
        if inputFormat != None:     problem.inputFormat = inputFormat
        if outputFormat != None:    problem.outputFormat = outputFormat
        if sampleInput != None:     problem.sampleInput = sampleInput
        if sampleOutput != None:    problem.sampleOutput = sampleOutput
        if testCaseNumber != None:  problem.testCaseNumber = testCaseNumber
        if AC != None:              problem.AC = AC
        if WA != None:              problem.WA = WA
        db.session.commit()
    
    def viewAll(self):
        problems = Problems.query.all()
        return problems
    
    def query(self, id:int):
        problem = Problems.query.filter_by(id=id).first()
        return problem
    
    def delete(self, id:int):
        problem = Problems.query.filter_by(id=id).first()
        db.session.delete(problem)
        db.session.commit()