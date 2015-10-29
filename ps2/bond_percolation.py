"""
    Bond Percolation
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
            if G[i][j]<10:
                Gstr = "0"
            else:
                Gstr = ""
            outstr = outstr + Gstr + str(G[i][j]) + " "
        print outstr

######
# main procedure


N = 25
# assume a square grid, number of bonds
M = 2*N - int(math.sqrt(N))*2

width = int(math.sqrt(N))
height = width

#grid, contains cluster label
G = [[0 for i in range(width)] for j in range(height)]
counter = 0
for i in range(width):
    for j in range(height):
        G[i][j] = counter
        counter = counter + 1

# size array
G_size = [1]*N

# need an ordering of bonds (edges)
# the order will be row based, horizontal first, vertical next
# horizontal bond first, total number is num_row * (num_col-1) 
# vertical bond next, total number is num_col * (num_row-1)

# random permutation
bondOrder = range(M)
random.shuffle(bondOrder)

print "Bond order is:"
print bondOrder

# adding bond one by one
for i in range(M):
    printGrid(G)
    # get bond index
    bondIdx = bondOrder[i]
    # convert to sub
    if bondIdx < height * (width-1):# horizontal bonds
        ri_start,ci_start = ind2sub(bondIdx, width-1)
        ri_end = ri_start
        ci_end = ci_start+1
    else:# vertical bonds
        ri_start,ci_start = ind2sub(bondIdx-height*(width-1), width)
        ri_end = ri_start+1
        ci_end = ci_start
     
    # check if two sites belong to the same cluster
    if G[ri_start][ci_start] != G[ri_end][ci_end]:
        # relabel the smaller cluster
        if G_size[G[ri_start][ci_start]] < G_size[G[ri_end][ci_end]]:
            #print "G_size[G["+str(ri_start)+"]["+str(ci_start)+"] < G_size[G["+str(ri_end)+"]["+str(ci_end)+"]]: "+str(G_size[G[ri_start][ci_start]])+" vs "+str(G_size[G[ri_end][ci_end]])
            oldLabel = G[ri_start][ci_start]
            newLabel = G[ri_end][ci_end]
            relabelG(G, ri_start, ci_start, oldLabel, newLabel)
        else:
            #print "G_size[G["+str(ri_start)+"]["+str(ci_start)+"] >= G_size[G["+str(ri_end)+"]["+str(ci_end)+"]]: "+str(G_size[G[ri_start][ci_start]])+" vs "+str(G_size[G[ri_end][ci_end]])
            oldLabel = G[ri_end][ci_end]
            newLabel = G[ri_start][ci_start]
            relabelG(G, ri_end, ci_end, oldLabel, newLabel)
        
        G_size[newLabel] = G_size[newLabel] + G_size[oldLabel]
        G_size[oldLabel] = 0

