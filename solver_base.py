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

        self.bssf = None
        self.max = None
        self.total = None
        self.pruned = None

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

    def set_bssf(self, route):
        self.bssf = TSPSolution(route)

    def solve(self):

        start_time = time.time()
        self.run_algorithm()
        end_time = time.time()

        self._results['cost'] = self.bssf.cost if self.bssf != None else math.inf
        self._results['time'] = end_time - start_time
        self._results['count'] = 0  # TODO ??
        self._results['soln'] = self.bssf
        self._results['max'] = self.max
        self._results['total'] = self.total
        self._results['pruned'] = self.pruned

    @abstractmethod
    def run_algorithm(self):
        pass
