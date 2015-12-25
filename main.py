from bge import logic, events, types, render
import math, mathutils
import numpy
import aud
import random
import utils

#sound = aud.Factory.file(logic.expandPath("//sound/Adventure Meme.mp3")).volume(.1).loop(-1)
#sound = aud.Factory.file(logic.expandPath("//sound/Unwritten Return.mp3")).volume(1).loop(-1)
sound = aud.Factory.file(logic.expandPath("//sound/Destiny Day.mp3")).volume(1).loop(-1)
music = aud.device().play(sound)

dict = logic.globalDict
playername = "player"
scene = logic.getCurrentScene()

levels = ['level1', 'level2']
dict["current_level"] = 0

class Sentry(types.KX_GameObject):
    
    def __init__(self, own):
        self.cont = self.controllers[0]
        
        self.target = logic.getCurrentScene().objects[playername]
        
        self.fireRate = .1
        self.range = 8
        
        if not self.get("projectile", 0):
            self.projectile_type = "standard_projectile"
        else:
            self.projectile_type = self["projectile"]
            
        print(self.name, "using", self.projectile_type)
        
        self.firenow = random.random()
        
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
        
        projectile = logic.getCurrentScene().addObject(self.projectile_type, self.firepoint, 0)
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
        player = logic.getCurrentScene().objects[playername]
        
        self.sound = sound

        self.speed = -30
        self.homing_factor = 0
        
        self.collisionCallbacks.append(self.on_collision)
        
        self.sound_device = aud.device()
        self.sound_device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR
        self.sound_device.listener_location = player.worldPosition
        self.sound_device.listener_velocity = player.getLinearVelocity()
        self.sound_device.doppler_factor = 3
        
        self.sound_handle = self.sound_device.play(self.sound)
        self.sound_handle.relative = False
        self.sound_handle.location = self.worldPosition
        self.sound_handle.velocity = self.getLinearVelocity()
        self.sound_handle.distance_maximum = 100
        self.sound_handle.distance_reference = 1
        
        
    def on_collision(self, object, point, normal):
            
        if "solid" in object:
        
            # Flip sign of normal if collision with triangle mesh
            # to workaround this bug: https://developer.blender.org/T47036
            if "floor_triangle_mesh" in object.name:
                normal = normal*-1
                
            d = mathutils.Vector(self.getLinearVelocity())
            n = mathutils.Vector(normal)
            
#            d = d * d.dot(n)
            
            # determine reflection direction
            r = d - ((2 * d * n) / (n*n)) * n
                        
            vectsplosion = logic.getCurrentScene().addObject("vectsplosion")
            vectsplosion["point"] = point
            vectsplosion["direction"] = r
            vectsplosion["color"] = (1, 0, 0)
            
            if object == logic.getCurrentScene().objects[playername]:
                player_death()
            else:
                self.endObject()
            
        
    def main(self):
        
        self.setLinearVelocity((self.speed, 0, 0), True)

        if self.sound_handle:
            self.sound_handle.pitch = utils.map_range(logic.getTimeScale() + utils.map_range(random.random(), to_min=-.1, to_max=.1), .05, 1, .2, 1)

class Vectsplosion(types.KX_GameObject):
    
    def __init__(self, own):
        
        self.origin = mathutils.Vector(self["point"])
        self.direction = mathutils.Vector(self["direction"])
        self.rcolor = self["color"]

        self.time = 0
        self.lines = []

        for i in range(random.randrange(3, 5)):
            self.lines.append(self.origin + self.direction + mathutils.Vector(numpy.random.normal(0, 5, 3)))
        
    def main(self):
        
        for line in self.lines:
            render.drawLine(self.origin.lerp(line, utils.clamp(self.time*2-.5)), self.origin.lerp(line, self.time), self.rcolor)
            
        self.time += .1*logic.getTimeScale()

        if self.time >= 1:
            self.endObject()
        

class Player(types.KX_GameObject):
    
    keyboard = logic.keyboard
    
    def __init__(self, own):
        
        self.alive = True
        self.recouperating = False
        self.movement_speed = 20
        self.light = logic.getCurrentScene().objects["player_light"]

        self.counter = 1
        
        
    def movement(self, keyboard=keyboard):
        ACTIVE = logic.KX_INPUT_ACTIVE
    
        movement = self.getLinearVelocity()

        # forward
        if keyboard.events[events.WKEY] == ACTIVE:
            movement[1] = utils.clamp(movement[1] + self.movement_speed*.1, -self.movement_speed, self.movement_speed)
            
        # backward
        if keyboard.events[events.SKEY] == ACTIVE:
            movement[1] = utils.clamp(movement[1] + -self.movement_speed*.1, -self.movement_speed, self.movement_speed)
        
        # left
        if keyboard.events[events.AKEY] == ACTIVE:
            movement[0] = utils.clamp(movement[0] + -self.movement_speed*.1, -self.movement_speed, self.movement_speed)
            
        # right
        if keyboard.events[events.DKEY] == ACTIVE:
            movement[0] = utils.clamp(movement[0] + self.movement_speed*.1, -self.movement_speed, self.movement_speed)
                
        #self.setLinearVelocity(movement * ((logic.getTimeScale()-1)**4+1))
        self.setLinearVelocity(movement)
        
        # cosmetic spinny stuff
        if self.getAngularVelocity() < mathutils.Vector((1,1,1)):
            self.setAngularVelocity(numpy.random.normal(0, 5, 3))
            
    def main(self):
        
        if self.alive:
            velocity = self.getLinearVelocity()
            speed = utils.velocity2speed(velocity)
            timescale = utils.clamp((speed/self.movement_speed)**2, .05, 1)
            
            if timescale != logic.getTimeScale():
                logic.setTimeScale(timescale)
                
            self.light.energy = (math.sin(logic.getRealTime())*.3) + .7

            self.movement()
        else:
            
            self.light.energy = self.light.energy * utils.clamp(float(self.counter), .5, 1)
            music.pitch = utils.clamp(self.counter)
            
            self.counter -= .01
            
        if self.alive == False and self.counter < 0:
            logic.sendMessage("player_death")
            
            self.alive = True
            self.recouperating = True
            
        if self.recouperating and self.alive == True:
           
            self.light.energy = ((math.sin(logic.getRealTime())*.3) + .7) * self.counter
            music.pitch = utils.clamp(self.counter)
            
            self.counter += .05
            
            if self.counter >= 1:
                self.recouperating = False
                music.pitch = 1
        
            
        
        #light_trail.main(cont)

def nextlevel():
    dict["current_level"] += 1
    lvl = dict["current_level"]
    print("going to level", lvl)
    
    logic.getCurrentScene().replace(levels[lvl])
    
def player_death():
    logic.setTimeScale(.03)
    logic.getCurrentScene().objects[playername].alive = False
    
#def main():
    