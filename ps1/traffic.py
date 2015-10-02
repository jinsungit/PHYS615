"""
    Traffic simulation
    Jin Sun
"""

import random
######
# Helper function


# find distance to next car
# cars is car array, i is current car position
def dis2nextCar(cars,i):
    minDist = numR
    for car in cars:
        dist = numR
        if car.position < i: # car is behind
            dist = (numR-1-i) + (car.position+1)
            if dist <= minDist:
                minDist = dist
    return minDist

# print road
def printRoad(cars):
    R = [0]*numR
    for car in cars:
        R[car.position] = car.speed

    s = ""
    for r in R:
        if r == 0:
            s = s + "."
        else:
            s = s + str(r)
    print s

######
class Car:
    def __init__(self, speed, position, numR):
        self.speed    = speed
        self.position = position
        self.dis2nextCar_val = 0
        self.numR = numR
        self.vmax = 5 # max speed
    
    def carActionRules(self):
        self.dis2nextCar_val = dis2nextCar(cars,self.position)
        # Acceleration
        if self.speed < self.vmax and self.dis2nextCar_val > self.speed+1:
            self.speed = self.speed + 1
        # Slowing down
        if self.dis2nextCar_val <= self.speed:
            self.speed = self.dis2nextCar_val - 1
        # Randomization
        if random.random() <= p:
            # should not have negative speed
            if self.speed >0:
                self.speed = self.speed - 1
        # Car motion
        self.position = (self.position + self.speed) % self.numR

# road blocks
numR = 100

# cars
numC = 9

# road init condition
cars = [Car]*numC
#cars[0] = Car(4,30,numR)
#cars[1] = Car(5,80,numR)
#cars[2] = Car(5,99,numR)

cars[0] = Car(4,10,numR)
cars[1] = Car(5,20,numR)
cars[2] = Car(5,26,numR)
cars[3] = Car(5,30,numR)
cars[4] = Car(0,50,numR)
cars[5] = Car(0,51,numR)
cars[6] = Car(1,53,numR)
cars[7] = Car(4,70,numR)
cars[8] = Car(5,99,numR)




# random param
p = 0.6
maxIter = 20

for iter in range(0, maxIter):
    for car in cars:
        # for each car
        car.carActionRules()        
    printRoad(cars)
