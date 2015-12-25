from main import Projectile
from bge import logic
import random
import aud

laser_sounds = [aud.Factory.file(logic.expandPath("//sound/laser/laserfire01_mono.wav")).volume(.5).fadeout(0, .4), aud.Factory.file(logic.expandPath("//sound/laser/laserfire02_mono.wav")).volume(.5).fadeout(0, .4)]

def main(cont):
    own = cont.owner
    
    if not "init" in own:
        own["init"] = True
        own = Projectile(own, sound=random.choice(laser_sounds))
    
    own.main()