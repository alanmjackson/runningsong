import unittest

from runnetwork import *

class Test(unittest.TestCase):

    def test_network_exist(self):
        self.assertTrue(len(NETWORK) > 0)

    
    def test_areConnected(self):
        self.assertTrue(areConnected('v1', 'v2'))
        self.assertTrue(areConnected('v2', 'v1'))
        self.assertTrue(areConnected('v61', 'v126'))
        self.assertTrue(areConnected('v1', 'v3') == False)

    def text_network_length(self):
        self.assertTrue(network_length(arcs) > 0)

    

    def test_findArcs(self):
        
        graph = [
            Arc('a1', 100, 'v1', 'v2',   0, 180),
            Arc('a2', 100, 'v1', 'v2', 315, 225),
            Arc('a3', 100, 'v1', 'v2',  45, 135),
            Arc('a4', 100, 'v2', 'v3',   0, 180)
        ]

        expected_arcs = [
            Arc('a1', 100, 'v1', 'v2',   0, 180),
            Arc('a2', 100, 'v1', 'v2', 315, 225),
            Arc('a3', 100, 'v1', 'v2',  45, 135)        
        ]
    
        self.assertTrue(findArcs('v1', 'v2', graph) == expected_arcs)
    
    
    
    def test_pathLength(self):
    
        # an arc is: arc_name, distance, vertex1, vertex2, angle1, angle2, waypoints
        path = Path('v1', 'v4',
            [
                Arc('a1', 100, 'v1', 'v2', 0, 180),
                Arc('a2', 220, 'v2', 'v3', 0, 180),
                Arc('a3', 370, 'v3', 'v4', 0, 180)
            ])
        
        self.assertTrue(path.distance == 690)


    def test_arcsEquall(self):
    
        arc1 = Arc('a1', 100, 'v1', 'v2',   0, 180)
        arc2 = Arc('a1', 100, 'v1', 'v2',   0, 180)
        arc3 = Arc('a1', 100, 'v1', 'v2',   0, 0)
        
        self.assertTrue(arc1 == arc2)
        self.assertTrue(arc1 != arc3)        
        

    def test_pathsEquall(self):

        path1 = Path('v1', 'v3',
            [
                Arc('a1', 100, 'v1', 'v2', 0, 180),
                Arc('a2', 220, 'v2', 'v3', 0, 180)
            ])
            

        path2 = Path('v1', 'v3',
            [
                Arc('a1', 100, 'v1', 'v2', 0, 180),
                Arc('a2', 220, 'v2', 'v3', 0, 180)
            ])
            
        
        path3 = Path('v1', 'v3',
            [
                Arc('a1', 100, 'v1', 'v2', 0, 180),
                Arc('a2', 220, 'v2', 'v4', 90, 270)
            ])
        
        self.assertTrue(path1 == path2)
        self.assertTrue(path1 != path3)
        

    def test_findPaths(self):
        """
        
        v1---a1---v2---a2---v3
                  |         |
                  +----a3---+ 
        
        """
    
        network = [
            Arc('a1', 1, 'v1', 'v2', 90, 270),
            Arc('a2', 1, 'v2', 'v3', 90, 270),
            Arc('a3', 2, 'v2', 'v3', 180, 180)
        ]

        expected_path_1 = Path('v1', 'v3',
            [
                Arc('a1', 1, 'v1', 'v2', 90, 270),
                Arc('a2', 1, 'v2', 'v3', 90, 270)
            ])

        expected_path_2 = Path('v1', 'v3',
            [
                Arc('a1', 1, 'v1', 'v2', 90, 270),
                Arc('a3', 2, 'v2', 'v3', 180, 180)
            ])

        expected_paths = sorted([expected_path_1, expected_path_2])
        
        found_paths = sorted(findPaths('v1', 'v3', 2, 3, network))
        
        print 'expected_paths:'
        for path in expected_paths:
            print path.toString()
            
        print 'found_paths:'
        for path in found_paths:
            print path.toString()
        
        
        self.assertTrue(expected_paths == found_paths)


    #test that the correct relative angles are generated for the directions
    def test_simpleDirectionAngles(self):

        path = Path('v1', 'v4',
            [
                Arc('a1', 100, 'v1', 'v2', 0, 180),
                Arc('a2', 220, 'v2', 'v3', 90, 270),
                Arc('a3', 370, 'v3', 'v4', 315, 135)
            ])

        expected_directions = "v1 0:100m 90:220m 225:370m v4"
        
        #print "expected_directions", expected_directions
        #print "path directions:", path.directions
        
        self.assertTrue(path.directions == expected_directions)


    #testing directions for paths where the arcs are not straight so have 
    #non-reciprocal angles at the ends
    def test_nonReciprocalDirectionAngles(self):

        path = Path('v1', 'v4',
            [
                Arc('a1', 100, 'v1', 'v2', 0, 270),
                Arc('a2', 200, 'v2', 'v3', 0, 90),
                Arc('a3', 300, 'v3', 'v4', 180, 90)
            ])

        expected_directions = "v1 0:100m 270:200m 270:300m v4"
        
        print "expected_directions", expected_directions
        print "path directions:", path.directions
        
        self.assertTrue(path.directions == expected_directions)


    def test_getArcByName(self):
    
        #test getting an arc from the default network
        arc = get_arc_by_name('a132')
        
        self.assertTrue(arc.name == 'a132')
        self.assertTrue(arc.distance == 51)


        #test getting an arc from a passed network (list)
        network = [
            Arc('a1', 100, 'v1', 'v2', 90, 270),
            Arc('a2', 200, 'v2', 'v3', 90, 270),
            Arc('a3', 300, 'v2', 'v3', 180, 180)
        ]

        arc = get_arc_by_name('a1', network)
        
        self.assertTrue(arc.name == 'a1')
        self.assertTrue(arc.distance == 100)                
        
        

        

if __name__ == "__main__":
    unittest.main()

