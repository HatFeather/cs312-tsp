import heapq


class SwapSuggestion:
    def __init__(self, cities):
        self.cities = cities


class SwapFinder:

    def __init__(self):
        self.cities = []
        self.suggestions = []

    def setCities(self, cities):
        self.cities = cities
        self._processSwapSuggestions()

    def getSuggestion(self):
        pass

    def _processSwapSuggestions(self):
        results = []
        for city in self.cities:
            currentTest = city
            results = []
            while currentTest is not None:
                print('', end='')
                # find shortest unused path coming out from city
                # if below certain threshold
                #   currentTest = nextCity
                #   add city to results
                # else
                #   currentTest = None
        return results


# # # # DEBUG TEST # # # #

# # # # END DEBUG  # # # #
