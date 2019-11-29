from branch_bound.rcm import RCM
from TSPClasses import City
from copy import deepcopy
from typing import List
import math


# NOTE: for all code below, let |V| be the number of cities
class BranchNode:

    def __init__(self, rcm: RCM, city: City, city_index: int, parent):
        '''
        intializes this branch node based on the arguments passed
        \ntime:     O(1)
        \nspace:    assigned class variables by reference --> O(1)
        '''

        super().__init__()

        # use the parent node to obtain the depth of this node
        self._depth = 1 if parent == None else parent.get_depth() + 1
        self._rcm = rcm
        self._children = []
        self._city_index = city_index
        self._city = city
        self._parent = parent

    def __lt__(self, other):
        '''
        compares two nodes; used to break ties in the priority queue
        \ntime:     O(1)
        \nspace:    O(1)
        '''
        return self.get_cost() < other.get_cost()

    def compute_path(self) -> List[City]:
        '''
        recursively travel up the tree to compute the route from the given node
        \ntime:     with at most |V| cities --> O(|V|)
        \nspace:    allocates a route array --> O(|V|)
        '''

        # base case, reached the end of the route
        if self.get_parent() == None:
            return [self.get_city()]

        # recurse to the next parent node at most O(|V|) times
        parent = self.get_parent()
        path = parent.compute_path()
        path.append(self.get_city())
        return path

    def generate_child_nodes(self, cities: List[City]):
        '''
        for the city associated with this node, generate child nodes
        based on the cities this node's city has a valid path to
        \ntime:     O(|V|) loop with O(|V|^2) at each loop --> O(|V|^3)
        \nspace:    generate O(|V|) children costing O(|V|^2) each --> O(|V|^3)
        '''

        # based on this nodes current city (and the row in the RCM associated
        # with that city), loop through all neighboring cities --> O(|V|) time
        from_idx = self.get_city_index()
        for to_idx in range(self.get_rcm().get_col_count()):

            # ensure that there is a valid path to that city
            cost = self.get_rcm().get_value_at(from_idx, to_idx)
            if cost < math.inf:

                # O(|V|^2) space and assumed O(|V|^2) time to copy
                rcm = deepcopy(self.get_rcm())
                rcm.do_selection(from_idx, to_idx)  # O(|V|) time
                rcm.do_reduction()                  # O(|V|^2) time

                # create and add the child node with the values allocated --> O(1)
                child = BranchNode(rcm, cities[to_idx], to_idx, self)
                self._children.append(child)

    ####### REGION: HELPER METHODS #######
    # all these methods are assumed to require consant time and space

    def get_depth(self) -> int:
        return self._depth

    def get_city_index(self) -> int:
        return self._city_index

    def get_rcm(self) -> RCM:
        return self._rcm

    def get_parent(self):
        return self._parent

    def get_city(self) -> City:
        return self._city

    def get_cost(self) -> float:
        return self.get_rcm().get_cost()

    def get_children(self):
        return self._children

    def get_child_count(self) -> int:
        return len(self.get_children())

    ####### END REGION: HELPER METHODS #######
