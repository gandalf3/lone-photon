from bge import logic, types
import utils

class Sentry(types.KX_GameObject):
    
    def __init__(self, own):
        self.cont = self.controllers[0]
#        scene = logic.getCurrentScene()
        
        self.target = self.scene.objects["player"]
        
        self.fireRate = .1
        self.range = 8
        
        if not self.get("projectile", 0):
            self.projectile_type = "standard_projectile"
        else:
            self.projectile_type = self["projectile"]
            
        print(self.name, "using", self.projectile_type)
        
        self.firenow = 0
        
        
        
    def aim(self):
        
        hit = self.rayCast(self.target, self, 0.0, "solid", 0, 1, 0)
        if hit[0] == self.target:
            self["cansee"] = True
            self.alignAxisToVect(hit[2], 0, 1)
        else:
            self["cansee"] = False
            
        return 
            
            
        
    def fire(self):
        
        print("pow")
        projectile = self.scene.addObject(self.projectile_type, self, 0)
        projectile.worldOrientation = self.worldOrientation
        projectile.setLinearVelocity((-20, 0, 0), True)
        
        self.firenow = 0
        
        
        
    def main(self):
        self.aim()
        
        print(self.firenow*logic.getTimeScale())
        if self.firenow*logic.getTimeScale() >= 1:
            self.fire()

        self.firenow += 1*self.fireRate
        
        
        
class Projectile(types.KX_GameObject):
    
    light_source = "standard_projectile_lamp"
    
    def __init__(self, own):
        self.cont = self.controllers[0]
        
        self.light = self.scene.addObject(light_source)
        self.light.setParent(self,0,0)
        
        