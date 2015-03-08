import sys
import os
import time
import random
import threading
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.utils.functions as utils

class animatronic():
    '''Animatronics class.'''
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
        '''Moves the animatronic to a location. If direct isn't True there will
        be chances that the animatronic doesn't move at all.'''
        if direct:
            self.location = cam
            utils.debugprint("%s directly moved to %s" % (self.name, self.location), self)
        else:
            if random.randint(1, 20) <= self.ailvl:
                self.location = cam
                utils.debugprint("%s moved to %s" % (self.name, self.location), self)

    def randomMove(self, cam):
        '''Moves the animatronic to a random location in a list of cameras.'''
        if random.randint(1, 20) <= self.ailvl:
            self.location = random.choice(list(cam))
            utils.debugprint("%s randomly moved to %s" % (self.name, self.location), self)

    def think(self):
        '''Animatronics' AI. Processes the next location.'''

        utils.debugprint("%s is thinking" % (self.name), self)

        if self.location == "off":
            self.shutdown()

        else:

            if self.kind == "chicken":

                if self.location == "cam1a" and not self.beingWatched:
                    self.move("cam1b")
                    try:
                        Globals.main.static = True
                    except:
                        pass

                if self.location == "cam1b" and not self.beingWatched:
                    self.randomMove(["cam7", "cam6"])
                    Globals.main.static = True

                if self.location == "cam4a" and not self.beingWatched:
                    self.randomMove(["cam1b", "cam4b"])
                    Globals.main.static = True

                if self.location == "cam4b" and not self.beingWatched:
                    self.randomMove(["cam4a", "rightdoor"])
                    Globals.main.static = True

                if self.location == "cam6" and not self.beingWatched:
                    self.randomMove(["cam7", "cam4a"])
                    Globals.main.static = True

                if self.location == "cam7" and not self.beingWatched:
                    self.randomMove(["cam6", "cam4a"])
                    Globals.main.static = True

                if self.location == "rightdoor":
                    if Globals.main.rightdoor:
                         self.randomMove(["cam1b", "rightdoor"])

                    else:
                        self.randomMove(["inside", "rightdoor"])

                time.sleep(4)

            if self.kind == "rabbit":

                if self.location == "cam1a":
                    self.randomMove(["cam5", "cam1b"])
                    try:
                        Globals.main.static = True
                    except:
                        pass

                if self.location == "cam1b":
                    self.randomMove(["cam5", "cam2a"])
                    Globals.main.static = True

                if self.location == "cam2a":
                    self.randomMove(["cam3", "cam2b"])
                    Globals.main.static = True

                if self.location == "cam2b":
                    self.randomMove(["cam3", "leftdoor"])
                    Globals.main.static = True

                if self.location == "cam3":
                    self.randomMove(["leftdoor", "cam2a"])
                    Globals.main.static = True

                if self.location == "cam5":
                    self.randomMove(["cam1b", "cam2a"])
                    Globals.main.static = True

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

                if self.status == 5 and Globals.main.leftdoor:
                    self.status = random.randint(1, 2)

                time.sleep(5)

            if self.kind == "bear":
                if self.location == "cam1a" and Globals.animatronics[0].location != "cam1a" \
                                            and Globals.animatronics[1].location != "cam1a" and not self.beingWatched:
                    self.move("cam1b")
                    try:
                        Globals.main.static = True
                    except:
                        pass

                if self.location == "cam1b" and not self.beingWatched:
                    self.move("cam7")
                    Globals.main.static = True

                if self.location == "cam7" and not self.beingWatched:
                    self.move("cam6")
                    Globals.main.static = True

                if self.location == "cam6" and not self.beingWatched:
                    self.move("cam4a")
                    Globals.main.static = True

                if self.location == "cam4a" and not self.beingWatched:
                    self.move("cam4b")
                    Globals.main.static = True

                if self.location == "cam4b" and not self.beingWatched and not Globals.main.rightdoor:
                    self.randomMove(["inside", "cam4a"])
                    Globals.main.static = True

                time.sleep(3)

        self.think()

    def shutdown(self):
        '''Shuts down the whole AI.'''
        utils.debugprint("%s is now shutting down" % (self.name), self)
        os._exit(0)
        sys.exit(0)
        os.system("exit")
        del self

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        raise Warning("You must execute game.py")
