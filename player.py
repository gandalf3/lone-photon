from bge import logic, events
import light_trail
import bge
import random
import math
import mathutils
import utils
import aud

sound = aud.Factory.file(logic.expandPath("//sound/Adventure Meme.mp3")).volume(.1).loop(-1)
#music = aud.device().play(sound)

scene = logic.getCurrentScene()



def movement(movement_speed):
    cont = logic.getCurrentController()
    own = cont.owner
    
    keyboard = logic.keyboard
    ACTIVE = logic.KX_INPUT_ACTIVE
    
    movement = own.getLinearVelocity()

    # forward
    if keyboard.events[events.WKEY] == ACTIVE:
        movement[1] = utils.clamp(movement[1] + movement_speed*.1, -movement_speed, movement_speed)
        
    # backward
    if keyboard.events[events.SKEY] == ACTIVE:
        movement[1] = utils.clamp(movement[1] + -movement_speed*.1, -movement_speed, movement_speed)
    
    # left
    if keyboard.events[events.AKEY] == ACTIVE:
        movement[0] = utils.clamp(movement[0] + -movement_speed*.1, -movement_speed, movement_speed)
        
    # right
    if keyboard.events[events.DKEY] == ACTIVE:
        movement[0] = utils.clamp(movement[0] + movement_speed*.1, -movement_speed, movement_speed)
            
    own.setLinearVelocity(movement)
    
    if own.getAngularVelocity() < mathutils.Vector((1,1,1)):
        own.setAngularVelocity(((random.random()*5)-2.5, (random.random()*5)-2.5, (random.random()*5)-2.5))
            
def main():
    cont = logic.getCurrentController()
    own = cont.owner
    
    movement_speed = 20
    
    velocity = own.getLinearVelocity()
    speed = utils.velocity2speed(velocity)
    timescale = utils.clamp(speed/movement_speed, .05, 1)
    
    own['timescale'] = timescale
    own['speed'] = speed
    if timescale != logic.getTimeScale():
        logic.setTimeScale(timescale)
        
    scene.objects["player_light"].energy = (math.sin(logic.getRealTime())*.3) + .7

    movement(movement_speed)
    light_trail.main(cont)
#    music.pitch = utils.clamp(timescale*.2 + .85)