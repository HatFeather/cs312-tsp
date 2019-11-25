from TSPClasses import City
from TSPClasses import Scenario
from typing import List
from typing import Set
from abc import abstractmethod

class SolverBase:

    def __init__(self, tsp_solver):
        super().__init__()
        self._results = {}
        self._tsp_solver = tsp_solver
        self._scenario = tsp_solver._scenario
        self._cities = self.get_scenario().getCities()
        self._city_count = len(self._cities)

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

    def get_start_city(self) -> City:
        return self.get_cities()[0]
    
    def get_city_range(self):
        return range(self.get_city_count())

    @abstractmethod
    def solve(self):
        pass

    def create_full_city_set(self) -> Set[City]:
        return set(self.get_cities())

    def create_empty_city_set(self) -> Set[City]:
        return set([])
