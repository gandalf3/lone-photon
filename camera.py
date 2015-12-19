from bge import logic

scene = logic.getCurrentScene()
player = scene.objects["player"]
    
def main(controller):
    own = controller.owner
    
    
    own.worldPosition.x += (player.worldPosition.x - own.worldPosition.x) * .1
    own.worldPosition.y += (player.worldPosition.y - own.worldPosition.y) * .1