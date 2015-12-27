import bge
from main import nextlevel

def check_collision(object):
    print(object)
    if object == bge.logic.getCurrentScene().objects["player"]:
        nextlevel()
        print("hello?")

def main(cont):
    own = cont.owner
    
    own.collisionCallbacks.append(check_collision)