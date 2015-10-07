"""
    Traffic simulation 
    Jin Sun
    PHYS615, Problem Set 1
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
def printRoad(cars_position, cars_speed, numL):
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

# calculate speed distribution
def speedDist(cars_speed):
    sd = [0]*6
    for cs in cars_speed:
        sd[cs] = sd[cs]+1
    return sd

######
# output file
favgSpeed = open('avgSpeed.txt','w')
fspeedDist = open('speedDist.txt','w')

## params
# road blocks
numL = 100

# random param
p = 0.6
vmax = 5
t0 = 10*numL
maxIter = 10000

numSimulation = 100

# density loop
densities = np.linspace(0.025,0.3,30)
#densities = [0.03, 0.08, 0.4, 0.6]


for simulationIdx in range(0,numSimulation):
    print 'Simulation '+str(simulationIdx+1)
    densityIdx = 0
    avgSpeedByDensity = [0]*len(densities)
    for rho in densities:
        numC = int(numL*rho)

        # car position array
        cars_position = [0]*numC
        # car speed array
        cars_speed    = [0]*numC

        # init condition
        cars_position = random.sample(range(0,numL), numC)
        # according to paper, init to be zero
        cars_speed    = [0]*numC 
        
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
                # Randomization
                if random.random() <= p:
                    # should not have negative speed
                    if cars_speed[c] >0:
                        cars_speed[c] = cars_speed[c] -1
                # Car motion
                new_cars_position[c] = (cars_position[c] + cars_speed[c]) % numL
            # print current road
            if False and iter>=t0:
                printRoad(cars_position, cars_speed, numL)
            cars_position = new_cars_position

        avgSpeedByDensity[densityIdx] = avgCarsSpeed(cars_speed, numC)
        densityIdx = densityIdx + 1
        
        # print speed distribution for current density
        #sd = speedDist(cars_speed)
        #for i in range(0,len(sd)):
            #fspeedDist.write(str(sd[i]))
            #fspeedDist.write(' ')
        #fspeedDist.write('\n')
        # density loop end

    for i in range(0,len(avgSpeedByDensity)):
        favgSpeed.write(str(avgSpeedByDensity[i]))
        favgSpeed.write(' ')
    favgSpeed.write('\n')

favgSpeed.close()
fspeedDist.close()
