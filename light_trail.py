from bge import logic, types
import bge
import collections
from mathutils import Vector
import utils

def sort_verts(k):
    
    if k['XYZ'][0] < 0:
        return k['XYZ'][1]+.001
    else:
       return k['XYZ'][1]
    

class LightTrail(types.KX_GameObject):
    
    def __init__(self, own):

        self.guide = "player" # object to follow
        
        self.segment_length = 0 # number of logic ticks to wait between reading parent position
        self.segments = 30
        
        self.age = 0
        self.past_locations = collections.deque(maxlen=self.segments)
        self.mesh_segments = []
        
        scene = logic.getCurrentScene()
        
        self.trailmesh = scene.addObject("trail")
        
        self.vertlist = []
        
        for i in range(self.segments):
            self.past_locations.append(scene.objects[self.guide].worldPosition)
            
        for mesh in self.trailmesh.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, v_index)
                    
                    self.vertlist.append({"XYZ": vertex.XYZ, "index": v_index})
                        
        self.vertlist.sort(key=sort_verts, reverse=True)
        for v in self.vertlist:
            print(v['index'], v['XYZ'])

        
        self.tick_count=0
        self.verts = collections.deque(maxlen=self.segments*2)
            
    def main(self):
        
        self.trailmesh.worldPosition = logic.getCurrentScene().objects[self.guide].worldPosition
        
        if self.tick_count*logic.getTimeScale() >= self.segment_length:
            
            g = logic.getCurrentScene().objects[self.guide]

            self.past_locations.append(g.worldPosition.copy())

            self.tick_count = 0
            
        
        for i in reversed(range(self.segments)):

            
#                [(.1,.1,0), (-.1,.1,0), (-.1,-.1,0), (.1,-.1,0)]
            thickness = i/self.segments * .5

            if i-1 > 0:
                a = self.past_locations[i] - self.past_locations[i-1]
            else:
                a = self.past_locations[i] - self.trailmesh.worldPosition
            b = Vector((0, 0, 0))
            
            dir = b - a
            dir.normalize()

            perp = Vector((-dir.y, dir.x, 0))
            
            
            c = b - perp * (thickness/2)
            d = b + perp * (thickness/2)
            
#            e = a + perp * (thickness/2)
#            f = a - perp * (thickness/2)
            
            left = self.past_locations[i] - self.trailmesh.worldPosition + d
            right = self.past_locations[i] - self.trailmesh.worldPosition + c

#            left = d
#            right = c
            
            if i%2:
                self.verts.append(right)
                self.verts.append(left)
#            self.verts.append(d)
#            self.verts.append(c)
            #print("count", i, len(self.verts))
          #  bge.render.drawLine(right, left, (1,1,1))
               
                
#        for n in range(len(self.verts)-1):
#            bge.render.drawLine(self.past_locations[i] + self.verts[n], self.past_locations[i] + self.verts[n+1], (1,1,1))
                
        #verts = [(.1,-.1,0), (-.1,-.1,0), (.1,0,0), (-.1,0,0), (.1,.1,0), (-.1,.1,0)]
        for mesh in self.trailmesh.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, self.vertlist[v_index]['index'])
                    #vertex2 = mesh.getVertex(m_index, v_index)
                    
                    if v_index <= len(self.verts):
#                        print(v_index, verts[v_index], self.vertlist[v_index]['index'], vertex.XYZ)
#                       print(v_index, self.vertlist[v_index+2]['index'])
#                        vertex.XYZ = self.verts[self.vertlist[v_index]['index']]
                        vertex.XYZ = self.verts[v_index]
#                        print(self.verts[v_index], vertex.XYZ)
#                        vertex.setNormal(Vector((0,0,-1)))
                        #print(vertex.normal)
                        
#                       vertex2.XYZ = self.verts[self.vertlist[v_index+2]['index']]
#                        print(self.verts[self.vertlist[v_index]['index']], self.verts[self.vertlist[v_index+1]['index']])
                        #if v_index < 4:
                        bge.render.drawLine((0,0,0), vertex.XYZ, (1,1,1))

            
        bge.render.drawLine(self.past_locations[1], \
            Vector(self.past_locations[1]).lerp(Vector(self.past_locations[0]), \
            1 - (self.tick_count*logic.getTimeScale()/self.segment_length)), (.8,.9,1))
            
        self.tick_count += 1
        
    
def main(cont):
    own = cont.owner
    
    if not "init" in own:
        own["init"] = True
        own = LightTrail(own)
    
    own.main()