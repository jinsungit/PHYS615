"""
    Calculate edge betweenness
    Jin Sun
"""

import random
import sys


# function to calculate edge betweenness, from a selected root
# edges: network stored in edge list format
# r:     root node 
def calBetweenness(edges, r):
    N = len(edges)
    d = [-1]*N # all nodes are unassigned by default
    d[r] = 0 # init root node to have distance 0
    Q = [r] # a queue, initially only contains r
    Np = [0]*N # number of geodesic paths
    Np[r] = 1
    parents = {} # list of parents
    for n in range(N):
        parents[n] = []

    # for each element in Q
    while len(Q)>0:
        u = Q.pop(0) # get first element
        # for each vertex reachable by u
        for v in edges[u]:
            # if the node is unassigned
            if d[v] == -1:
                # assign v's distance
                d[v] = d[u]+1
                # u is parent of v
                parents[v].append(u)
                # add v to the end of Q
                Q.append(v)
                Np[v] = Np[u]
            else:
                if d[v] == d[u]+1:
                    # if the node is already assigned
                    parents[v].append(u)
                    Np[v] = Np[v] + Np[u]
    
    return Np, parents, d

