from .models import ProblemSet, Problem, Account
from app import db
from . import initDB

db.create_all()

problemSets = ProblemSet()
problems = Problem()
accounts = Account()

