from .models import ProblemSet, Problem, Account
from .initDB import init
import os
from pathlib import Path

base = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.absolute())
if not os.path.exists(base+'\site.db'):
    init()
del(base)

problemSets = ProblemSet()
problems = Problem()
accounts = Account()