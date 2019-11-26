from TSPClasses import City
from TSPClasses import Scenario
from TSPClasses import TSPSolution
from typing import List
from abc import abstractmethod
import time
import math


class SolverBase:

    def __init__(self, tsp_solver):
        super().__init__()

        self._results = {}
        self._tsp_solver = tsp_solver
        self._scenario = tsp_solver._scenario
        self._cities = self.get_scenario().getCities()
        self._city_count = len(self._cities)

        self.set_bssf(None)
        self.set_max(None)
        self.set_total(None)
        self.set_pruned(None)

    def get_results(self):
        return self._results

    def get_tsp_solver(self):
        return self._tsp_solver

    def get_scenario(self) -> Scenario:
        return self._scenario

    def get_cities(self) -> List[City]:
        return self._cities

    def get_city_count(self) -> int:
        return self._city_count

    def get_city_at(self, index) -> City:
        return self.get_cities()[index]

    def get_city_range(self):
        return range(self.get_city_count())

    def set_bssf_from_route(self, route):
        self.set_bssf(TSPSolution(route))

    def get_bssf(self):
        return self._bssf

    def set_bssf(self, value):
        self._bssf = value

    def get_max(self):
        return self._max

    def set_max(self, value):
        self._max = value

    def get_total(self):
        return self._total

    def set_total(self, value):
        self._total = value

    def get_pruned(self):
        return self._pruned

    def set_pruned(self, value):
        self._pruned = value

    def increment_pruned(self):
        self.set_pruned(self.get_pruned() + 1)

    def solve(self):

        start_time = time.time()
        self.run_algorithm()
        end_time = time.time()

        bssf = self.get_bssf()
        self._results['cost'] = bssf.cost if bssf != None else math.inf
        self._results['time'] = end_time - start_time
        self._results['count'] = 0  # TODO ??
        self._results['soln'] = self.get_bssf()
        self._results['max'] = self.get_max()
        self._results['total'] = self.get_total()
        self._results['pruned'] = self.get_pruned()

    @abstractmethod
    def run_algorithm(self):
        pass
