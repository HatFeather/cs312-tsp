from branch_bound.rcm import RCM
from TSPClasses import City
from copy import deepcopy
from typing import List
import math


class BranchNode:

    def __init__(self, rcm: RCM, city: City, city_index: int, parent):
        super().__init__()
        self._rcm = rcm
        self._children = []
        self._city_index = city_index
        self._city = city
        self._parent = parent
        self._depth = 1 if parent == None else parent.get_depth() + 1

    def __lt__(self, other): 
        return self.get_cost() < other.get_cost()

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

    def get_path(self) -> List[City]:
        if self.get_parent() == None:
            return [self.get_city()]
        else:
            parent = self.get_parent()
            path = parent.get_path()
            path.append(self.get_city())
            return path

    def get_cost(self) -> float:
        return self.get_rcm().get_cost()

    def get_children(self):
        return self._children

    def get_child_count(self) -> int:
        return len(self.get_children())

    def generate_child_nodes(self, cities: List[City]):

        from_idx = self.get_city_index()
        for to_idx in range(self.get_rcm().get_col_count()):

            cost = self.get_rcm().get_value_at(from_idx, to_idx)
            if cost < math.inf:

                rcm = deepcopy(self.get_rcm())
                rcm.do_selection(from_idx, to_idx)
                rcm.do_reduction()

                child = BranchNode(rcm, cities[to_idx], to_idx, self)
                self._children.append(child)
