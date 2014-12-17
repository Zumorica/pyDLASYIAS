import sys, os, time, random, thread, threading, Globals
from utils import cls
from utils import debug

class animatronic(object): #Animatronics' class.
    def __init__(self, name, kind, ailvl=20, location="cam1a"):
        self.name = name         #Name will be used for printing things.
        self.kind = kind         #Kinds: Chicken / Rabbit / Bear (WIP) / Fox
        self.ailvl = ailvl       #AI LVL. 1 - 20. ("0 AI LVL" is impossible to achieve, because you can't divide by zero.)
        self.location = location #This location determines where the animatronics are.
        self.slocation = location #Starting location.

        if self.kind == "fox":   #Foxkind variables.
            self.foxstatus = 0 #0 = Hiding. 1 = Peeking. 2 = Looking thro. 3 = Out 4 = About to sprint 5 = Sprinting
            self.foxtseen = 0 #Times seen.
            self.foxsleep = 0 #Number of seconds to sleep until next status.

        if self.kind == "bear": #Bearkind variables.
            self.bseen = False #Being seen. If the camera is active, this variable will be true. Else, it will be false.

        if self.ailvl <= 20:
            debug.debugprint("%s's AI started. -%s BEHAVIOR-" % (self.name.upper(), self.kind.upper()))
            if self.kind == "bear":
                if self.ailvl > 5:
                    debug.debugprint("%s's AI IS NOW ACTIVE! -%s BEHAVIOR-" % (self.name.upper(), self.kind.upper()))
                    self.dmove("cam1a")
                else:
                    self.dmove("off")
            thread.start_new_thread(self.think, ()) #Multithreading. This makes the game possible



        else:
            print "%s's AI LEVEL OVER 20. BE CAREFUL! -%s BEHAVIOR-" % (self.name.upper(), self.kind.upper())
            if self.kind == "bear":
                if self.ailvl > 5:
                    debug.debugprint("%s's AI IS NOW ACTIVE! -%s BEHAVIOR-" % (self.name.upper(), self.kind.upper()))
                    self.dmove("cam1a")
                else:
                    self.dmove("off")
            thread.start_new_thread(self.think, ()) #Multithreading. This makes the game possible

    def dmove(self, room): #Direct move / Debug move. Moves an animatronic to a location.
        self.location = room
        debug.debugprint("DMoved %s to %s" % (self.name, room))
        return None

    def rmove(self, room): #Random move. Moves an animatronic (or not) to a location.
        self.choice = random.choice(room) #Yup. You can input lists!
        debug.debugprint("%s's choice was %s -%s BEHAVIOR-" % (self.name, self.choice, self.kind.upper()))
        if random.randint(0, 20) in range(0, self.ailvl):
            self.location = self.choice
            debug.debugprint("%s moved to %s -%s BEHAVIOR-" % (self.name, self.choice, self.kind.upper()))
            self.think()
            return None

        else:
            debug.debugprint("%s didn't move at all" % (self.name))
            self.think()
            return None

    def think(self):
        if self.location == "off": #Shuts down the AI
            debug.debugprint("%s's AI is shutting down." % (self.name))
            os.system("exit")
            sys.exit(0)
            os._exit(0)
            return None
        else:
            #Chicken's AI
            if self.kind == "chicken":
                debug.debugprint("%s is thinking... -CHICKEN BEHAVIOR- -%s-" % (self.name, self.location))
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.location == "cam1a":
                    self.rmove(["cam1b"])
                if self.location == "cam1b":
                    self.rmove(["cam1a", "cam7", "cam6", "cam4a"])
                if self.location == "cam7":
                    self.rmove(["cam1b"])
                if self.location == "cam6":
                    self.rmove(["cam1b"])
                if self.location == "cam4a":
                    self.rmove(["cam1b", "rightdoor", "cam4b", "cam4b"])
                if self.location == "cam4b":
                    self.rmove(["cam4a", "rightdoor", "rightdoor", "cam1a"])
                if self.location == "rightdoor":
                    debug.debugprint("%s is at rightdoor." % (self.name))
                if self.location == "inside":
                    pass
                return None


            #Rabbit's AI
            if self.kind == "rabbit":
                debug.debugprint("%s is thinking... -RABBIT BEHAVIOR- -%s-" % (self.name, self.location))
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.location == "cam1a":
                    self.rmove(["cam1b"])
                if self.location == "cam1b":
                    self.rmove(["cam1a", "cam5", "cam2a", "cam2a"]) #Do not edit cam2a, it's doubled for a reason.
                if self.location == "cam5":
                    self.rmove, (["cam1b"])
                if self.location == "cam2a":
                    self.rmove(["cam3", "leftdoor", "cam2b", "cam2b"])
                if self.location == "cam3":
                    self.rmove(["cam2a", "leftdoor", "cam2b"])
                if self.location == "cam2b":
                    self.rmove(["cam2a", "leftdoor", "leftdoor", "cam1a"])
                if self.location == "leftdoor":
                    debug.debugprint("%s is at leftdoor." % (self.name))
                if self.location == "inside":
                    pass
                return None

            #Fox's AI
            if self.kind == "fox":
                debug.debugprint("%s is thinking... -FOX BEHAVIOR- -%s-" % (self.name, self.location))
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.foxstatus == 4:
                    time.sleep(100 / self.ailvl)
                    self.foxstatus = 5


                if self.foxstatus >= 5:
                    debug.debugprint("%s is sprinting towards you! -FOX BEHAVIOR- -%s-" % (self.name, self.location))
                    time.sleep(20 / self.ailvl)
                    self.location = "cam2a"
                    time.sleep(20 / self.ailvl)
                    self.location = "leftdoor"

                if self.foxtseen >= 1:
                    debug.debugprint("%s status remains at %s -FOX BEHAVIOR- -%s-" % (self.name, self.foxstatus, self.location))
                    self.foxsleep += self.foxtseen
                    self.basesleep = random.randint(150, 200) / self.ailvl
                    self.foxtseen = 0
                    time.sleep(self.basesleep + self.foxsleep)
                    if random.randint(0, 1) == 1:
                        self.foxstatus += 1
                        debug.debugprint("%s status is now %s -FOX BEHAVIOR- -%s-" % (self.name, self.foxstatus, self.location))
                        self.think()
                    else:
                        debug.debugprint("%s status remains at %s -FOX BEHAVIOR- -%s-" % (self.name, self.foxstatus, self.location))
                        self.think()



                else:
                    if random.randint(0, 1) == 1:
                        self.foxstatus +=1
                        debug.debugprint("%s status is now %s" % (self.name, self.foxstatus))
                    else:
                        debug.debugprint("%s status remains at %s" % (self.name, self.foxstatus))
                    time.sleep(random.randint(150, 200) / self.ailvl)
                    self.think()

            #Bear's AI
            if self.kind == "bear":
                if self.ailvl > 5:
                    debug.debugprint("FYI: Bear behavior doesn't *really* work. Be careful around this.")
                    time.sleep(random.randint(20, 25) / self.ailvl)
                    if self.location == "cam1a":
                        if self.someoneThere("cam1a") == True:
                            debug.debugprint("%s.bseen = %s -%s BEHAVIOR-" % (self.name, self.bseen, self.kind.upper()))
                            if self.bseen == False:
                                self.rmove("cam1b")
                                print "A deep laugh can be heard."
                                self.think()
                        else:
                            self.think()


                    if self.location == "cam1b":
                        if self.bseen == False:
                            print "A deep laugh can be heard."
                            self.rmove("cam7")
                        else:
                            self.think()

                    if self.location == "cam7":
                        if self.bseen == False:
                            print "A deep laugh can be heard."
                            self.rmove("cam6")
                        else:
                            self.think()

                    if self.location == "cam4a":
                        if self.bseen == False:
                            print "A deep laugh can be heard."
                            self.rmove("cam4b")

                    if self.location == "cam4b":
                        time.sleep(random.randint(20, 25) / self.ailvl)
                        if self.bseen == False:
                            print "A deep laugh can be heard."
                            self.rmove(["inside", "cam4a", "cam4a"])

                    if self.location == "rightdoor":
                        pass
                else:
                    pass

                return None


    def someoneThere(self, cam): #Function for bearkind. Duh.
        for animatronic in Globals.animatronics:
            if animatronic.kind == "bear":
                pass
            elif animatronic.location == cam:
                return True
        return False
