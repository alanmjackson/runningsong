"""
Loads in a path network from a CSV file and performs queries on it. 

Bramber = v1
Home = v126

"""

import random
from functools import total_ordering

network_file_name = 'Network.kml.csv'

DEFAULT_START = 'v126'
DEFAULT_END = 'v126'

@total_ordering
class Arc:
    
    def __init__(self, name, distance, v1, v2, angle1, angle2, waypoints=[]):
        self.name = name
        self.distance = distance
        self.vertex1 = v1
        self.vertex2 = v2
        self.angle1 = angle1
        self.angle2 = angle2
        self.waypoints = waypoints
        self.vertices = set([self.vertex1, self.vertex2])
        self.__hash = hash(self.name)

    def __eq__(self, other):
    
        endpoints_are_equal = (self.vertex1 == other.vertex1 and \
            self.angle1 == other.angle1 and \
            self.vertex2 == other.vertex2 and \
            self.angle2 == other.angle2) or \
            (self.vertex1 == other.vertex2 and \
            self.angle1 == other.angle2 and \
            self.vertex2 == other.vertex1 and \
            self.angle2 == other.angle1)
    
        is_equall = self.name == other.name and \
            self.distance == other.distance and \
            endpoints_are_equal and \
            self.waypoints == other.waypoints
        
        return is_equall
        

    def __ne__(self, other):
        equal = self.__eq__(other)
        return equal if equal is NotImplemented else not equal

        
    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        #just hashing on the name. Probably a bit hacky. 
        return self.__hash

    def otherVertex(self, vertex):
        """Return the vertex at the other end of the arc"""
        if self.vertex1 == vertex:
            return self.vertex2
        elif self.vertex2 == vertex:
            return self.vertex1
        else:
            return None
    
    def getAngle(self, vertex):
        """Return the angle for the given vertex"""
        if self.vertex1 == vertex:
            return self.angle1
        elif self.vertex2 == vertex:
            return self.angle2
        else:
            return None


    def toString(self):
        arc_string = self.name + ' '
        arc_string += str(self.distance) + ' '
        arc_string += self.vertex1  + ' '
        arc_string += self.vertex2 + ' '
        arc_string += str(self.angle1) + ' '
        arc_string += str(self.angle2)
        
        #ignore waypoints for now
        #self.waypoints 
        return arc_string


#Ingest the CSV file
network_file = open(network_file_name, 'r')


@total_ordering
class Path:

    def __init__(self, start_vertex, end_vertex, arcs):
        self.start = start_vertex
        self.end = end_vertex
        self.arcs = arcs

        #calculate the distance field        
        self.distance = 0
        for arc in self.arcs:
            self.distance += arc.distance
    

        #create the description string
        self.description = self.start + ' ' 
        for arc in self.arcs:
            self.description += arc.name + ' '
        self.description += self.end

        #create the directions string by traversing the path
        self.directions = self.start + ' '
        self.directions_csv = self.start + '\n'
        self.bearings = ''
        self.bearings_csv = ''
        
        last_bearing = 0     #start facing North
        vertex = self.start
        for arc in self.arcs:
            
            bearing = arc.getAngle(vertex)
            while bearing < 0:
                bearing += 360
                
            turn = arc.getAngle(vertex) - last_bearing
            while turn < 0:
                turn += 360
                
            
            self.directions += str(turn) + ':' + str(arc.distance) + 'm '
            self.directions_csv += str(turn) + ',' + str(arc.distance) + '\n'
            
            self.bearings += str(bearing) + ' '
            self.bearings_csv += str(bearing) + '\n'
            
            vertex = arc.otherVertex(vertex)
            last_bearing = reciprocal(arc.getAngle(vertex))

        self.directions += self.end
        self.directions_csv += self.end
    
    
    def toString(self):
        path_string = self.start + ' \n' 
        
        for arc in self.arcs:
            path_string += arc.toString()
            path_string += '\n'
            
        path_string += self.end
        
        return path_string
        
            
    def __eq__(self, other):
        vertices_are_equall = self.start == other.start and \
            self.end == other.end

        arcs_are_equall = True
        if len(self.arcs) == len(other.arcs):
            for i in range(len(self.arcs)):
                if self.arcs[i] != other.arcs[i]:
                    arcs_are_equall = False
        else:
            arcs_are_equall = False
            
        return vertices_are_equall and arcs_are_equall
        
        
    def __ne__(self, other):
        equal = self.__eq__(other)
        return equal if equal is NotImplemented else not equal
        
        
    def __lt__(self, other):
        if self.start != other.start:
            return self.start < other.start
        
        if self.end != other.end:
            return self.end < other.end
            
        if len(self.arcs) != len(other.arcs):
            return len(self.arcs) < len(other.arcs)
            
        for i in range(len(self.arcs)):
            if self.arcs[i] != other.arcs[i]:
                return self.arcs[i] < other.arcs[i]
        
        return False
            
        


# an arc is: arc_name, distance, vertex1, vertex2, angle1, angle2, waypoints

NETWORK = []
NETWORK_DICT = {}

for line in network_file:
    arc = []
    fields = line.split('\t')
    
    if fields[0] !='name':
    
        arc = Arc(
            fields[0],
            int(fields[1]),
            fields[2],
            fields[3],
            int(fields[4]),
            int(fields[5]),
            fields[6])
    
        NETWORK.append(arc)
        NETWORK_DICT[fields[0]] = arc

network_file.close()



VERTICES = []
for arc in NETWORK:
    VERTICES.append(arc.vertex1)
    VERTICES.append(arc.vertex2)

VERTICES = list(set(VERTICES))


#returns the reciprocal angle of the given angle
def reciprocal(angle):
    return (angle + 180) % 360


def get_arc_by_name(arc_name, network=NETWORK_DICT):
    if isinstance(network, dict):
        return network[arc_name]
    else:
        for arc in network:
            if arc.name == arc_name:
                return arc


def network_length(network=NETWORK):
	length = 0.0
	for arc in network:
		length += arc.distance

	return length


def areConnected(vertex1, vertex2, network=NETWORK):
    """ Returns true if vertex1 is connected directly to vertex2 by at least one arc. 
    """
    
    arcs = findArcs(vertex1, vertex2, network)
    return len(arcs) > 0



def findArcs(vertex1, vertex2, network=NETWORK):
    """ Returns all arcs that directly join vertex1 to vertex2
    """
    
    vertices = set([vertex1, vertex2])
    
    joining_arcs = []
    
    for arc in network:
        if vertices == arc.vertices:
            joining_arcs.append(arc)
    
    return joining_arcs        


def getAdjoiningArcs(vertex, network=NETWORK):
    arcs_from_vertex = []
    for arc in network:
        if vertex in arc.vertices:
            arcs_from_vertex.append(arc)
    
    return arcs_from_vertex


  

def findRandomPath(vertex1, vertex2, min_dist, max_dist, network=NETWORK):

    while True:
        next_vertex = vertex1        
        path_arcs = []
        print '\n=',
        while network_length(path_arcs) < max_dist:
        
            all_arcs_from_vertex = getAdjoiningArcs(next_vertex)
            
            next_arcs = []
            
            for arc in all_arcs_from_vertex:
                #guard against tight loops
                if not arc in path_arcs[-10:]:
                    next_arcs.append(arc)
                    
            if len(next_arcs) > 0:
                next_arc = random.choice(next_arcs)
            else:
                break

            path_arcs.append(next_arc)
            print '\n.',
            for arc in path_arcs:
                print arc.name, 

            next_vertex = next_arc.otherVertex(next_vertex)
            
            if next_vertex == vertex2:
                length = network_length(path_arcs)
                if length >= min_dist and length <= max_dist:
                    return Path(vertex1, vertex2, path_arcs)



def findPaths(vertex1, vertex2, min_dist, max_dist, network=NETWORK, arcs_so_far=[]):

    #you can reverse down a path you've just come up but you can't do the same
    #path twice in the same direction.  

    #print 'vertex1: ', vertex1, 'vertex2: ', vertex2, 'min: ', min_dist, 'max: ', max_dist

    paths = []
        
        
    #find all the arcs that start from v1
    arcs_from_v1 = []
    for arc in network:
        if vertex1 in arc.vertices and not arc in arcs_so_far:
            arcs_from_v1.append(arc)
    
    #print 'arcs from v1: ',  arcs_from_v1 
    
    for arc in arcs_from_v1:

        
        if vertex2 in arc.vertices:
            path = Path(vertex1, vertex2, [arc])
            if min_dist <= path.distance <= max_dist:
                arcs_so_far.append(arc)
                paths.append(path)


        else:
            #if the arc doesn't end at vertex2 then recurse...
            
            #get the vertex that is neither vertex1 or vertex2
            if arc.vertex1 == vertex1:
                end_vertex = arc.vertex2
            else:
                end_vertex = arc.vertex1
                
            tail_min = max(min_dist - arc.distance, 0)
            tail_max = max_dist - arc.distance
                
            if tail_max > 0:
                tail_paths = findPaths(
                    end_vertex, 
                    vertex2, 
                    tail_min, 
                    tail_max,  
                    network,
                    arcs_so_far + [arc])
                
                if len(tail_paths) > 0:
                    arcs_so_far.append(arc)
                
          
                for tail_path in tail_paths:
                    path = Path(vertex1, vertex2, list([arc] + tail_path.arcs))
                    paths.append(path)
                
                
    return paths
            
    

            

def printNetworkStats(network=NETWORK):
    print 'network contains ' + str(len(NETWORK)) + ' arcs and ' + str(len(VERTICES)) + ' vertices.'
    print 'network length: ' + str(network_length() / 1000) + 'km'



if __name__ == "__main__":
    print 'imported from ' + network_file_name
    printNetworkStats()

    start = raw_input('start vertex: [' + DEFAULT_START + ']' )
    if len(start) == 0:
        start = DEFAULT_START
        
    end = raw_input('end vertex: [' + DEFAULT_END + ']' )
    if len(end) == 0:
        end = DEFAULT_END
    
    min_dist_input = raw_input('minimum distance (km): [5]')
    if len(min_dist_input) == 0:
        min_dist = 5000
    else:
        min_dist = float(min_dist_input) * 1000.0
        
    max_dist_input = raw_input('maximum distance (km): [+10%]')
    if len(max_dist_input) == 0:
        max_dist = min_dist * 1.1
    else:    
        max_dist = float(max_dist_input) * 1000.0
        max_dist = max(max_dist, min_dist)

    path = findRandomPath(start, end, min_dist, max_dist)
    print '\n\n===================================================================\n'
    print 'distance (km): ', path.distance / 1000.0 
    print '\ndescription: '
    print path.description
    print '\ndirections: '
    print path.directions
    print '\ndetails: '
    print path.toString()


    if raw_input('save? (y/n): [n]') == 'y':
        filename = raw_input('file name:')
        fp = open(filename, 'w')
        fp.write(str(path.distance) + '\n\n')
        fp.write(path.description + '\n\n')
        fp.write(path.directions + '\n\n')
        fp.write(path.toString())
        fp.write('\n\n')
        fp.write(path.directions_csv)
        fp.close()




#    paths = findPaths('v1', 'v126', MIN, MAX)
#    for path in paths:
#        print path.description(), path.distance


    


