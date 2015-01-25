import time
import pyDLASYIAS.Globals as Globals

Globals.log = open("log.txt", "a")
Globals.log.write(time.strftime("\n %d/%m/%Y - %H:%M:%S \n"))

def debugprint(text, animatronic=None, writetolog=True):
    if writetolog == True:
        if animatronic == None:
            Globals.log.write("%s %s \n" % (text, time.strftime("%H:%M:%S")))
        else:
            Globals.log.write("%s -%s BEHAVIOR- -AI LVL: %s- -AGRE.: %s-  -%s- %s \n" % (text, animatronic.kind.upper(), animatronic.ailvl, animatronic.agressiveness, animatronic.location.upper(), time.strftime("%H:%M:%S")))

    if Globals.debug == True:
        if animatronic == None:
            print("%s -%s USAGE- -%s POWER- -%s TIME IN-GAME- -%s- \n" % (text, time.strftime("%H:%M:%S")))
        else:
            print("%s -%s BEHAVIOR- -AI LVL: %s- -AGRE.: %s- -%s- %s \n" % (text, animatronic.kind.upper(), animatronic.ailvl, animatronic.agressiveness, animatronic.location.upper(), time.strftime("%H:%M:%S")))

    return None

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
