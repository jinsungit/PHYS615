"""
    Small world networks
    Jin Sun
    PHYS615, Problem Set 3
"""
import random
import sys
import math
import calBetweenness as cb

######
# helper functions

def visGraph(edges, N):
    f_data = open("network.json",'w')
    f_data.write("{\n")

    # write node
    f_data.write("\"nodes\":[\n")
    for n in range(N):
        thestr = "{\"name\":\"" + str(n) + "\"}"
        if n != N-1:
            thestr = thestr + ","
        f_data.write(thestr+"\n")
    f_data.write("],\n")

    # write edges
    f_data.write("\"links\":[\n")
    for n in range(N):
        for j in edges[n]:
            thestr = "{\"source\":" + str(n) + ",\"target\":" + str(j) + ",\"value\":1}"
            if n != N-1 or j != edges[n][len(edges[n])-1]:
                thestr = thestr + ","
            f_data.write(thestr+"\n")
    f_data.write("]\n")
    f_data.write("}\n")
        

# find element in list, if not found return False
def inlist(thelist, element):
    for l in thelist:
        if l == element:
            return True
    return False



######
# main procedure

# number of nodes
N = 5
# store network in edge list
edges = {}
for n in range(N):
    edges[n] = []
    # connect two neighbors each side
    edges[n].append( (n+1) % N )
    edges[n].append( (n+2) % N )
    edges[n].append( (n-1) % N )
    edges[n].append( (n-2) % N )

# print edge list
#print(edges)

#visGraph(edges, N)

# calculate betweenness before rewiring
bl = cb.calBetweenness(edges)
print(bl)

# rewiring network

# rewiring probability
p = 0.1

# for each node
for n in range(N):
    # for each of its one side edges (2 edges):
    for e in range(2):
        # check rewiring probability
        if random.random() <= p:
            # rewiring!
            validRewiring = False
            oldnode = edges[n][e]
            while not validRewiring:
                # pick another node at uniform random
                newnode = random.randint(0, N-1)
                # make sure no duplicate edges
                if newnode != n and not inlist(edges[n], newnode):
                    edges[n][e] = newnode
                    # dont need to change oldnode's edge list, because we only do one side edges
                    validRewiring = True
                    
    
# visGraph(edges, N)

bl = cb.calBetweenness(edges)

print(bl)

print "All done"
