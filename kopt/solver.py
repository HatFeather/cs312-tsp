from solver_base import SolverBase
from greedy.solver import GreedySolver


class KOptSolver(SolverBase):

    def __init__(self, tsp_solver, max_time):
        super().__init__(tsp_solver, max_time)

    def run_algorithm(self):
        
        route = self.build_initial_route()
        self.set_bssf_from_route(route)


    def swap_cities(self, city_indices):
        pass

    def build_initial_route(self):
        greedy = GreedySolver(self.get_tsp_solver(), self.get_max_time())
        greedy.solve()
        route = greedy.get_bssf_route()

        # use default tour if greedy fails
        if route == None:
            default_results = self.get_tsp_solver().defaultRandomTour()
            route = default_results['soln'].route

        return route
