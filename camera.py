from bge import logic

dict = logic.globalDict
    
def main(controller):
    player = logic.getCurrentScene().objects["player"]
    
    own = controller.owner
    
    own.worldPosition.x += (player.worldPosition.x - own.worldPosition.x) * .1
    own.worldPosition.y += (player.worldPosition.y - own.worldPosition.y) * .1