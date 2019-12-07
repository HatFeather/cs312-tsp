from kopt.getSwapSuggestions import SwapFinder
from solver_base import SolverBase
from greedy.solver import GreedySolver


class KOptSolver(SolverBase):

    def __init__(self, tsp_solver, max_time):
        super().__init__(tsp_solver, max_time)

    def run_algorithm(self):

        route = self.build_initial_route()
        self.set_bssf_from_route(route)
        swapFinder = SwapFinder()
        swapFinder.setCities(route)

        suggestion = swapFinder.getSuggestion()
        while suggestion is not None:
            suggestion = swapFinder.getSuggestion()
            # newPath = swap_cities(route, suggestion)
            # if cost of path is less than old best
            #   swapFinder.setCities(newPath)
            #   suggestion = swapFinder.getSuggestion()
        return

    def swap_cities(self, route, indices):
        '''
        take in k indices to swap in the given route\n
        how it works: 
            lazily picks pairs of indices and swaps the cities at those indices;
            i.e. (indices[0], indices[1]), (indices[1], indices[2]) ... (indices[k - 1], indices[k])\n

        time: O(k) loops and O(n) time to swap and concatenate paths --> O(k * n)
        space: stores only one route at a time --> O(n)
        '''

        indices_len = len(indices)
        self.print_route(route, label='before swap')

        # O(k) loop through pairs of swap indices
        for i in range(1, indices_len):

            # ensure indices are in increasing order
            index_a = min(indices[i - 1], indices[i])
            index_b = max(indices[i - 1], indices[i]) + 1

            part_a = route[0:index_a]               # keep the same start of the path
            part_b = route[index_a:index_b][::-1]   # the middle cities must be reversed
            part_c = route[index_b:]                # keep the same end of the path

            # concatenate the path together (not guaranteed to be a valid path)
            route = part_a + part_b + part_c 

        self.print_route(route, label='after swap')
        return route

    def get_route_cost(self, route):
        '''
        O(n) time and O(1) space to loop through a route
        and get its total cost
        TODO: @Avery does your suggestion class already compute costs?
        '''

        cost = 0
        route_len = len(route)

        # sum up the cost of the route
        for i in range(1, route_len):
            prev = route[i - 1]
            curr = route[i]
            cost += prev.costTo(curr)

        cost += route[route_len - 1].costTo(route[0])
        return cost

    def build_initial_route(self):
        '''
        first attempts to solve the TSP greedily; if that fails, the
        default tour is used\n
        this method takes O(n^3) time and O(n) space
        '''

        greedy = GreedySolver(self.get_tsp_solver(), self.get_max_time())
        greedy.solve()
        route = greedy.get_bssf_route()

        # use default tour if greedy fails
        if route == None:
            default_results = self.get_tsp_solver().defaultRandomTour()
            route = default_results['soln'].route

        return route

    def print_route(self, route, label='path'):
        print('{}:\t'.format(label), end='')
        if route == None:
            print('None')
        else:
            for i in range(len(route)):
                print('{}, '.format(route[i]._index), end='')
            print('')
