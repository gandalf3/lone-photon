import bge
from main import nextlevel
player = bge.logic.globalDict['player']

def check_collision(object):
    if object == player:
        nextlevel()

def main(cont):
    own = cont.owner
    
    own.collisionCallbacks.append(check_collision)