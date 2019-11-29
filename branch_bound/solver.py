from branch_bound.rcm import RCM
from branch_bound.bnode import BranchNode
from queue import PriorityQueue
from queue import LifoQueue
from copy import deepcopy
from solver_base import SolverBase
from greedy.solver import GreedySolver
from random import randrange
import math


class BranchAndBoundSolver(SolverBase):

    def __init__(self, tsp_solver, max_nodes, max_time):
        super().__init__(tsp_solver, max_time)

        self._node_queue = PriorityQueue(max_nodes)
        self.set_max(max_nodes)

    def run_algorithm(self):

        self._do_greedy()
        if self.exceeded_max_time():
            return

        start_index = randrange(self.get_city_count())
        start_city = self.get_city_at(start_index)
        start_rcm = RCM(self.get_scenario())
        start_rcm.do_reduction()

        root = BranchNode(start_rcm, start_city, start_index, None)
        self._node_queue.put((self._get_node_key(root), root))
        self.increment_total()

        while not self._node_queue.empty() and not self.exceeded_max_time():

            current = self._node_queue.get()[1]

            # prune pointless paths as we go
            best_cost = math.inf if self.get_bssf() == None else self.get_bssf().cost
            if current.get_cost() >= best_cost:
                self.increment_pruned()
                continue

            # try the solution if we've traversed all cities
            if current.get_depth() == self.get_city_count():
                self.increment_solution_try_count()
                loop_cost = current.get_city().costTo(start_city)
                if loop_cost == math.inf:
                    continue
                elif loop_cost < best_cost:
                    route = current.get_path()
                    self.set_bssf_from_route(route)
                    print('sol (t: {0:.3f})'.format(self.get_clamped_time()))

            # continue branching
            current.generate_child_nodes(self.get_cities())
            self.increment_total(current.get_child_count())
            for child in current.get_children():
                if not self._node_queue.full():
                    self._node_queue.put((self._get_node_key(child), child))
                else:
                    self.increment_pruned()
                    break

        print('fin (t: {0:.3f})'.format(self.get_clamped_time()))
        self.increment_pruned(self._node_queue.qsize())

    def _get_node_key(self, bnode):
        return bnode.get_cost() / bnode.get_depth()

    def _do_greedy(self):
        greedy = GreedySolver(self.get_tsp_solver(), self.get_max_time())
        greedy.solve()
        self.set_bssf(greedy.get_bssf())
