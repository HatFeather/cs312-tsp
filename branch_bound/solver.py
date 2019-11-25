from branch_bound.rcm import RCM
# from branch_bound.pqueue import PriorityQueue
from branch_bound.bnode import BranchNode
from queue import PriorityQueue
from copy import deepcopy

class BranchAndBoundSolver:

    def solve(self, solver):
        self.results = {}
        self.solver = solver
        self.scenario = solver._scenario

        rcm0 = RCM(self.scenario)
        rcm0.print()
        # rcm1 = RCM(self.scenario)
        # rcm2 = RCM(self.scenario)

        # rcm0.cost = 0
        # rcm1.cost = 1
        # rcm2.cost = 2



        # node0 = BranchNode(rcm0, [], 2)
        # node1 = BranchNode(rcm1, [], 1)
        # node2 = BranchNode(rcm2, [], 0)

        # queue = PriorityQueue(3)
        # queue.print("Initialized")

        # queue.insert(node0)
        # queue.print("Insert node 0")

        # queue.insert(node1)
        # queue.print("Insert node 1")

        # rcm = RCM()
        # rcm.init_as_original(self.scenario)
        # cpy = deepcopy(rcm)

        # rcm.do_reduction()
        # rcm.do_selection(0, 1)
        # rcm.do_reduction()

        # cpy.do_reduction()
        # cpy.do_selection(0, 3)
        # cpy.do_reduction()

        # rcm.print()
        # cpy.print()
