"""
    Traffic simulation
    Jin Sun
"""

import random
import numpy as np
######
# Helper function


# find distance to next car
# cars is car array, i is current car position
def dis2nextCar(cars_position, current_car_position, numL):
    minDist = numL
    for c in range(0,len(cars_position)):
        dist = numL
        if cars_position[c] < current_car_position: # car is behind
            dist = (numL-1-current_car_position) + (cars_position[c]+1)
        elif cars_position[c] > current_car_position: # car is ahead
            dist = cars_position[c] - current_car_position
        if dist <= minDist:
            minDist = dist
    return minDist

# print road
def printLoad(cars_position, cars_speed, numL):
    L = [-1]*numL
    for c in range(0,len(cars_position)):
        L[cars_position[c]] = cars_speed[c]
    s = ""
    for r in L:
        if r == -1:
            s = s + "."
        else:
            s = s + str(r)
    print s

# calculate average car speed
def avgCarsSpeed(cars_speed, numC):
    return sum(cars_speed)/(numC*1.0)


######

## params
# road blocks
numL = 100

# random param
p = 0.6
maxIter = 100

vmax = 5


# density loop
#densities = np.linspace(0.025,0.3,30)
densities = [0.05]

densityIdx = 0

avgSpeedByDensity = [0]*len(densities)
for rho in densities:
    numC = int(numL*rho)

    # car position array
    cars_position = [0]*numC
    # car speed array
    cars_speed    = [0]*numC

    # init condition
    #cars_position = [10, 20, 26, 30, 50, 51, 53, 70, 99]
    #cars_speed    = [4, 5, 5, 5, 0, 0, 1, 4, 5]
    cars_position = random.sample(range(0,numL), numC)
    cars_speed    = [0]*numC
    for c in range(0,numC):
        cars_speed[c] = random.randint(0,5)

    for iter in range(0, maxIter):
        new_cars_position = [0]*numC
        # for each car
        for c in range(0,len(cars_position)):
            # calculate distance to next car
            dis2nextCar_val =  dis2nextCar(cars_position, cars_position[c], numL)
            # Acceleration
            if cars_speed[c] < vmax and dis2nextCar_val > cars_speed[c]+1:
                cars_speed[c] = cars_speed[c] + 1
            # SLowing down
            if dis2nextCar_val <= cars_speed[c]:
                cars_speed[c] = dis2nextCar_val -1
            # Landomization
            if random.random() <= p:
                # should not have negative speed
                if cars_speed[c] >0:
                    cars_speed[c] = cars_speed[c] -1
            # Car motion
            new_cars_position[c] = (cars_position[c] + cars_speed[c]) % numL
        printLoad(cars_position, cars_speed, numL)
        cars_position = new_cars_position

    avgSpeedByDensity[densityIdx] = avgCarsSpeed(cars_speed, numC)
    densityIdx = densityIdx + 1

print avgSpeedByDensity
