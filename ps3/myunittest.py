import unittest

import calBetweenness as cb
# build network example used in lecture 
def network_lecture():
    edges = {}
    edges[0] = [1,2]
    edges[1] = [0,3]
    edges[2] = [0,3]
    edges[3] = [1,2,4]
    edges[4] = [3]
    return edges

# a slightly different version
def network_lecture_variant():
    edges = {}
    edges[0] = [1,2]
    edges[1] = [0,3]
    edges[2] = [0,5]
    edges[3] = [1,4,5]
    edges[4] = [3]
    edges[5] = [2,3]
    return edges


class mytests(unittest.TestCase):
    # unit test on cb.bfs
    def test_bfs(self):
        ####
        # test lecture example
        edges = network_lecture()

        # test on node 0
        Np, parents, d = cb.bfs(edges, 0)
        
        self.assertEqual(Np, [1,1,1,2,2])
        self.assertEqual(parents, {0: [], 1: [0], 2: [0], 3: [1,2], 4: [3]})
        self.assertEqual(d, [0,1,1,2,3])
        
        # test on node 1
        Np, parents, d = cb.bfs(edges, 1)

        self.assertEqual(Np, [1,1,2,1,1])
        self.assertEqual(parents, {0: [1], 1: [], 2: [0,3], 3: [1], 4: [3]})
        self.assertEqual(d, [1,0,2,1,2])

        # test on node 3
        Np, parents, d = cb.bfs(edges, 3)

        self.assertEqual(Np, [2,1,1,1,1])
        self.assertEqual(parents, {0: [1,2], 1: [3], 2: [3], 3: [], 4: [3]})
        self.assertEqual(d, [2,1,1,0,1])

        ####
        # test variant network example
        edges = network_lecture_variant()

        # test on node 0
        Np, parents, d = cb.bfs(edges, 0)
        
        self.assertEqual(Np, [1,1,1,1,1,1])
        self.assertEqual(parents, {0: [], 1: [0], 2: [0], 3: [1], 4: [3], 5: [2]})
        self.assertEqual(d, [0,1,1,2,3,2])
        
    
    #unit test on calculate betweenness
    def test_calBetweenness(self):
        #test on lecture example
        edges = network_lecture()
        bl = cb.calBetweenness(edges,1)
        
        self.assertEqual(bl, [[0,2,2,0,0],[2,0,0,1,0],[2,0,0,1,0],[0,1,1,0,1],[0,0,0,1,0]])

        bl = cb.calBetweenness(edges,2)

        #self.assertEqual(bl, [[0,1.5,0.5,0,0],[1.5,0,0,2.5,0],[0.5,0,0,0.5,0],[0,2.5,0.5,0,1],[0,0,0,1,0]])
        self.assertEqual(bl, [[0,3.5,2.5,0,0],[3.5,0,0,3.5,0],[2.5,0,0,1.5,0],[0,3.5,1.5,0,2],[0,0,0,2,0]])


edges = network_lecture()
for i in range(5):
    Np, parents, d = cb.bfs(edges, i)
    print('........  r = ' + str(i) + '  .........') 
    print('Np:')
    print(Np)
    print('parents:')
    print(parents)
    print('d:')
    print(d)

suite = unittest.TestLoader().loadTestsFromTestCase(mytests)
unittest.TextTestRunner(verbosity=2).run(suite)
