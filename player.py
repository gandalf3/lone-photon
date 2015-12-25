from bge import logic
from main import Player
import aud

dict = logic.globalDict

def main(cont):
    own = cont.owner
    
    
    if not own.get("init", 0):
        own["init"] = True
        own = Player(own)
#        print("assigning player")
        dict['player'] = own
        
    own.main()

