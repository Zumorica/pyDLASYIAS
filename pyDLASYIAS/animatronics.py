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

        if self.kind == "chicken":

            if self.location == "cam1a" and not self.beingWatched:
                self.move("cam1b")

            if self.location == "cam1b" and not self.beingWatched:
                self.randomMove(["cam7", "cam6"])

            if self.location == "cam4a" and not self.beingWatched:
                self.randomMove(["cam1b", "cam4b"])

            if self.location == "cam4b" and not self.beingWatched:
                self.randomMove(["cam4a", "rightdoor"])

            if self.location == "cam6" and not self.beingWatched:
                self.randomMove(["cam7", "cam4a"])

            if self.location == "cam7" and not self.beingWatched:
                self.randomMove(["cam6", "cam4a"])

            if self.location == "rightdoor":
                if Globals.main.rightdoor:
                     self.randomMove(["cam1b", "rightdoor"])

                else:
                    self.randomMove(["inside", "rightdoor"])

            time.sleep(4)

        if self.kind == "rabbit":

            if self.location == "cam1a" and not self.beingWatched:
                self.randomMove(["cam5", "cam1b"])

            if self.location == "cam1b" and not self.beingWatched:
                self.randomMove(["cam5", "cam2a"])

            if self.location == "cam2a" and not self.beingWatched:
                self.randomMove(["cam3", "cam2b"])

            if self.location == "cam2b" and not self.beingWatched:
                self.randomMove(["cam3", "leftdoor"])

            if self.location == "cam3" and not self.beingWatched:
                self.randomMove(["leftdoor", "cam2a"])

            if self.location == "cam5" and not self.beingWatched:
                self.randomMove(["cam1b", "cam2a"])

            if self.location == "leftdoor":
                if Globals.main.leftdoor:
                     self.randomMove(["cam1b", "leftdoor"])

                else:
                    self.randomMove(["inside", "leftdoor"])

            time.sleep(4)

        if self.kind == "fox":
            if self.status < 3 and not self.beingWatched:
                if random.randint(0, 20) <= self.ailvl:
                    self.status += 1

            time.sleep(5)

        if self.kind == "bear":
            if self.location == "cam1a" and Globals.animatronics[0].location != "cam1a" \
                                        and Globals.animatronics[1].location != "cam1a" and not self.beingWatched:
                self.move("cam1b")

            if self.location == "cam1b" and not self.beingWatched:
                self.move("cam7")

            if self.location == "cam7" and not self.beingWatched:
                self.move("cam6")

            if self.location == "cam6" and not self.beingWatched:
                self.move("cam4a")

            if self.location == "cam4a" and not self.beingWatched:
                self.move("cam4b")

            if self.location == "cam4b" and not self.beingWatched and not Globals.main.rightdoor:
                self.randomMove(["inside", "cam4a"])

            time.sleep(3)

        self.think()

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
