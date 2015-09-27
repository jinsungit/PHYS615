"""
    Traffic simulation
    Jin Sun
"""

import random
######
# Helper function


# find distance to next car
# R is road array, i is current car position
def dis2nextCar(R,i):
    numR = len(R)
    for j in range(1,numR):
        if R[(i + j)%numR] >0:
            return j
    return numR 

# print road
def printRoad(R):
    s = ""
    for r in R:
        if r == 0:
            s = s + "."
        else:
            s = s + str(r)
    print s


# road blocks
numR = 100
R = [0] * numR

vmax = 5



# road init condition
R[20] = 4
R[80] = 5
R[99] = 5

# random param
p = 0.5

maxIter = 20

for iter in range(0, maxIter):
    printRoad(R)
    for i in range(0, numR):
        # for each car
        if R[i]>0:
            dis2nextCar_val = dis2nextCar(R,i)
            # Acceleration
            if R[i]<vmax and dis2nextCar_val>R[i]+1:
                R[i] = R[i]+1
            # Slowing down
            if dis2nextCar_val <= R[i]:
                R[i] = dis2nextCar_val - 1
            # Randomization
            if random.random() <= p:
                R[i] = R[i] - 1
                if R[i] == -1:
                    R[i] = 0
            # Car motion
            R[(i+R[i]) % numR] = R[i]
            R[i] = 0

