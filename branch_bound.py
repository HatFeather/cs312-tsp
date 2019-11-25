from rcm import *
from utils import *

class BranchAndBoundSolver:

    def solve(self, solver):
        self.results = {}
        self.solver = solver
        self.scenario = solver._scenario

