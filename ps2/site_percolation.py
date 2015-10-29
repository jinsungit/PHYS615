"""
    Site Percolation
    Jin Sun
    PHYS615, Problem Set 2
"""
import random
import sys
import math

######
# helper functions

# convert linear index to subscript index, assume row based.
def ind2sub(ind, width):
    ri = int(ind/width)
    ci = ind % width
    return ri,ci
# convert subscript index to linear index, assume row based.
def sub2ind(ri, ci, width):
    return ri*width + ci

# relabel cluster
def relabelG(G, ri, ci, targetLabel, replacementLabel):
    if G[ri][ci] == targetLabel:
        G[ri][ci] = replacementLabel
        if ri-1 >= 0:
            relabelG(G, ri-1, ci, targetLabel, replacementLabel)
        if ri+1 <= len(G)-1:# number of rows
            relabelG(G, ri+1, ci, targetLabel, replacementLabel)
        if ci-1 >=0:
            relabelG(G, ri, ci-1, targetLabel, replacementLabel)
        if ci+1 <= len(G[0])-1:# number of cols
            relabelG(G, ri, ci+1, targetLabel, replacementLabel)

# print grid
def printGrid(G):
    print '====================='
    for i in range(height):
        outstr = ""
        for j in range(width):
            if G[i][j]<10 and G[i][j]>-1:
                Gstr = "0"
            else:
                Gstr = ""
            outstr = outstr + Gstr + str(G[i][j]) + " "
        print outstr

######
# main procedure

# a square grid
N = 25

width = int(math.sqrt(N))
height = width

#grid, contains cluster label, init to be all empty
G = [[-1 for i in range(width)] for j in range(height)]


# size array
G_size = [0]*N

# need an ordering of filling sites

# random permutation
siteOrder = range(N)
random.shuffle(siteOrder)

siteOrder = [0, 14, 15, 16, 9, 3, 23, 13, 10, 1, 5, 19, 2, 18, 11, 8, 6, 7, 20, 17, 12, 4, 21, 22, 24]


print "Site order is:"
print siteOrder

# adding sites one by one
for i in range(N):
    printGrid(G)
    # get site index
    siteIdx = siteOrder[i]
    # convert to sub
    ri,ci = ind2sub(siteIdx, width)
    
    print "Inserting " + str(siteIdx) + " at [" + str(ri) + "," + str(ci) + "]"
    
    G[ri][ci] = siteIdx
    G_size[G[ri][ci]] = 1 # each new site is of its own cluster with size 1

    # check if any of four neibhors sites already occupied, if so, add a bond between them. Repeat procedure in bond percolation.
    neighbors = [[ri-1,ci],[ri+1,ci],[ri,ci-1],[ri,ci+1]]
    ri_start = ri
    ci_start = ci

    for ni in range(len(neighbors)):
        if neighbors[ni][0] >=0 and neighbors[ni][0] <height and neighbors[ni][1] >=0 and neighbors[ni][1] <width:
            ri_end = neighbors[ni][0]
            ci_end = neighbors[ni][1]
            # if bond connects two real clusters
            if G[ri_start][ci_start] != G[ri_end][ci_end] and G[ri_end][ci_end] != -1:
                # relabel the smaller cluster
                if G_size[G[ri_start][ci_start]] < G_size[G[ri_end][ci_end]]:
                    print "G_size[G["+str(ri_start)+"]["+str(ci_start)+"] < G_size[G["+str(ri_end)+"]["+str(ci_end)+"]]: "+str(G_size[G[ri_start][ci_start]])+" vs "+str(G_size[G[ri_end][ci_end]])
                    oldLabel = G[ri_start][ci_start]
                    newLabel = G[ri_end][ci_end]
                    relabelG(G, ri_start, ci_start, oldLabel, newLabel)
                else:
                    print "G_size[G["+str(ri_start)+"]["+str(ci_start)+"] >= G_size[G["+str(ri_end)+"]["+str(ci_end)+"]]: "+str(G_size[G[ri_start][ci_start]])+" vs "+str(G_size[G[ri_end][ci_end]])
                    oldLabel = G[ri_end][ci_end]
                    newLabel = G[ri_start][ci_start]
                    relabelG(G, ri_end, ci_end, oldLabel, newLabel)
                
                G_size[newLabel] = G_size[newLabel] + G_size[oldLabel]
                G_size[oldLabel] = 0
printGrid(G)
