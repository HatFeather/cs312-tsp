from rcm import *
from utils import *

class BranchAndBoundSolver:

    def solve(self, solver):
        self.results = {}
        self.solver = solver
        self.scenario = solver._scenario

        rcm = RCM()
        rcm.init_as_original(self.scenario)
        rcm.print("initialized")

        rcm.do_reduction()
        rcm.print("reduced")

