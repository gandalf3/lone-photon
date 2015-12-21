from bge import logic, types
import aud
import random
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
        
        self.mparts = []
        
        for child in self.children:
            if "firepoint" in child.name:
                self.firepoint = child
            if "mpart" in child.name:
                self.mparts.append(child)
            
        
        
        
    def aim(self):
        
        hit = self.rayCast(self.target, self, 0.0, "solid", 0, 1, 0)
        if hit[0] == self.target:
            self["cansee"] = True
            self.alignAxisToVect(hit[2], 0, 1)
        else:
            self["cansee"] = False
            
        return self["cansee"]
            
            
        
    def fire(self):
        
        projectile = self.scene.addObject(self.projectile_type, self.firepoint, 0)
        projectile.worldOrientation = self.worldOrientation
        
        for part in self.mparts:
            part.playAction(name="sentry", start_frame=1, end_frame=4)
        
        self.firenow = 0
        
        
        
    def main(self):
        aim = self.aim()
     
        if self.firenow > 1 and aim:
            self.fire()

        self.firenow += 1*self.fireRate*logic.getTimeScale()

        
        
class Projectile(types.KX_GameObject):
    
    
    def __init__(self, own, sound):
        
        self.sound = sound

        self.speed = -30
        self.homing_factor = 0
        
        self.light_source = "standard_projectile_lamp"        
        
#        self.light = self.scene.addObject(self.light_source)
        
        self.sound_handler = aud.device().play(self.sound)
#        self.setLinearVelocity((self.speed, 0, 0), True)
        
    def main(self):

        self.setLinearVelocity((self.speed, 0, 0), True)
        
        #self.light.worldPosition = self.worldPosition

        print(utils.map_range(logic.getTimeScale() + utils.map_range(random.random(), to_min=-.1, to_max=.1), .05, 1, .2, 1))
        if self.sound_handler:

            self.sound_handler.pitch = utils.map_range(logic.getTimeScale() + utils.map_range(random.random(), to_min=-.1, to_max=.1), .05, 1, .2, 1)
            print(self.sound_handler.pitch)
        