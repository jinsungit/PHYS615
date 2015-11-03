"""
    Self-organized Site Percolation
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

# fill a site with new cluster or spark
def fillSite(G, G_size, width, siteIdx, fillType):
    # convert to sub
    ri,ci = ind2sub(siteIdx, width)

    if fillType != "spark":# normal filling
        if verbose: print "Inserting " + str(siteIdx) + " at [" + str(ri) + "," + str(ci) + "]" 
        # if already occupied
        if G[ri][ci] != -1:
            if verbose: print "Already occupied, do nothing!"
            return "filling"
        G[ri][ci] = t
        G_size[t] = 1 # each new site is of its own cluster with size 1
    else:# filling with spark
        if verbose: print "Spark at [" +str(ri) + "," + str(ci) + "]"
        if G[ri][ci] == -1:
            if verbose: print "But hit an unoccupied site, nothing happend!"
            return "miss_hit"
        
    
    # check if any of four neibhors sites already occupied, if so, add a bond between them. Repeat procedure in bond percolation.
    neighbors = [[ri-1,ci],[ri+1,ci],[ri,ci-1],[ri,ci+1]]
    ri_start = ri
    ci_start = ci

    # if spark
    if fillType == "spark":
        oldLabel = G[ri_start][ci_start]
        newLabel = -1
        relabelG(G, ri_start, ci_start, oldLabel, newLabel)
        if verbose:     print "Burned down " + str(G_size[oldLabel]) + " sites."
        G_size[oldLabel] = 0 # all burned down
        return "hit"

    for ni in range(len(neighbors)):
        if neighbors[ni][0] >=0 and neighbors[ni][0] <height and neighbors[ni][1] >=0 and neighbors[ni][1] <width:
            ri_end = neighbors[ni][0]
            ci_end = neighbors[ni][1]
            
            # if bond connects two real clusters
            if fillType == "normal" and G[ri_start][ci_start] != G[ri_end][ci_end] and G[ri_end][ci_end] != -1:
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



######
# main procedure

# do we need visualization?
verbose = False
#verbose = True

# a square grid
N = 2500

width = int(math.sqrt(N))
height = width

#grid, contains cluster label, init to be all empty
G = [[-1 for i in range(width)] for j in range(height)]


# size hash table
# hash table is used because each time when we add a site, the site label is determined by time step
G_size = {}


# occupied density vs time
d_vs_t = []

# density vs time after one spark
d_vs_t_spark = []

# cluster size distribution of different occupation probability


t = 0
maxT = 20000
# adding sites by time step
while t < maxT:
    
    sparkValid = False
    
    if verbose:    printGrid(G)
    # randomly pick a site index
    siteIdx = random.randint(0, N-1)
    
    fillSite(G, G_size, width, siteIdx, "normal")

    if t % 100 == 0:
        # randomly pick a spark index
        siteIdx = random.randint(0, N-1)
        sparkRes = fillSite(G, G_size, width, siteIdx, "spark")
        if sparkRes == "hit":
            sparkValid = True


    # calculate density
    density = 0.0
    for g in G_size:
        if g != -1:
            density = density + G_size[g]
    d_vs_t.append(density/N)
    
    # if just hit a spark
    if sparkValid:  d_vs_t_spark.append(density/N)
    if verbose:     print "density: " + str(density/N)


    t = t+1
if verbose:     printGrid(G)

f = open("SOC_percolation_d_vs_t.txt",'w')
#f.write("Density vs time\n")
for item in d_vs_t:
    f.write(str(item)+" ")
f.write("\n")


f = open("SOC_percolation_d_vs_t_spark.txt",'w')
for item in d_vs_t_spark:
    f.write(str(item)+" ")
f.write("\n")

print "All done"
