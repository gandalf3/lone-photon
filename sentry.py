from bge import logic
from random import random

def search():
    cont = logic.getCurrentController()
    own = cont.owner

    scene = logic.getCurrentScene()
    target = scene.objects["player"]
    
    hit = own.rayCast(target, own, 0.0, "player", 0, 0, 0)
    
    print(hit)
    if hit != (None, None, None):
        own["cansee"] = True
        if random() < .1:
            fire(hit[2])
    else:
        own["cansee"] = False
        
def fire(direction):
    cont = logic.getCurrentController()
    own = cont.owner
    
    scene = logic.getCurrentScene()
    
    projectile = scene.addObject("standard_projectile", own, 0)
    projectile.worldOrientation = direction
    projectile.setLinearVelocity((5, 0, 0), True)