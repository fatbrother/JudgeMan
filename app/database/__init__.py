from .models import ProblemSet, Problem, Account
from .initDB import init
import os
from pathlib import Path

base = Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute()
if not Path(base, 'site.db').is_file():  # JudgeMan/app/site.db
    init()
del(base)

problemSets = ProblemSet()
problems = Problem()
accounts = Account()