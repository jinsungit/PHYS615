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

# do we need visualization?
verbose = False


# a square grid
N = 2500

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

if verbose:
    print "Site order is:"
    print siteOrder

# size of largest component vs occupation probability
lc_vs_p = [0]*N

# cluster size distribution of different occupation probability
p02 = G_size[:]
p06 = G_size[:]
p09 = G_size[:]

# adding sites one by one
for i in range(N):
    if verbose:    printGrid(G)
    # get site index
    siteIdx = siteOrder[i]
    # convert to sub
    ri,ci = ind2sub(siteIdx, width)
    
    if verbose:     print "Inserting " + str(siteIdx) + " at [" + str(ri) + "," + str(ci) + "]"
    
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
                    if verbose:     print "G_size[G["+str(ri_start)+"]["+str(ci_start)+"] < G_size[G["+str(ri_end)+"]["+str(ci_end)+"]]: "+str(G_size[G[ri_start][ci_start]])+" vs "+str(G_size[G[ri_end][ci_end]])
                    oldLabel = G[ri_start][ci_start]
                    newLabel = G[ri_end][ci_end]
                    relabelG(G, ri_start, ci_start, oldLabel, newLabel)
                else:
                    if verbose:     print "G_size[G["+str(ri_start)+"]["+str(ci_start)+"] >= G_size[G["+str(ri_end)+"]["+str(ci_end)+"]]: "+str(G_size[G[ri_start][ci_start]])+" vs "+str(G_size[G[ri_end][ci_end]])
                    oldLabel = G[ri_end][ci_end]
                    newLabel = G[ri_start][ci_start]
                    relabelG(G, ri_end, ci_end, oldLabel, newLabel)
                
                G_size[newLabel] = G_size[newLabel] + G_size[oldLabel]
                G_size[oldLabel] = 0
    lc_vs_p[i] = max(G_size)

    if i==499:
        p02 = G_size[:]
    if i==1499:
        p06 = G_size[:]
    if i==2249:
        p09 = G_size[:]
if verbose:     printGrid(G)

f = open("site_percolation_result.txt",'w')
f.write("Largest component size vs occupation probability\n")
for item in lc_vs_p:
    f.write(str(item)+" ")
f.write("\n")

f.write("p = 0.2, cluster size distribution\n")
for item in p02:
    f.write(str(item)+" ")
f.write("\n")

f.write("p = 0.6, cluster size distribution\n")
for item in p06:
    f.write(str(item)+" ")
f.write("\n")

f.write("p = 0.9, cluster size distribution\n")
for item in p09:
    f.write(str(item)+" ")
f.write("\n")

f.close()

print "All done"
