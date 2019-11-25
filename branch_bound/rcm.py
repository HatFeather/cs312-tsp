import numpy
import math
import branch_bound.utils as utils


class RCM:

    def __init__(self, scenario):
        cities = scenario.getCities()
        city_len = len(cities)

        self.cost = 0.0
        self.length = city_len
        self.values = numpy.empty((self.length, self.length))
        for row in range(self.length):
            for col in range(self.length):
                self.values[row, col] = cities[row].costTo(cities[col])

    def get_cost(self):
        return self.cost

    def get_row_count(self):
        return self.length

    def get_col_count(self):
        return self.length

    def do_selection(self, row_index, col_index):
        self.cost += self.values[row_index, col_index]
        self.values[col_index, row_index] = math.inf
        for i in range(self.length):
            self.values[i, col_index] = math.inf
            self.values[row_index, i] = math.inf

    def do_reduction(self):
        for row in range(self.length):
            min_val = math.inf
            for col in range(self.length):
                if self.values[row, col] < min_val:
                    min_val = self.values[row, col]
            if min_val == math.inf:
                continue

            self.cost += min_val
            for col in range(self.length):
                self.values[row, col] -= min_val

        for col in range(self.length):
            min_val = math.inf
            for row in range(self.length):
                if self.values[row, col] < min_val:
                    min_val = self.values[row, col]
            if min_val == math.inf:
                continue

            self.cost += min_val
            for row in range(self.length):
                self.values[row, col] -= min_val

    def print(self, label="RCM"):
        print('{}: {}'.format(label, self.get_cost()))
        print(self.values)
        print('')
