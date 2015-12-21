from main import Sentry

def main(cont):
    own = cont.owner
    
    if not "init" in own:
        own["init"] = True
        print("setup")
        own = Sentry(own)
    
    own.main()