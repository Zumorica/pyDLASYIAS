import time
import pyDLASYIAS.Globals as Globals

log = open("log.txt", "a")
log.write(time.strftime("\n %d/%m/%Y - %H:%M:%S \n"))

def debugprint(text, animatronic=None, writetolog=True):
    if writetolog == True:
        if animatronic == None:
            log.write("%s %s \n" % (text, time.strftime("%H:%M:%S")))
        else:
            log.write("%s -%s BEHAVIOR- -AI LVL: %s- -AGRE.: %s-  -%s- %s \n" % (text, animatronic.kind.upper(), animatronic.ailvl, animatronic.agressiveness, animatronic.location.upper(), time.strftime("%H:%M:%S")))

    if Globals.debug == True:
        if animatronic == None:
            print("%s %s \n" % (text, time.strftime("%H:%M:%S")))
        else:
            print("%s -%s BEHAVIOR- -AI LVL: %s- -AGRE.: %s- -%s- %s \n" % (text, animatronic.kind.upper(), animatronic.ailvl, animatronic.agressiveness, animatronic.location.upper(), time.strftime("%H:%M:%S")))

    return None
