from app import db, app
import json

class ProblemSet(db.Model):
    __tablename__ = "problem"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    problems = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Problem('{self.title}', '{self.problems}')"

    def insert(self, id:int, title: str, problems: list):
        problemsId = json.dumps(problems)
        problem = ProblemSet(id=id, title=title, problems=problemsId)
        db.session.add(problem)
        db.session.commit()
    
    def update(self, id:int, title: str = None, problems: list = None):
        problemsId = json.dumps(problems)
        problem = ProblemSet.query.filter_by(id=id).first()
        if title != None:    problem.title = title
        if problems != None: problem.problems = problemsId
        db.session.commit()
    
    def viewAll(self):
        problems = ProblemSet.query.all()
        return problems

    def query(self, id:int):
        problem = ProblemSet.query.filter_by(id=id).first()
        return problem
    
    def delete(self, id:int):
        problem = ProblemSet.query.filter_by(id=id).first()
        db.session.delete(problem)
        db.session.commit()