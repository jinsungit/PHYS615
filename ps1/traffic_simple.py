"""
    Traffic simulation
    Jin Sun
"""

import random
######
# Helper function


# find distance to next car
# cars is car array, i is current car position
def dis2nextCar(cars_position, current_car_position, numR):
    minDist = numR
    for c in range(0,len(cars_position)):
        dist = numR
        if cars_position[c] < current_car_position: # car is behind
            dist = (numR-1-current_car_position) + (cars_position[c]+1)
        elif cars_position[c] > current_car_position: # car is ahead
            dist = cars_position[c] - current_car_position
        if dist <= minDist:
            minDist = dist
    return minDist

# print road
def printRoad(cars_position, cars_speed, numR):
    R = [-1]*numR
    for c in range(0,len(cars_position)):
        R[cars_position[c]] = cars_speed[c]

    s = ""
    for r in R:
        if r == -1:
            s = s + "."
        else:
            s = s + str(r)
    print s

######

# road blocks
numR = 100


# cars
numC = 9

# car position array
cars_position = [0]*numC
# car speed array
cars_speed    = [0]*numC


# init condition
cars_position = [10, 20, 26, 30, 50, 51, 53, 70, 99]
cars_speed    = [4, 5, 5, 5, 0, 0, 1, 4, 5]

# random param
p = 0.6
maxIter = 200

vmax = 5

for iter in range(0, maxIter):
    printRoad(cars_position, cars_speed, numR)
    new_cars_position = [0]*numC
    # for each car
    for c in range(0,len(cars_position)):
        # calculate distance to next car
        dis2nextCar_val =  dis2nextCar(cars_position, cars_position[c], numR)
        # Acceleration
        if cars_speed[c] < vmax and dis2nextCar_val > cars_speed[c]+1:
            cars_speed[c] = cars_speed[c] + 1
        # SLowing down
        if dis2nextCar_val <= cars_speed[c]:
            cars_speed[c] = dis2nextCar_val -1
        # Randomization
        if random.random() <= p:
            # should not have negative speed
            if cars_speed[c] >0:
                cars_speed[c] = cars_speed[c] -1
        # Car motion
        new_cars_position[c] = (cars_position[c] + cars_speed[c]) % numR
    cars_position = new_cars_position
