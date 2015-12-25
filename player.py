from main import Player


def main(cont):
    own = cont.owner
    
    if not own.get("init", 0):
        own["init"] = True
        own = Player(own)
        
    own.main()

