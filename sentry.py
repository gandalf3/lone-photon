from bge import logic
import random
import math
import aud
import utils

laser_sound = aud.Factory.file(logic.expandPath("//sound/laser/laserfire01.ogg")).volume(.5)


def search():
    cont = logic.getCurrentController()
    own = cont.owner

    scene = logic.getCurrentScene()
    target = scene.objects["player"]
    
    hit = own.rayCast(target, own, 0.0, "solid", 0, 1, 0)
    
    if hit[0] == target:
        own["cansee"] = True
        if own.get("fireclock", 0)*logic.getTimeScale() > 1:
#            l.pitch = random.randrange(5, 15)*.1
            
            fire(hit[2])
            own["fireclock"] = 0
    
    else:
        own["cansee"] = False

    own["fireclock"] = own.get("fireclock", 0) + 1
            
def fire(direction):
    cont = logic.getCurrentController()
    own = cont.owner
    
    scene = logic.getCurrentScene()
    
    projectile = scene.addObject("standard_projectile", own, 0)
    projectile.alignAxisToVect(direction, 0, 1)
    projectile.setLinearVelocity((-20, 0, 0), True)
    
    projectile["sound_handler"] = aud.device().play(laser_sound)
    if projectile.get("sound_handler", 0):
        projectile["sound_handler"].pitch = logic.getTimeScale()
