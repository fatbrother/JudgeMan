from .models import ProblemSet, Problem, Account
from app import db
from . import initBD

db.create_all()

problemSets = ProblemSet()
problems = Problem()
accounts = Account()

