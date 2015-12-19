import bge
import collections
import mathutils
import utils

tail_length=20
past_locations = collections.deque(maxlen=20)
for i in range(tail_length):
    past_locations.append((0,0,0))

    
def main(controller):
    own = controller.owner
    
    time_fac = own.get("do_update", 0)*bge.logic.getTimeScale()
        
    if time_fac >= 1:
        past_locations.append(own.worldPosition.copy())        
        
        own["do_update"] = 0
    #print(time_fac)
    bge.render.drawLine(past_locations[0], mathutils.Vector(past_locations[0]).lerp(mathutils.Vector(past_locations[1]), time_fac), (.8,.9,1))
#    for i in range(len(past_locations)-1):
#        bge.render.drawLine(past_locations[i], past_locations[i+1], (.8,.9,1))
            
    
    own["do_update"] = own.get("do_update", 0) + 1