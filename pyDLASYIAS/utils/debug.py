import time
from .. import Globals

log = open("log.txt", "a")
log.write(time.strftime("\n %d/%m/%Y - %H:%M:%S \n"))

def debugprint(text, writetolog=True):
    if writetolog == True:
        log.write(text + "\n")
    if Globals.debug == True:
        print text + "\n"
    else:
        pass

    return None
