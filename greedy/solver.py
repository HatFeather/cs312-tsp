from solver_base import SolverBase
from copy import copy
from random import randrange
import math


class GreedySolver(SolverBase):

    def __init__(self, tsp_solver):
        super().__init__(tsp_solver)

    def run_algorithm(self):

        start_index = randrange(super().get_city_count())
        for i in super().get_city_range():

            original = (start_index + i) % super().get_city_count()
            current = original
            visited = {current}
            route = [super().get_city_at(current)]

            sol = self._greedy_solve(original, current, visited, route)
            if sol == None:
                continue
            
            super().set_bssf(sol)
            return

    def _greedy_solve(self, original, current, visited, route):
        if len(visited) == super().get_city_count():
            original_city = super().get_city_at(original)
            cost_to_original = super().get_city_at(current).costTo(original_city)
            return None if cost_to_original == math.inf else route

        target = self._get_next_city(current, visited)
        if target == None:
            return None
        else:
            visited.add(target)
            route.append(super().get_city_at(target))
            return self._greedy_solve(original, target, visited, route)

    def _get_next_city(self, source, visited):
        min_cost = math.inf
        min_index = None

        for i in super().get_city_range():
            if i in visited:
                continue

            target = super().get_city_at(i)
            cost_to_city = super().get_city_at(source).costTo(target)
            if cost_to_city < min_cost:
                min_cost = cost_to_city
                min_index = i

        return min_index
