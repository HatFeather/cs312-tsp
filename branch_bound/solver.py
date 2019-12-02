from branch_bound.rcm import RCM
from branch_bound.bnode import BranchNode
from queue import PriorityQueue
from copy import deepcopy
from solver_base import SolverBase
from greedy.solver import GreedySolver
from random import randrange
import math


# NOTE: for all code below, let |V| be the number of cities
# NOTE: also let MAX_NODES be the max number of nodes in the priority queue
class BranchAndBoundSolver(SolverBase):

    def __init__(self, tsp_solver, max_nodes, max_time):
        '''
        initializes the base solver as well as creates a priority queue
        with max nodes
        \ntime:     initialize an empty queue --> O(1)
        \nspace:    the queue is initialially empty, but is capped at max nodes --> O(1)
        '''

        super().__init__(tsp_solver, max_time)

        # cap the number of nodes allowed in the priority queue to MAX_NODES
        # NOTE: the priority queue is implemented as a binary tree
        # with O(log(MAX_NODES)) as the upper bound insertion and removal time
        self._node_queue = PriorityQueue(max_nodes)
        self.set_max_concurrent_nodes(0)
        self.try_update_max_concurrent_nodes(self._node_queue.qsize())

    def run_algorithm(self):
        '''
        runs the branch and bound algorithm for the TSP by creating an pruning
        routes as it goes, in an effort to find the most optimal solution
        \ntime:     consider to following:
                    1) the initial greedy solver takes O(|V|^3) time to compute;
                    2) each branch node has (|V| - #-of-cities-already-traversed)
                       sub-problems (branch nodes), each costing O(|V|^2) to produce;
                    3) each branch node requires and upper bound of O(log(queue_size) 
                       to be queued/dequeued; 
                    4) computing a path from a branch node only happens if children aren't
                       generated, thus this cost can be ignored;
                    5) the tree generated is, worst case, n levels deep and each node braches
                       into |V| - depth other nodes
                    `total complexity --> O(|V|! * |V|^2 * log(queue_size))` capped at max_time and 
        \nspace:    with at most queue_size in the queue, each node takes O(|V|^2)
                    space --> O(queue_size * |V|^2)
        '''

        # O(|V|^3) time and O(|V|) space call to greedily compute the initial bssf
        greedy = GreedySolver(self.get_tsp_solver(), self.get_max_time())
        greedy.solve()
        self.set_bssf(greedy.get_bssf())
        if self.exceeded_max_time():
            return

        # pick the initial city and initialize the root RCM based on that city
        start_index = randrange(self.get_city_count())
        start_city = self.get_city_at(start_index)
        start_rcm = RCM(self.get_scenario())
        start_rcm.do_reduction()

        # construct the root branch node from the start city with its associated RCM
        # (the first state created for this branch and bound problem)
        root = BranchNode(start_rcm, start_city, start_index, None)
        self.increment_total()
        if root.get_cost() < self.get_best_cost():
            self._node_queue.put((self._get_node_key(root), root))
            self.try_update_max_concurrent_nodes(self._node_queue.qsize())

        # loop while there are still paths to process and theres still time
        while not self._node_queue.empty() and not self.exceeded_max_time():

            # binary heap removal: upper bound O(log(MAX_NODES)) to remove from the queue
            current = self._node_queue.get()[1]

            # prune paths that exceed the bssf as we go
            if current.get_cost() >= self.get_best_cost():
                self.increment_pruned()
                continue

            # if we've traversed all cities, try to connect the route to its start node
            # (indicating that we're considering a solution)
            if current.get_depth() == self.get_city_count():

                # O(1) check to see if the this route fails
                loop_cost = current.get_city().costTo(start_city)
                if loop_cost == math.inf or loop_cost >= self.get_best_cost():
                    continue

                # the current route is more optimal, choose it
                route = current.compute_path()      # O(|V|) time and space
                self.set_bssf_from_route(route)     # assumed constant time and space
                self.increment_solution_count()     # O(1)
                print('sol (t: {0:.3f})'.format(self.get_clamped_time()))
                continue

            # continue branching: create nodes for the currently selected node (popped
            # off of the priority queue) --> O(|V|^2) time and space for each child generated 
            current.generate_child_nodes(self.get_cities())
            self.increment_total(current.get_child_count())

            # loop through all children nodes --> O(|V|)
            for child in current.get_children():
                # try to push the child onto the queue --> upper bound O(log(MAX_NODES))
                if not self._node_queue.full() and child.get_cost() < self.get_best_cost():
                    self._node_queue.put((self._get_node_key(child), child))
                else:
                    self.increment_pruned()

            # some nodes were inserted into the queue, try toupdate the max nodes
            # stored at a given time --> O(1)
            self.try_update_max_concurrent_nodes(self._node_queue.qsize())

        # count the remaining nodes as pruned
        self.increment_pruned(self._node_queue.qsize()) 
        print('fin (t: {0:.3f})'.format(self.get_clamped_time()))

    def _get_node_key(self, bnode):
        '''
        compute the key for a given node by factoring in the cost of a node
        (equivalent to the node's RCM cost) as well as the depth of the node.
        nodes with a lower cost and a higher depth (meaning that more of a 
        path has been discovered) will have higher priority, and will thus
        be dequeued first
        \ntime:     constant --> O(1)
        \nspace:    constant --> O(1)
        '''
        return bnode.get_cost() / bnode.get_depth()
