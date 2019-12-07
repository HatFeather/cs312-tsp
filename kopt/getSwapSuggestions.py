import heapq


# given an index into an array representing a path,
# returns the city specified by the index and the two
# adjacent cities.
def getAdjacent(index, array):
    first = index - 1
    if first < 0:
        first = len(array) - 1

    last = (index + 1) % len(array)

    return [array[first], array[index], array[last]]


# represents a suggestion of cities to put next to each other
# in a swap
class SwapSuggestion:
    def __init__(self, cities, costs):
        self.cities = cities
        self._cost = sum(costs) / len(costs)

    def getPriority(self):
        return self._cost - 300 * len(self.cities)

    def __lt__(self, other):
        return self.getPriority() < other.getPriority()


# this constant decides which cities are counted as 'close'. The higher the number,
# the more suggested paths the algorithm will return
CLOSE_CITY = 0.8


# class that finds cities to swap given a path
class SwapFinder:

    def __init__(self):
        self._cities = []
        self._suggestions = []
        self._shorter = []

    # call to reset the path to a new one
    def setCities(self, cities):
        self._cities = cities
        self._processSwapSuggestions()

    # return the suggestion with the lowest cost and remove it
    def getSuggestion(self):
        if len(self._suggestions) is 0:
            return None
        suggestion = heapq.heappop(self._suggestions)
        return suggestion.cities

    # gets the cities close to the given city that are not being used in the current path.
    # runs in O(n) where n is the number of cities because it iterates through each city.
    def _getCloseUnused(self, index):
        results = []
        city = self._cities[index]

        removedCities = getAdjacent(index, self._cities)
        candidates = [city if city not in removedCities else None for city in self._cities]

        dist = self._cities[index].costTo(self._cities[(index+1) % len(self._cities)])

        for i in range(len(candidates)):
            city2 = candidates[i]
            if city2 is not None and city.costTo(city2) < dist * CLOSE_CITY:
                results.append(i)
        return results

    # given two indicies in the cities, updates the suggestions to include
    # the path between those two cities as well as several paths that start with those cities
    def _addSuggestion(self, index1, index2):
        # add the initial 2 cities
        city1, city2 = self._cities[index1], self._cities[index2]
        initPath = [index1, index2]
        initCost = city1.costTo(city2)
        heapq.heappush(self._suggestions, SwapSuggestion(initPath, [initCost]))

        # look for paths of length longer than 2
        bestCost = 0
        lastPath = initPath
        lastCosts = [initCost]
        while bestCost < float('inf'):
            bestCost = float('inf')
            bestPath = []
            last = lastPath[len(lastPath) - 1]
            for newCity in self._shorter[last]:
                if newCity not in lastPath:
                    newPath = lastPath + [newCity]
                    newCost = self._cities[last].costTo(self._cities[newCity])
                    newCosts = lastCosts + [newCost]
                    heapq.heappush(self._suggestions, SwapSuggestion(newPath, newCosts))

                    if newCost < bestCost:
                        # next iteration, we only use the best path found for time's sake
                        bestCost = newCost
                        bestPath = newPath

            lastPath = bestPath

    # given a new set of cities, update all of the suggestions
    # runs in O(n^2) because of the nested for loop
    def _processSwapSuggestions(self):
        self._suggestions = []
        for i in range(len(self._cities)):
            self._shorter.append([])
            for j in self._getCloseUnused(i):
                self._shorter[i].append(j)

        for i in range(len(self._shorter)):
            for j in self._shorter[i]:
                self._addSuggestion(i, j)


