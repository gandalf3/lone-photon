from main import Vectsplosion

def main(cont):
    own = cont.owner
    
    if not "init" in own:
        own["init"] = True
        own = Vectsplosion(own)
        
    own.main()
        
    
