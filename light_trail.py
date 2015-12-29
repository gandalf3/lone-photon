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
        self.thickness_factor = .9
        
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
#                    print(v_index)
                    self.vertlist.append({"XYZ": vertex.XYZ.copy(), "index": v_index})
                        
        self.vertlist.sort(key=sort_verts, reverse=True)

        
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

            thickness = utils.clamp(i/self.segments * self.thickness_factor, .4, 1)
            target_thickness = utils.clamp((i-1)/self.segments * self.thickness_factor, .4, 1)

            
            tan = self.past_locations[i] - self.past_locations[i-1] if i-1>=0 else self.trailmesh.worldPosition
            target_tan = self.past_locations[i-1 if i-1>=0 else 0] - self.past_locations[i-2 if i-2>=0 else 0]
            
            a = tan.lerp(target_tan, self.tick_count * logic.getTimeScale())                
            b = Vector((0, 0, 0))
            
            dir = b - a
            dir.normalize()

            perp = Vector((-dir.y, dir.x, 0))
            
            
            c = b - perp * (utils.lerp(thickness, target_thickness, self.tick_count*logic.getTimeScale()) /2)
            d = b + perp * (utils.lerp(thickness, target_thickness, self.tick_count*logic.getTimeScale()) /2)
            
            
            interpolated_segment_pos = self.past_locations[i].lerp(self.past_locations[i+1] if i+1<len(self.past_locations) else self.trailmesh.worldPosition, self.tick_count*logic.getTimeScale())
            
            left = interpolated_segment_pos - self.trailmesh.worldPosition + d
            right = interpolated_segment_pos - self.trailmesh.worldPosition + c
            
            self.verts.append(right)
            self.verts.append(left)

        for mesh in self.trailmesh.meshes:
            for m_index in range(len(mesh.materials)):
                for v_index in range(mesh.getVertexArrayLength(m_index)-1):
                    vertex = mesh.getVertex(m_index, self.vertlist[v_index]['index'])
                    vertex2 = mesh.getVertex(m_index, self.vertlist[v_index+1]['index'])
                    
                    
                    vertex.XYZ = self.verts[v_index]
                    vertex2.XYZ = self.verts[v_index+1]
#                    if v_index == 58:
#                        vertex.XYZ = (0,5,0)
                        
#                    bge.render.drawLine(self.trailmesh.worldPosition + vertex.XYZ, self.trailmesh.worldPosition + vertex2.XYZ, (v_index/self.segments,1,1))
            
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