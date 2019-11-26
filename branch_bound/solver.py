from branch_bound.rcm import RCM
from branch_bound.bnode import BranchNode
from queue import PriorityQueue
from queue import LifoQueue
from copy import deepcopy
from solver_base import SolverBase
from greedy.solver import GreedySolver


class BranchAndBoundSolver(SolverBase):

    def __init__(self, tsp_solver, max_nodes):
        super().__init__(tsp_solver)
        self.node_queue = PriorityQueue(max_nodes)

    def run_algorithm(self):
        
        greedy = GreedySolver(self.get_tsp_solver())
        greedy.solve()

        pass
