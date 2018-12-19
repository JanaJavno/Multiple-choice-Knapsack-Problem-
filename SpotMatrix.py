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
        if len(self.data[i]) > j - self.shifts[i]:
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
