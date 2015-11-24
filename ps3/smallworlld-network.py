"""
    Small world networks
    Jin Sun
    PHYS615, Problem Set 3
"""
import random
import sys
import math
import numpy

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

# edge list to affinity matrix
def edges2affinity(edges):
    N = len(edges)
    A = [[0 for x in range(N)] for x in range(N)]
    for n in range(N):
        for e in edges[n]:
            if e!= -1:
                A[n][e] = 1
                A[e][n] = 1
    return A

######
# main procedure

# number of nodes
N = 500
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


# rewiring probability
p = 0.1
print('rewiring probability: ' + str(p))

# store short cut edges that has been rewired
shortCutEdges = [[0 for x in range(N)] for x in range(N)]
shortCutCounts = 0

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
                    # need to change current node n's edge list
                    edges[n][e] = newnode
                    # and newnode's edge list
                    edges[newnode].append(n)
                    # also need to change oldnode's edge list
                    edges[oldnode][e+2] = -1
                    
                    validRewiring = True
                    shortCutEdges[n][newnode] = 1
                    shortCutEdges[newnode][n] = 1
                    shortCutCounts = shortCutCounts + 1
                    
    
# visGraph(edges, N)

bl = cb.calBetweenness(edges)
A = edges2affinity(edges)

print('total number of short cuts: '+str(shortCutCounts))

# calculate avg betweenness of short cut and non short cut edges
# only check one edge once
B_shortcut = []
B_nonshortcut = []
for i in range(N):
    for j in range(i+1,N):
        # if there is a valid edge
        if A[i][j] == 1:
            if shortCutEdges[i][j] == 1:
                B_shortcut.append(bl[i][j])
            else:
                B_nonshortcut.append(bl[i][j])


avgB = numpy.array([B_shortcut])
avgB_mean = numpy.mean(avgB)
avgB_std  = numpy.std(avgB, ddof=1)
print('avg betweenness of short-cut edges: ' + str(avgB_mean) + ' +- ' + str(
    avgB_std) + ', from ' + str(len(B_shortcut)) + ' edges.')


avgB = numpy.array([B_nonshortcut])
avgB_mean = numpy.mean(avgB)
avgB_std  = numpy.std(avgB, ddof=1)
print('avg betweenness of non-short-cut edges:' + str(avgB_mean) + ' +- ' +
      str(avgB_std) + ', from ' + str(len(B_nonshortcut)) + ' edges. ')

avgB_f = open('avgB_shortcut.txt','w')
for b in B_shortcut:
    avgB_f.write(str(b)+' ')
avgB_f.write('\n')
avgB_f.close()

avgB_f = open('avgB_nonshortcut.txt','w')
for b in B_nonshortcut:
    avgB_f.write(str(b)+' ')
avgB_f.write('\n')
avgB_f.close()



print "All done"
