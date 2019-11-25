from typing import List
from TSPClasses import City
import numpy
import math


class RCM:

    def __init__(self, scenario):
        super().__init__()
        
        cities = scenario.getCities()
        city_len = len(cities)

        self._cost = 0.0
        self._length = city_len
        self._values = numpy.empty((self._length, self._length))
        for row in range(self._length):
            for col in range(self._length):
                self._values[row, col] = cities[row].costTo(cities[col])

    def get_cost(self) -> float:
        return self._cost

    def get_row_count(self) -> int:
        return self._length

    def get_col_count(self) -> int:
        return self._length

    def get_values(self) -> List[City]:
        return self._values

    def do_selection(self, row_index, col_index):
        self._cost += self._values[row_index, col_index]
        self._values[col_index, row_index] = math.inf
        for i in range(self._length):
            self._values[i, col_index] = math.inf
            self._values[row_index, i] = math.inf

    def do_reduction(self):
        for row in range(self._length):
            min_val = math.inf
            for col in range(self._length):
                if self._values[row, col] < min_val:
                    min_val = self._values[row, col]
            if min_val == math.inf:
                continue

            self._cost += min_val
            for col in range(self._length):
                self._values[row, col] -= min_val

        for col in range(self._length):
            min_val = math.inf
            for row in range(self._length):
                if self._values[row, col] < min_val:
                    min_val = self._values[row, col]
            if min_val == math.inf:
                continue

            self._cost += min_val
            for row in range(self._length):
                self._values[row, col] -= min_val

    def print(self, label="RCM"):
        print('{}: {}'.format(label, self.get_cost()))
        print(self._values)
        print('')
