import sys
import os
import time
import random
import threading
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.utils.functions as utils

class animatronic():
    def __init__(self, name, kind, ailvl):
        self.name = name
        self.kind = kind
        self.ailvl = ailvl
        self.beingWatched = False
        self.status = 0

        if self.ailvl > 20:
            self.ailvl = 20

        if self.kind == "fox":
            self.location = "cam1c"

        else:
            self.location = "cam1a"

        Globals.animatronics.append(self)

        self.aiThread = threading.Thread(target=self.think)
        self.aiThread.setDaemon(True)

        self.aiThread.start()

    def move(self, cam, direct=False):
        if direct:
            self.location = cam
            utils.debugprint("%s directly moved to %s" % (self.name, self.location), self)
        else:
            if random.randint(1, 20) <= self.ailvl:
                self.location = cam
                utils.debugprint("%s moved to %s" % (self.name, self.location), self)

    def randomMove(self, cam):
        if random.randint(1, 20) <= self.ailvl:
            self.location = random.choice(list(cam))
            utils.debugprint("%s randomly moved to %s" % (self.name, self.location), self)

    def think(self):

        utils.debugprint("%s is thinking" % (self.name), self)

        if self.location == "off":
            self.shutdown()

        if self.kind == "chicken" and not self.beingWatched:

            if self.location == "cam1a":
                self.move("cam1b")

            if self.location == "cam1b":
                self.randomMove(["cam7", "cam6"])

            if self.location == "cam4a":
                self.randomMove(["cam1b", "cam4b"])

            if self.location == "cam4b":
                self.randomMove(["cam4a", "rightdoor"])

            if self.location == "cam6":
                self.randomMove(["cam7", "cam4a"])

            if self.location == "cam7":
                self.randomMove(["cam6", "cam4a"])

            if self.location == "rightdoor":
                time.sleep(random.randint(6, 15))
                if Globals.main.rightdoor:
                     self.randomMove(["cam1b", "rightdoor"])

                else:
                    self.randomMove(["inside", "rightdoor"])

        if self.kind == "rabbit" and not self.beingWatched:

            if self.location == "cam1a":
                self.randomMove(["cam5", "cam1b"])

            if self.location == "cam1b":
                self.randomMove(["cam5", "cam2a"])

            if self.location == "cam2a":
                self.randomMove(["cam3", "cam2b"])

            if self.location == "cam2b":
                self.randomMove(["cam3", "leftdoor"])

            if self.location == "cam3":
                self.randomMove(["leftdoor", "cam2a"])

            if self.location == "cam5":
                self.randomMove(["cam1b", "cam2a"])

            if self.location == "leftdoor":
                time.sleep(random.randint(4, 10))
                if Globals.main.leftdoor:
                     self.randomMove(["cam1b", "leftdoor"])

                else:
                    self.randomMove(["inside", "leftdoor"])

        time.sleep(1)
        self.think()

        if self.kind == "fox":
            if self.status < 3 and not self.beingWatched:
                if random.randint(0, 20) <= self.ailvl:
                    self.status += 1

        if self.kind == "bear" and not self.beingWatched:
            if self.location == "cam1a" and Globals.animatronics[0].location != "cam1a" \
                                        and Globals.animatronics[1].location != "cam1a":
                self.move("cam1b")

            if self.location == "cam1b":
                self.move("cam7")

            if self.location == "cam7":
                self.move("cam6")

            if self.location == "cam6":
                self.move("cam4a")

            if self.location == "cam4a":
                self.move("cam4b")

            if self.location == "cam4b":
                self.randomMove(["inside", "cam4a"])

    def shutdown(self):
        utils.debugprint("%s is now shutting down" % (self.name), self)
        os._exit(0)
        sys.exit(0)
        os.system("exit")
        del self

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
