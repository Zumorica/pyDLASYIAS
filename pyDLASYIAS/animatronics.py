import sys
import os
import time
import random
import _thread
import threading
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.utils.functions as utils

class animatronic(object): #Animatronics' class.
    def __init__(self, name, kind, ailvl=20, location="cam1a"):
        self.name = name
        self.kind = kind
        self.ailvl = ailvl
        self.location = location
        self.slocation = location
        self.agressiveness = 0
        Globals.animatronics.append(self)
        if self.kind == "fox":
            self.foxstatus = 0
            self.foxviewing = False
            self.dmove("cam1c")

        if self.kind == "bear":
            self.bseen = False

        if self.ailvl <= 20:
            if self.ailvl == 0:
                self.ailvl = 0.5
            utils.debugprint("%s's AI started." % (self.name.upper()), self)
            if self.kind == "bear":
                self.dmove("cam1a")

            _thread.start_new_thread(self.think, ())

        else:
            print("%s's AI LEVEL IS OVER 20. BE CAREFUL!" % (self.name.upper()))
            if self.kind == "bear":
                if self.ailvl > 5:
                    utils.debugprint("%s's AI IS NOW ACTIVE!" % (self.name.upper()), self)
                    self.dmove("cam1a")
                else:
                    self.dmove("off")
            _thread.start_new_thread(self.think, ())

    def dmove(self, room):
        self.location = room
        if room == "off":
            utils.debugprint("%s has been queued for shutdown." % (self.name), self)
        else:
            utils.debugprint("DMoved %s to %s" % (self.name, room), self)
        return None

    def rmove(self, room):
        self.choice = random.choice(list(room))
        utils.debugprint("%s chose %s" % (self.name, self.choice), self)
        if random.randint(0, int(self.ailvl)) in range(int(self.ailvl / 2)):
            self.location = self.choice
            utils.debugprint("%s has been moved to %s" % (self.name, self.location), self)
        else:
            utils.debugprint("%s didn't move from its location" % (self.name), self)
        return None

    def think(self):
        if self.location == "off":
            utils.debugprint("%s's AI is shutting down." % (self.name), self)
            del self
            os.system("exit")
            sys.exit(0)
            os._exit(0)
            return None
        else:
            if self.kind == "chicken":
                utils.debugprint("%s is thinking..." % (self.name), self)
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.agressiveness == 0:
                    if self.location == "cam1a":
                        self.rmove(["cam1b", "cam6", "cam7"])
                    if self.location == "cam1b":
                        self.rmove(["cam7", "cam6"])
                    if self.location == "cam7":
                        self.rmove(["cam1b", "cam6"])
                    if self.location == "cam6":
                        self.rmove(["cam1b", "cam7"])
                    if random.randint(0, int(self.ailvl)) in range(0, int(self.ailvl / 2)):
                        self.agressiveness = 1

                if self.agressiveness == 1:
                    if self.location == "cam1a":
                        self.rmove(["cam1b"])
                    if self.location == "cam1b":
                        self.rmove(["cam7", "cam6", "cam4a"])
                    if self.location == "cam7":
                        self.rmove(["cam1b"])
                    if self.location == "cam6":
                        self.rmove(["cam1b"])
                    if self.location == "cam4a":
                        self.rmove(["cam1b", "rightdoor", "cam4b"])
                    if self.location == "cam4b":
                        self.rmove(["cam4a", "cam1a"])
                    if random.randint(0, int(self.ailvl)) in range(0, int(self.ailvl / 3)):
                        self.agressiveness = 2

                if self.agressiveness == 2:
                    if self.location == "cam1a":
                        self.rmove(["cam1b"])
                    if self.location == "cam1b":
                        self.rmove(["cam7", "cam6", "cam4a"])
                    if self.location == "cam7":
                        self.rmove(["cam1b", "cam4a"])
                    if self.location == "cam6":
                        self.rmove(["cam1b", "cam4a"])
                    if self.location == "cam4a":
                        self.rmove(["cam1b", "rightdoor", "cam4b", "cam4b", "cam4b"])
                    if self.location == "cam4b":
                        self.rmove(["cam4a", "rightdoor", "rightdoor", "rightdoor"])
                    if self.location == "rightdoor":
                        pass
                    if self.location == "inside":
                        pass
                    if random.randint(0, int(self.ailvl)) in range(0, int(self.ailvl / 4)):
                        self.agressiveness = 3

                if self.agressiveness == 3:
                    if self.location == "cam1a":
                        self.rmove(["cam1b"])
                    if self.location == "cam1b":
                        self.rmove(["cam4a"])
                    if self.location == "cam6":
                        self.rmove(["cam4a"])
                    if self.location == "cam7":
                        self.rmove(["cam4a"])
                    if self.location == "cam4a":
                        self.rmove(["cam4b"])
                    if self.location == "cam4b":
                        self.rmove(["rightdoor"])
                    if self.location == "rightdoor":
                        pass
                    if self.location == "inside":
                        pass

                time.sleep(random.randint(20, 25) / self.ailvl)
                self.think()
                return None

            if self.kind == "rabbit":
                utils.debugprint("%s is thinking..." % (self.name), self)
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.agressiveness == 0:
                    if self.location == "cam1a":
                        self.rmove(["cam1b", "cam5"])
                    if self.location == "cam1b":
                        self.rmove(["cam5", "cam2a"])
                    if self.location == "cam5":
                        self.rmove(["cam1b", "cam2a"])
                    if self.location == "cam2a":
                        self.rmove(["cam1b", "cam3"])
                    if random.randint(0, int(self.ailvl)) in range(0, int(self.ailvl / 2)):
                        self.agressiveness = 1

                if self.agressiveness == 1:
                    if self.location == "cam1a":
                        self.rmove(["cam1b", "cam5", "cam5", "cam2a"])
                    if self.location == "cam1b":
                        self.rmove(["cam5", "cam2a"])
                    if self.location == "cam5":
                        self.rmove(["cam1b", "cam2a"])
                    if self.location == "cam2a":
                        self.rmove(["cam3", "cam1b", "cam2b"])
                    if self.location == "cam3":
                        self.rmove(["cam2a", "cam2b", "cam1b"])
                    if self.location == "cam2b":
                        self.rmove(["leftdoor", "cam2a", "cam3", "cam1b"])
                    if self.location == "leftdoor":
                        pass
                    if random.randint(0, int(self.ailvl)) in range(0, int(self.ailvl / 3)):
                        self.agressiveness = 2

                if self.agressiveness == 2:
                    if self.location == "cam1a":
                        self.rmove(["cam1b", "cam5", "cam2a"])
                    if self.location == "cam1b":
                        self.rmove(["cam5", "cam2a", "cam2a"])
                    if self.location == "cam5":
                        self.rmove(["cam1b", "cam2a"])
                    if self.location == "cam2a":
                        self.rmove(["cam3", "cam2b"])
                    if self.location == "cam3":
                        self.rmove(["cam2a", "cam2b"])
                    if self.location == "cam2b":
                        self.rmove(["leftdoor", "cam2a", "cam3", "cam1b", "leftdoor"])
                    if self.location == "leftdoor":
                        pass
                    if random.randint(0, int(self.ailvl)) in range(0, int(self.ailvl / 4)):
                        self.agressiveness = 3

                if self.agressiveness == 3:
                    if self.location == "cam1a":
                        self.rmove(["cam1b"])
                    if self.location == "cam1b":
                        self.rmove(["cam2a"])
                    if self.location == "cam5":
                        self.rmove(["cam1b"])
                    if self.location == "cam2a":
                        self.rmove(["cam2b", "leftdoor"])
                    if self.location == "cam3":
                        self.rmove(["cam2b", "leftdoor"])
                    if self.location == "cam2b":
                        self.rmove(["leftdoor"])
                    if self.location == "leftdoor":
                        pass

                time.sleep(random.randint(20, 25) / self.ailvl)
                self.think()
                return None

            if self.kind == "fox":
                utils.debugprint("%s is thinking..." % (self.name), self)
                time.sleep(20 / self.ailvl)

                if self.foxstatus < 3 and not self.foxviewing:
                    if random.randint(0, 20) <= self.ailvl:
                        self.foxstatus += 1

                time.sleep(20 / self.ailvl)
                self.think()
                return None

            if self.kind == "bear":
                if self.ailvl > 5:
                    utils.debugprint("%s is thinking..." % (self.name), self)
                    time.sleep(40 / self.ailvl)
                    if self.location == "cam1a":
                        if Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location != "cam1a":
                            utils.debugprint("%s.bseen = %s" % (self.name, self.bseen), self)
                            if self.bseen == False:
                                self.rmove(["cam1b"])
                                print("")
                                print("A deep laugh can be heard.")
                                print("> ", end="")
                                self.think()
                        else:
                            self.think()


                    if self.location == "cam1b":
                        if self.bseen == False:
                                print("")
                                print("A deep laugh can be heard.")
                                print("> ", end="")
                                self.rmove(["cam7"])
                        else:
                            self.think()

                    if self.location == "cam7":
                        if self.bseen == False:
                                print("")
                                print("A deep laugh can be heard.")
                                print("> ", end="")
                                self.rmove(["cam6"])
                        else:
                            self.think()

                    if self.location == "cam4a":
                        if self.bseen == False:
                                print("")
                                print("A deep laugh can be heard.")
                                print("> ", end="")
                                self.rmove(["cam4b"])

                    if self.location == "cam4b":
                        time.sleep(40 / self.ailvl)
                        if self.bseen == False:
                            print("")
                            print("A deep laugh can be heard.")
                            print("> ", end="")
                            self.rmove(["inside", "cam4a", "cam4a"])

                    if self.location == "rightdoor":
                        pass
                else:
                    pass

                return None

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
