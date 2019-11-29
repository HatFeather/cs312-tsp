from solver_base import SolverBase
from copy import copy
from random import randrange
import math


# NOTE: for all code below, let |V| be the number of cities
class GreedySolver(SolverBase):

    def __init__(self, tsp_solver, max_time):
        '''
        initialize this solver using all the defaults provided in solver base
        \ntime:     constant
        \nspace:    constant
        '''
        super().__init__(tsp_solver, max_time)

    def run_algorithm(self):
        '''
        repeatedly tries to greedily solve the TSP by calling 'self._greedy_solve'
        \ntime:     O(|V|) loop, with O(|V|^2) at each loop --> O(|V|^3)
        \nspace:    for the visted set and route array --> O(|V|)
        '''

        # pick a random city to start at
        start_index = randrange(self.get_city_count())

        # O(|V|) loop through all the cities and try to run the greedy algorithm
        for i in self.get_city_range():

            if self.exceeded_max_time():
                return

            # prepare for a new greedy traversal, O(|V|) space at most
            original = (start_index + i) % self.get_city_count()
            current = original
            visited = {current}
            route = [self.get_city_at(current)]

            # O(|V|^2) cost to solve greedily starting at the original node
            sol = self._greedy_solve(original, current, visited, route)
            if sol == None:
                continue

            # a greedy solution was found, update bssf
            self.set_bssf_from_route(sol)
            self.increment_solution_count()
            return

    def _greedy_solve(self, original, current, visited, route):
        '''
        a recursive definition to greedily attempt to find optimal routes
        \ntime:     recurses at most O(|V|) times, each costing O(|V|) --> O(|V|^2)
        \nspace:    visted set and route array take up at most O(2|V|) --> O(|V|)
        '''

        # base case: if all cities have been visited, try and close this route: O(1) time
        # (fails if there is no route back to the original city)
        if len(visited) == self.get_city_count():
            original_city = self.get_city_at(original)
            cost_to_original = self.get_city_at(current).costTo(original_city)
            return None if cost_to_original == math.inf else route

        # O(|V|) time to get the next city (see below)
        target = self._get_next_city(current, visited)
        if target == None:
            return None     # base case: failed to complete route
        else:
            # append the target node found and continue traversing; recurses
            # at most O(|V|) times (as a solution must obtain every city)
            visited.add(target)                     # assumed constant time, at most O(|V|) space
            route.append(self.get_city_at(target))  # assumed constant time, at most O(|V|) space
            return self._greedy_solve(original, target, visited, route)

    def _get_next_city(self, source, visited):
        '''
        gets the least expensive, unvisted neighboring city to the source node
        \ntime:     loops through all neighboring cities --> O(|V|)
        \nspace:    no significant allocations --> O(1)
        '''

        min_cost = math.inf
        min_index = None

        # O(|V|) loop to find the least expensive neighboring city
        for i in self.get_city_range():
            if i in visited:
                continue

            # constant time update for the cheapest 
            # neighboring city not already visted
            target = self.get_city_at(i)
            cost_to_city = self.get_city_at(source).costTo(target)
            if cost_to_city < min_cost:
                min_cost = cost_to_city
                min_index = i

        # return the index of the neighboring least 
        # expensive city to traverse to
        return min_index
