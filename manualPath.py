'''Manually create a path to recalculate the directions'''

from runnetwork import *


arcs = []
arcs.append(get_arc_by_name('a132'))
arcs.append(get_arc_by_name('a067'))
arcs.append(get_arc_by_name('a066'))
arcs.append(get_arc_by_name('a065')) 
arcs.append(get_arc_by_name('a062')) 
arcs.append(get_arc_by_name('a063')) 
arcs.append(get_arc_by_name('a152')) 
arcs.append(get_arc_by_name('a153')) 
arcs.append(get_arc_by_name('a223')) 
arcs.append(get_arc_by_name('a222')) 
arcs.append(get_arc_by_name('a221')) 
arcs.append(get_arc_by_name('a129'))
arcs.append(get_arc_by_name('a130')) 
arcs.append(get_arc_by_name('a097')) 
arcs.append(get_arc_by_name('a227')) 
arcs.append(get_arc_by_name('a096')) 
arcs.append(get_arc_by_name('a095')) 
arcs.append(get_arc_by_name('a144')) 
arcs.append(get_arc_by_name('a068')) 
arcs.append(get_arc_by_name('a223')) 
arcs.append(get_arc_by_name('a132'))

path = Path('v126', 'v126', arcs)

print path.directions
print path.directions_csv
print path.bearings_csv




