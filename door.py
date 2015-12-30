from main import Door


def main(cont):
    own = cont.owner
    
    if not own.get("init", 0):
        own["init"] = True
        own = Door(own)

    own.main()

