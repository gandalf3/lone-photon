from bge import logic, types
import bge
import collections
from mathutils import Vector
import utils



class LightTrail(types.KX_GameObject):
    
    def __init__(self, own):

        self.guide = "player" # object to follow
        
        self.segment_length = 1 # number of logic ticks to wait between reading parent position
        self.segments = 30
        
        self.age = 0
        self.past_locations = collections.deque(maxlen=self.segments)
        self.mesh_segments = []
        
        scene = logic.getCurrentScene()

        for i in range(self.segments):
            self.past_locations.append(scene.objects[self.guide].worldPosition)
#        for i in range(self.segments/2):
            self.mesh_segments.append(LightTrailSegment(scene.addObject("trail_segment")))
        
        self.tick_count=0
            
    def main(self):
        
        if self.tick_count*logic.getTimeScale() >= self.segment_length:
            
            g = logic.getCurrentScene().objects[self.guide]

            self.past_locations.append(g.worldPosition.copy())

            self.tick_count = 0
            
        
        for i in range(self.segments):
            #self.mesh_segments[i].worldPosition = self.past_locations[i]
            #self.mesh_segments[i].worldOrientation = (0, 0, 0)

            if i-1 > 0:
                #[(.1,.1,0), (-.1,.1,0), (-.1,-.1,0), (.1,-.1,0)]
                thickness = .2
                
                a = (self.past_locations[i] - self.past_locations[i-1])
                b = Vector((0, 0, 0))
                
                dir = b - a
                dir.normalize()

                perp = Vector((-dir.y, dir.x, 0))
                
                
                c = b - perp * (thickness/2)
                d = b + perp * (thickness/2)
                
                e = a + perp * (thickness/2)
                f = a - perp * (thickness/2)
                
                top_right = c
                top_left = d
                bottom_left = e
                bottom_right = f
                
                bge.render.drawLine(self.past_locations[i], self.past_locations[i] - (self.past_locations[i] - self.past_locations[i-1]), (1,1,1))
                
                verts = [top_right, top_left, bottom_left, bottom_right]
                
#                for n in range(len(verts)-1):
#                    bge.render.drawLine(self.past_locations[i] + verts[n], self.past_locations[i] + verts[n+1], (1,1,1))
#                bge.render.drawLine(self.past_locations[i] + verts[0], self.past_locations[i] + verts[3], (1,1,1))
                
#                self.mesh_segments[i].verts = verts
                
#                self.mesh_segments[i].update()
            
        bge.render.drawLine(self.past_locations[1], \
            Vector(self.past_locations[1]).lerp(Vector(self.past_locations[0]), \
            1 - (self.tick_count*logic.getTimeScale()/self.segment_length)), (.8,.9,1))
            
        self.tick_count += 1

class LightTrailSegment(types.KX_GameObject):
    
    def __init__(self, own):
        self.verts = []
        
    def update(self):
        
        for mesh in self.meshes:
           for m_index in range(len(mesh.materials)):
              for v_index in range(mesh.getVertexArrayLength(m_index)):
                 vertex = mesh.getVertex(m_index, v_index)
                 vertex.XYZ = (self.verts[v_index])
    
def main(cont):
    own = cont.owner
    
    if not "init" in own:
        own["init"] = True
        own = LightTrail(own)
    
    own.main()