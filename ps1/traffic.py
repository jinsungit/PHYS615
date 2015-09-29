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
R[30] = 4
R[12] = 3
R[45] = 5
R[67] = 3
R[80] = 5
R[99] = 5

# random param
p = 0.1

maxIter = 20

for iter in range(0, maxIter):
    printRoad(R)
    nextR = list(R)
    for i in range(0, numR):
        # for each car
        if R[i]>0:
            dis2nextCar_val = dis2nextCar(R,i)
            # Acceleration
            if R[i]<vmax and dis2nextCar_val>R[i]+1:
                nextR[i] = R[i]+1
            # Slowing down
            if dis2nextCar_val <= R[i]:
                nextR[i] = dis2nextCar_val - 1
            # Randomization
            if random.random() <= p:
                nextR[i] = R[i] - 1
                if nextR[i] == -1:
                    nextR[i] = 0
            # Car motion
            nextR[(i+nextR[i]) % numR] = nextR[i]
            nextR[i] = 0
    R = nextR

