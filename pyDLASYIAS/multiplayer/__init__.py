try:
    import sys
    import pyDLASYIAS.multiplayer.guard
    import pyDLASYIAS.multiplayer.chicken
    #import pyDLASYIAS.multiplayer.rabbit
    #import pyDLASYIAS.multiplayer.bear
    #import pyDLASYIAS.multiplayer.fox
except ImportError:
    e = sys.exc_info()[1]
    print("Could not import multiplayer module %s" %e)
