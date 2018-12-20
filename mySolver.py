import numpy as np
from numpy import array, zeros, ones
from readModule import readSpots, readConfines
from SpotMatrix import SpotMatrix

data, shifts = readSpots()
SM = SpotMatrix(np.array(data), np.array(shifts))

def greedy_solver():
    confines = np.array(readConfines())

    zeros = np.zeros((confines.size,), dtype=int)

    max_spots = []
    result_spots = []
    while not np.array_equal(confines, zeros):
        max_spots = []
        for i, confine in enumerate(confines):
            if confine > 0:
                temp = confine
                max_spots_i_row = sorted(SM.getrow(i), reverse=True)[:confine]
                for elem in sorted(set(max_spots_i_row), reverse=True):
                    indices = np.where(np.array(SM.getrow(i)) == elem)[0]
                    for index in indices:
                        if temp > 0:
                            max_spots.append((elem, i, index + SM.shifts[i]))
                            temp -= 1
        max_spots.sort(reverse=True)
        for big_spot in max_spots:
            if SM.getitem(big_spot[1], big_spot[2]) != 0:
                SM.greedy_quality += big_spot[0]
                result_spots.append((big_spot[0], big_spot[1], big_spot[2] - SM.shifts[1]))
                SM.nullcolumn(big_spot[1], big_spot[2])
                confines[big_spot[1]] -= 1

    with open("output.txt", "w") as fileoutput:
        fileoutput.write(str(SM.greedy_quality) + '\n')
        fileoutput.write(str(result_spots))