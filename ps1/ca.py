"""
    One dimensional Cellular Automata
    Jin Sun
    for PHYS615
    Problem Set 1
"""

import random
import sys

########
## Helper function
########

# print cell array in a nice form
def printCellArray(C):
    str = ""
    for c in C:
        if c == 1:
            str += "*"
        else:
            str += "."
    print str

# get n-bit string, source http://stackoverflow.com/questions/699866/python-int-to-binary
get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)

# print a single rule
def printRule(rule):
    print "CA rule:"
    for i in range(0,8):
        str = get_bin(7-i,3) + " -> " + rule[7-i]
        print str 

# calculate density of defects
# defects: two consecutive 1's
def calDensityDefects(C):
    defectsCount = 0.0
    for i in range(0,len(C)):
        if i == len(C)-1:
            nextCi = C[0]
        else:
            nextCi = C[i+1]
        if C[i]==1 and nextCi==1:
            defectsCount = defectsCount + 1
    return defectsCount/len(C)


##########

# arguments
print sys.argv
if len(sys.argv) == 1:
    which_rule = 18
else:
    which_rule = int(sys.argv[1])


# generate pool of rules
# Each rule is a dictionary (hash table) that maps neighborhood coding to 0/1
rules = {}
for rule_index in range(0, 256):
    rules[rule_index] = {}
    # convert rule number to 8-bit binary string. For 3 neighbors ca, all neighborhood configuration is 2^3 
    neighbors = get_bin(rule_index,8)
    for i in range(0,8):
        # each key to the rule is a decimal number converted from binary string
        rules[rule_index][7-i] = neighbors[i]
    


# Cell array
num_c = 771 # make an odd number so there exists a middle point
C = [0]*num_c # init cell array

# initial condition
random_C = True

if random_C:
    C = [int(random.random()+0.5) for i in range(num_c)]
else:
    C[(num_c-1)/2] = 1 # middle point is 1, others are 0, consistent with lecture slides


# get rules
cur_rule = rules[which_rule]
printRule(cur_rule)

print "Start Cellular Automata simulation..."
maxIter = 20
densityDefects = [0]*maxIter
# apply rule to cell array
for iter in range(0,maxIter):
    #printCellArray(C)
    newC = list(C)
    densityDefects[iter] = calDensityDefects(C)
    for cellIdx in range(0,num_c):
        # periodic boundary conditions
        if cellIdx == 0:
            leftCell = C[num_c-1]
        else:
            leftCell = C[cellIdx-1]

        if cellIdx == num_c-1:
            rightCell = C[0]
        else:
            rightCell = C[cellIdx+1]
        
        neighbors_str = str(leftCell) + str(C[cellIdx]) + str(rightCell)
        neighbors = int(neighbors_str,2)
        #print neighbors_str + ": " + str(neighbors)
        newC[cellIdx] = int(cur_rule[neighbors])
    C = list(newC)

print densityDefects

#i = len(l) - 1
#jIndex = (i - 1) % len(l)
#kIndex = (i + 1) % len(l)

#j = l[jIndex]
#k = l[kIndex]

