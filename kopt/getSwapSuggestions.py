import heapq


def getAdjacent(index, array):
    first = index - 1
    if first < 0:
        first = len(array) - 1

    last = (index + 1) % len(array)

    return [array[first], array[index], array[last]]


class SwapSuggestion:
    def __init__(self, cities, costs):
        self.cities = cities
        self._cost = sum(costs) / len(costs)

    def getPriority(self):
        return self._cost - 300 * len(self.cities)

    def __lt__(self, other):
        return self.getPriority() < other.getPriority()


CLOSE_CITY = 0.8


class SwapFinder:

    def __init__(self):
        self._cities = []
        self._suggestions = []
        self._shorter = []

    def setCities(self, cities):
        self._cities = cities
        self._processSwapSuggestions()

    def getSuggestion(self):
        if len(self._suggestions) is 0:
            return None
        suggestion = heapq.heappop(self._suggestions)
        return suggestion.cities

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

    def _addSuggestion(self, index1, index2):
        city1, city2 = self._cities[index1], self._cities[index2]
        initPath = [index1, index2]
        initCost = city1.costTo(city2)
        heapq.heappush(self._suggestions, SwapSuggestion(initPath, [initCost]))

        bestCost = 0
        bestPath = initPath
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
                        bestCost = newCost
                        bestPath = newPath
            lastPath = bestPath

    def _processSwapSuggestions(self):
        self._suggestions = []
        for i in range(len(self._cities)):
            self._shorter.append([])
            for j in self._getCloseUnused(i):
                self._shorter[i].append(j)

        for i in range(len(self._shorter)):
            for j in self._shorter[i]:
                self._addSuggestion(i, j)


