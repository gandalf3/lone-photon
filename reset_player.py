from bge import logic

#cont = logic.getCurrentController()
#message = cont.sensors["Message"]


def main(cont):
    own = cont.owner
    logic.getCurrentScene().objects["player"].worldPosition = own.worldPosition
    
    if 'init' not in own:
        logic.getCurrentScene().objects["camera"].worldPosition.x = own.worldPosition.x
        logic.getCurrentScene().objects["camera"].worldPosition.y = own.worldPosition.y
        own['init'] = True
