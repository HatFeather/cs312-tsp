from typing import List
from TSPClasses import City
import numpy
import math


# NOTE: for all code below, let |V| be the number of cities
class RCM:

    def __init__(self, scenario):
        '''
        initializes the RCM based on city-to-city costs
        \ntime:     allocating and initializing the matrix --> O(|V|^2)
        \nspace:    allocating an |V|*|V| matrix --> O(|V|^2)
        '''

        super().__init__()
        
        cities = scenario.getCities()
        city_len = len(cities)

        # allocate the matrix, requiring O(|V|^2) space and assumed 
        # to take O(|V|^2) time
        self._cost = 0.0
        self._length = city_len
        self._values = numpy.empty((self._length, self._length))

        # O(|V|^2) loop to set all inital city-to-city costs
        for row in range(self._length):
            for col in range(self._length):
                self._values[row, col] = cities[row].costTo(cities[col])

    def do_selection(self, row_index, col_index):
        '''
        performs a selection on the specified row and columns (i.e. marks 
        cityX --> cityY as visited and increments the cost by taking that route)
        \ntime:     Loop through all values in a row and column --> O(|V|)
        \nspace:    no significant allocations --> O(1)
        '''

        # constant time increment the cost of the rcm based on the city chosen
        self._cost += self._values[row_index, col_index]

        # O(|V|) loop to update all values in the row/column to infinity, and
        # thereby mark cityX --> cityY as visited
        self._values[col_index, row_index] = math.inf
        for i in range(self._length):
            self._values[i, col_index] = math.inf
            self._values[row_index, i] = math.inf

    def do_reduction(self):
        '''
        row and column reduction to increment the cost of this RCM
        \ntime:     two (|V|^2) loops to reduce --> O(|V|^2)
        \nspace:    just using memory alread allocated --> O(1)
        '''

        # O(|V|) time loop to reduce all rows, O(|V|) time at each loop
        for row in range(self._length):

            # compute the min value in the row, O(|V|) time (don't 
            # reduce if no min was found)
            min_val = math.inf
            for col in range(self._length):
                if self._values[row, col] < min_val:
                    min_val = self._values[row, col]
            if min_val == math.inf:
                continue

            # O(|V|) loop to decrement all values in the row by the min
            self._cost += min_val
            for col in range(self._length):
                self._values[row, col] -= min_val

        # O(|V|) time loop to reduce all columns, O(|V|) time at each loop
        for col in range(self._length):

            # compute the min value in the column, O(|V|) time (don't 
            # reduce if no min was found)
            min_val = math.inf
            for row in range(self._length):
                if self._values[row, col] < min_val:
                    min_val = self._values[row, col]
            if min_val == math.inf:
                continue

            # O(|V|) loop to decrement all values in the column by the min
            self._cost += min_val
            for row in range(self._length):
                self._values[row, col] -= min_val

    ####### REGION: HELPER METHODS #######
    # all these methods are assumed to require consant time and space

    def get_cost(self) -> float:
        return self._cost

    def get_row_count(self) -> int:
        return self._length

    def get_col_count(self) -> int:
        return self._length

    def get_value_at(self, row, col) -> float:
        return self._values[row, col]

    def print(self, label="RCM"):
        print('{}: {}'.format(label, self.get_cost()))
        print(self._values)
        print('')

    ####### END REGION: HELPER METHODS #######
