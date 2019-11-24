import numpy
import math
import utils


class RCM:

    def init_as_copy(self, rcm_to_copy):
        pass

    def init_as_original(self, scenario):

        cities = scenario.getCities()
        city_len = len(cities)

        self.length = city_len
        self.values = numpy.empty((city_len, city_len))
        for row in range(self.length):
            for col in range(self.length):
                edge_exists = scenario._edge_exists[row, col]
                if edge_exists:
                    sqr_dist = utils.compute_sqr_dist(cities[row], cities[col])
                    self.values[row, col] = sqr_dist
                else:
                    self.values[row, col] = math.inf

    def get_row_count(self):
        return self.length

    def get_col_count(self):
        return self.length

    def do_selection(self, from_index, to_index):
        pass

    def do_reduction(self):

        for row in range(self.length):
            min_val = math.inf
            for col in range(self.length):
                if self.values[row, col] < min_val:
                    min_val = self.values[row, col]
            for col in range(self.length):
                self.values[row, col] -= min_val

        for col in range(self.length):
            min_val = math.inf
            for row in range(self.length):
                if self.values[row, col] < min_val:
                    min_val = self.values[row, col]
            for row in range(self.length):
                self.values[row, col] -= min_val

    def print(self, label="RCM"):
        print(label)
        print(self.values)
