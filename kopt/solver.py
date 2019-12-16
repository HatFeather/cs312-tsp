from kopt.getSwapSuggestions import SwapFinder
from solver_base import SolverBase
from greedy.solver import GreedySolver
from greedy.solver import get_route_cost


class KOptSolver(SolverBase):

    def __init__(self, tsp_solver, max_time):
        super().__init__(tsp_solver, max_time)
    

    def run_algorithm(self):
        '''
        Local search which updates suggestions for the current route.
        Each time 'swapFinder.setCities(route)' is called, a new bucket 
        of possible search spaces is produced. When a better solution is
        found, the search space is updated.\n
        '''

        # O(n^3) time and O(n) space to compute initial BSSF
        route = self.build_initial_route()
        self.set_bssf_from_route(route)
        swapFinder = SwapFinder()
        swapFinder.setCities(route)

        # check all the suggestions procuded by the swapFinder
        suggestion = swapFinder.getSuggestion()
        while suggestion is not None and not self.exceeded_max_time():

            # the suggestion has k suggested swaps --> O(k * n) time to swap cities
            next_route = self.swap_cities(route, suggestion)
            next_cost = get_route_cost(next_route)

            # update the bssf if we've found a less expensive route by swapping
            if next_cost < self.get_best_cost():
                route = next_route
                swapFinder.setCities(route)
                self.increment_solution_count()
                self.set_bssf_from_route(route)
                print('sol (t: {0:.3f})'.format(self.get_clamped_time()))

            suggestion = swapFinder.getSuggestion()
            
        print('fin (t: {0:.3f})'.format(self.get_clamped_time()))
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

        return route
    

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
        return
