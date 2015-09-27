"""
    One dimensional Cellular Automata
    Jin Sun
    for PHYS615
    Problem Set 1
"""

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
    


# cell array
num_c = 71 # make an odd number so there exists a middle point
C = [0]*num_c # init cell array

# initial condition
C[(num_c-1)/2] = 1 # middle point is 1, others are 0, consistent with lecture slides

# get rules
cur_rule = rules[which_rule]
printRule(cur_rule)

print "Start Cellular Automata simulation..."

# apply rule to cell array
for iter in range(1,200000):
    printCellArray(C)
    newC = list(C)
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



#i = len(l) - 1
#jIndex = (i - 1) % len(l)
#kIndex = (i + 1) % len(l)

#j = l[jIndex]
#k = l[kIndex]

