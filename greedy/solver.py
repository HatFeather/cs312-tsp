from solver_base import SolverBase
from queue import PriorityQueue
from queue import LifoQueue
from copy import copy


class GreedySolver(SolverBase):

    def __init__(self, tsp_solver):
        super().__init__(tsp_solver)
        self._visited = super().create_empty_city_set()
        self._visit_matrix = self._create_sorted_visit_matrix()

    def solve(self):

        # TODO
        # start at a city, go to its nearest neighbor, repeat
        # if not loop found, backtrack and go back up
        # 
        # the _visit_matrix sorts by distance, so just follow those

        pass

    def _create_sorted_visit_matrix(self):
        result = [None] * super().get_city_count()

        for i in super().get_city_range():
            city_a = super().get_city_at(i)
            sorted_cities = copy(super().get_cities())
            sorted_cities.sort(key=lambda city_b: city_a.costTo(city_b))
            result[i] = sorted_cities

        return result
