from solver_base import SolverBase
from copy import copy
from random import randrange
import math


class GreedySolver(SolverBase):

    def __init__(self, tsp_solver, max_time):
        super().__init__(tsp_solver, max_time)

    def run_algorithm(self):

        start_index = randrange(self.get_city_count())
        for i in self.get_city_range():

            original = (start_index + i) % self.get_city_count()
            current = original
            visited = {current}
            route = [self.get_city_at(current)]

            sol = self._greedy_solve(original, current, visited, route)
            self.increment_solution_try_count()
            if sol == None:
                continue

            self.set_bssf_from_route(sol)
            return

    def _greedy_solve(self, original, current, visited, route):
        if len(visited) == self.get_city_count():
            original_city = self.get_city_at(original)
            cost_to_original = self.get_city_at(current).costTo(original_city)
            return None if cost_to_original == math.inf else route

        target = self._get_next_city(current, visited)
        if target == None:
            return None
        else:
            visited.add(target)
            route.append(self.get_city_at(target))
            return self._greedy_solve(original, target, visited, route)

    def _get_next_city(self, source, visited):
        min_cost = math.inf
        min_index = None

        for i in self.get_city_range():
            if i in visited:
                continue

            target = self.get_city_at(i)
            cost_to_city = self.get_city_at(source).costTo(target)
            if cost_to_city < min_cost:
                min_cost = cost_to_city
                min_index = i

        return min_index
