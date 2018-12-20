from numpy import array, ones

class SpotMatrix:
    data = []
    shifts = []
    greedy_quality = 0

    def __init__(self, data, shifts):
        self.data = data
        self.shifts = shifts

    def __iter__(self):
        for i in self.data:
            yield i

    def getitem(self, i, j):
        if len(self.data[i]) > j - self.shifts[i] >= 0:
            return self.data[i][j - self.shifts[i]]
        else:
            return 0

    def setitem(self, value, i, j):
        try:
            if len(self.data[i]) > j - self.shifts[i] >= 0:
                self.data[i][j - self.shifts[i]] = value
        except IndexError:
            print('i: ' + str(i) + 'j: ' + str(j) + 'len: ' + str(len(self.data[i])) + 'shift: ' + str(self.shifts[i]))

    def getrow(self, i):
        return self.data[i]

    def nullcolumn(self, i,  j):
        for k, _ in enumerate(self.shifts):
            if k != i:
                self.setitem(0, k, j)

    def toVector(self):
        vector = []
        for row in self.data:
            vector += row
        return vector

    def columnCount(self):
        return self.shifts[-1] + len(self.data[-1])

    def indicators(self):
        result, values = [], []
        subresult = []
        allSpots = len(self.toVector())
        allCampaigns = len(self.data)
        for j in range(allSpots):
            subresult = []
            for i in range(allCampaigns):
                if self.getitem(i, j) != 0:
                    subresult.append(i)
            result.append(array(subresult))
            values.append(ones(len(subresult)))
        return result, values
