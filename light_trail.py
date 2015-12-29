from bge import logic, types
import bge
import collections
from mathutils import Vector
import utils

def sort_verts(k):
    
    if k['XYZ'][0] < 0:
        return k['XYZ'][1]+.0001
    else:
       return k['XYZ'][1]
    

class LightTrail(types.KX_GameObject):
    
    def __init__(self, own):

        self.guide = "player" # object to follow
        
        self.segment_length = 1 # number of logic ticks to wait between reading parent position
        self.segments = 30
        self.thickness_factor = .7
        
        self.age = 0
        self.past_locations = collections.deque(maxlen=self.segments)
        self.mesh_segments = []
        
        scene = logic.getCurrentScene()
        
        self.trailmesh = scene.addObject("trail")
        
        self.vertlist = []
        
        self.clear()
            
        for mesh in self.trailmesh.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, v_index)
                    
                    print(m_index, v_index, mesh.getVertex(m_index, v_index).getXYZ())
                    self.vertlist.append({"XYZ": vertex.XYZ.copy(), "index": v_index})
                        
        self.vertlist.sort(key=sort_verts, reverse=True)
#        for v in self.vertlist:
#            print(v['index'], v['XYZ'])

        
        self.tick_count=0
        self.verts = collections.deque(maxlen=self.segments*2)
        
    def clear(self):
        
        for i in range(self.segments):
            self.past_locations.append(logic.getCurrentScene().objects[self.guide].worldPosition - Vector((-i*.001,0,0)))
            
    def main(self):
        
        self.trailmesh.worldPosition = logic.getCurrentScene().objects[self.guide].worldPosition
        
        if self.tick_count*logic.getTimeScale() >= self.segment_length:
            g = logic.getCurrentScene().objects[self.guide]
            
            self.past_locations.append(g.worldPosition.copy())

            self.tick_count = 0
            
        
        for i in reversed(range(self.segments)):

            thickness = i/self.segments * self.thickness_factor

            if i-1 > 0:
                a = (self.past_locations[i] - self.past_locations[i-1]).lerp(self.past_locations[i] - self.past_locations[i], self.tick_count*logic.getTimeScale())
            else:
                a = self.past_locations[i] - self.trailmesh.worldPosition
                
            b = Vector((0, 0, 0))
            
            dir = b - a
            dir.normalize()

            perp = Vector((-dir.y, dir.x, 0))
            
            
            c = b - perp * (thickness/2)
            d = b + perp * (thickness/2)
            
            left = self.past_locations[i] - self.trailmesh.worldPosition + d
            right = self.past_locations[i] - self.trailmesh.worldPosition + c
            
            self.verts.append(right)
            self.verts.append(left)

        for mesh in self.trailmesh.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)):
                    vertex = mesh.getVertex(m_index, self.vertlist[v_index]['index'])
                    
                    if v_index <= len(self.verts):
                        vertex.XYZ = self.verts[v_index]
            
        self.tick_count += 1
        
    
def main(cont):
    own = cont.owner
    
    if not "init" in own:
        own["init"] = True
        own = LightTrail(own)
    
    own.main()
    
def clear(cont):
    own = cont.owner
    
    own.clear()