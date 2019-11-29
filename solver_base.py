from TSPClasses import City
from TSPClasses import Scenario
from TSPClasses import TSPSolution
from typing import List
from abc import abstractmethod
import time
import math


# a base class for all TSP solvers that helps abstract the logic
# for creating, returning, and updating solutions
class SolverBase:

    # initialize references to helper variables
    # time:     constant
    # space:    constant
    def __init__(self, tsp_solver, max_time):
        super().__init__()

        # cache values that are used throughout
        # the different solvers
        self._results = {}
        self._tsp_solver = tsp_solver
        self._scenario = tsp_solver._scenario
        self._cities = self.get_scenario().getCities()
        self._city_count = len(self._cities)
        self._max_time = max_time
        self._start_time = None
        self._end_time = None
        self._intermediate_cnt = 0
        self._total = 0
        self._pruned = 0

        self.set_bssf(None)
        self.set_max(None)

    # runs and solves the TSP using some algorithm (based on whichever solver 
    # implements this class); thus, the time and space complexity will vary
    def solve(self):

        # time and run the algorithm
        self._start_time = time.time()
        self.run_algorithm()

        # update the results dictionary
        bssf = self.get_bssf()
        self._results['cost'] = bssf.cost if bssf != None else math.inf
        self._results['time'] = self.get_clamped_time()
        self._results['count'] = self._intermediate_cnt
        self._results['soln'] = bssf
        self._results['max'] = self.get_max()
        self._results['total'] = self._total
        self._results['pruned'] = self._pruned

    # child classes will implement this method based on different ways of 
    # solving the TSP (time and space complexity will vary)
    @abstractmethod
    def run_algorithm(self):
        pass

    ####### REGION: HELPER METHODS #######
    # all methods in this region are assumed to have constant time and space 
    # complexity and will not be counted toward the total complexity of the 
    # algorithms (these methods are self explanatory and just make the code 
    # more readable)

    def get_max_time(self):
        return self._max_time

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

    def get_bssf(self) -> TSPSolution:
        return self._bssf

    def set_bssf(self, value):
        self._bssf = value

    def get_max(self):
        return self._max

    def set_max(self, value):
        self._max = value

    def increment_total(self, amount=1):
        self._total += amount

    def increment_pruned(self, amount=1):
        self._pruned += amount

    def increment_solution_count(self, amount=1):
        self._intermediate_cnt += amount

    def get_total_time(self):
        return time.time() - self._start_time

    def get_clamped_time(self):
        return min(self.get_max_time(), self.get_total_time())

    def exceeded_max_time(self):
        return self.get_total_time() > self.get_max_time()

    ####### END REGION: HELPER METHODS #######
