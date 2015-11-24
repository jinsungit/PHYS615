"""
    Calculate edge betweenness
    Jin Sun
"""

import random
import sys


# function to perform BFS, from a selected root
# [INPUT]  edges: network stored in edge list format
#              r:     root node 
# [OUTPUT] Np, parents, d as in lecture example 
def bfs(edges, r):
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


# calculate betweenness
# [INPUT]   edges: network in edge list format
# [OUTPUT]     bl: betweenness for each edge, stored in NxN matrix
def calBetweenness(edges, whichr):
    N = len(edges)
    bl = [[0 for x in range(N)] for x in range(N)]
    # do bfs for every node
    #for r in range(N):
    for r in range(whichr):
        Np, parents, d = bfs(edges, r)
        Bk = [1]*N        # betweenness for each node

        # start from the node furthest from r
        sortedIdx = sorted(range(len(d)), key=lambda k: d[k]) 

        for ki in range(N-1,0,-1):
            k = sortedIdx[ki] # k is the current furthest node index
            # modify k's parents' Bk
            for p in parents[k]:
                amount = Bk[k] * Np[p]/(Np[k]*1.0)
                Bk[p] = Bk[p] + amount
                bl[k][p] = bl[k][p] + amount
                bl[p][k] = bl[p][k] + amount
    return bl



if False:
    # simple test
    edges = {}
    edges[0] = [1,2]
    edges[1] = [0,3]
    edges[2] = [0,3]
    edges[3] = [1,2,4]
    edges[4] = [3]

    Np,parents,d = bfs(edges,0)
    bl = calBetweenness(edges)
    print(bl)
