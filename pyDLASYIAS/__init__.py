import pyDLASYIAS.Globals
import pyDLASYIAS.spr
import pyDLASYIAS.snd
import pyDLASYIAS.multiplayer

try:
    import sys
    import pyDLASYIAS.Globals
    Globals.init()
    import pyDLASYIAS.spr
    spr.init()
    import pyDLASYIAS.snd
    snd.init()

except ImportError:
    e = sys.exc_info()[1]
    print("Could not import module %s" %e)
