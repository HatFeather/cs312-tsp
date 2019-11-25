import numpy
import math
import utils

class RCM:

    def init_as_copy(self, rcm_to_copy):
        self.cost = rcm_to_copy.cost
        self.length = rcm_to_copy.length
        self.values = numpy.copy(rcm_to_copy.values)

    def init_as_original(self, scenario):
        cities = scenario.getCities()
        city_len = len(cities)

        self.cost = 0.0
        self.length = city_len
        self.values = numpy.empty((self.length, self.length))
        for row in range(self.length):
            for col in range(self.length):
                edge_exists = scenario._edge_exists[row, col]
                if edge_exists:
                    sqr_dist = utils.compute_sqr_dist(cities[row], cities[col])
                    self.values[row, col] = sqr_dist
                else:
                    self.values[row, col] = math.inf

        self.length = 4
        self.values = numpy.array([
            [math.inf, 7, 3, 12],
            [3, math.inf, 6, 14],
            [5, 8, math.inf, 6],
            [9, 3, 5, math.inf]])

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
