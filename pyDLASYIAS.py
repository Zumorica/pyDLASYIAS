import sys, os, time, random, thread
from threading import Timer

debug = False

def debugprnt(text):
    if debug == True:
        print text + "\n"
    else:
        pass



camsl = ["cam1a", "cam1b", "cam2a", "cam2b", "cam3", "cam4a", "cam4b", "cam5", "cam6", "cam7"]
gdoorl = False
gdoorl = True


class animatronic(object):
    def __init__(self, name, kind, ailvl=25, location="cam1a"): #Only change location for special animatronics
        self.name = name
        self.ailvl = ailvl
        self.location = location
        self.kind = kind
        thread.start_new_thread(self.think, ())
        #Special locations: leftdoor / rightdoor

    def move(self, adyacent=[]):
        self.choice = random.choice(adyacent)
        debugprnt("%s's choice was %s" % (self.name, self.choice))
        if random.randint(0, 25) in range(0, self.ailvl):
            self.location = self.choice
            self.think()
            debugprnt("%s moved to %s" % (self.name, self.location))
        else:
            debugprnt("%s didn't move at all" % (self.name))
            self.think()
            return None
        
    def think(self):
        #Chicken's AI / Also, this is very confusing
        if self.kind == "chicken":
            debugprnt("%s is thinking..." % (self.name))
            time.sleep(2)
            if self.location == "cam1a":
                self.move(["cam1b"])
            if self.location == "cam1b":
                self.move(["cam1a", "cam7", "cam6", "cam4a"])
            if self.location == "cam7":
                self.move(["cam1b"])
            if self.location == "cam6":
                self.move(["cam1b"])
            if self.location == "cam4a":
                self.move(["cam1b", "rightdoor"])
            if self.location == "rightdoor":
                pass
                
        #Rabbit's AI / Confusing. 
        if self.kind == "rabbit":
            debugprnt("%s is thinking..." % (self.name))
            time.sleep(2)
            if self.location == "cam1a":
                self.move(["cam1b"])
            if self.location == "cam1b":
                self.move(["cam1a", "cam5", "cam2a", "cam2a"]) #Do not edit cam2a, it's doubled for a reason.
            if self.location == "cam5":
                self.move(["cam1b"])
            if self.location == "cam2a":
                self.move(["cam3", "leftdoor", "leftdoor"]) #Do not edit leftdoor neither
            if self.location == "cam3":
                self.move(["cam2a"])
            if self.location == "leftdoor":
                pass
                



#Above this comment: Animatronics' AI
#Below this comment: Main game / etc

class main(object):
    def __init__(self, doorl=False, doorr=False, lightl=False, lightr=False, power=100, usage=9.6, time=0):
        self.doorl = doorl
        self.doorr = doorr
        self.lightl = lightl
        self.lightr = lightr
        self.power = power
        self.usage = usage
        self.camon = False
        self.time = time
        self.recalculatePowUsage()
        self.secoffice()
        self.checkAnimDoors()

    def recalculatetime(self):
        self.rtime = Timer(86.0, self.hour)

    def hour(self):
        self.time += 1
        if self.time == 6:
            print "5AM -> 6AM"
            print "You survived."
            sys.exit(0)

    def powUsage(self):
        self.power -= 1
        if self.power <= 0:
            #Freddy SHOULD appear here
            print "Game over"
            sys.exit(0)

    def animAtDoors(self):
        for animatronic in animatronics:
            if animatronic.location == "leftdoor":
                time.sleep(10)
                if self.doorl == False:
                    print "%s got you. Game over!" % (animatronic.name)
                    time.sleep(2)
                    sys.exit(0)
                else:
                    animatronic.move(["cam1a"])
                    
            if animatronic.location == "rightdoor":
                time.sleep(10)
                if self.doorr == False:
                    print "%s got you. Game over!" % (animatronic.name)
                    time.sleep(1)
                    sys.exit(0)
                else:
                    animatronic.move(["cam1a"])
    def checkAnimDoors(self):
        self.animdoors = Timer(5, self.animAtDoors)
        self.animatdoors.start()
    
    def recalculatePowUsage(self):
        self.t = Timer(long(self.usage), self.powUsage)
        try:
            self.t.stop()
        except:
            pass
        if self.doorl == False and self.doorr == False and self.lightl == False and self.lightr == False and self.camon == False:
            self.usage = 9.6

        if self.doorl == True:
            self.usage -= 2.4
            
        if self.doorr == True:
            self.usage -= 2.4

        if self.lightl == True:
            self.usage -= 2.4

        if self.lightr == True:
            self.usage -= 2.4

        if self.camon == True:
            self.usage -= 2.4

        if self.usage <= 0:
            self.usage = 2.4
        self.t.start()
        
    def secoffice(self):
        self.recalculatePowUsage()
        print "----- %s" % (self.power)
        print "Security Office"
        if self.time == 0:
            print "----- 12 PM"
        else:
            print "----- %s AM" % (self.time)
        usrinput = raw_input("> ")                             #Asks for input
        if usrinput.lower() in ["power", "electricity", "energy"]:
            print "Power %s %s" % (self.power, "%")
            self.secoffice()

        if usrinput.lower() in ["cam", "sec cam", "security cam", "camera", "cams", "cm", "camer"]:
            self.camAsk()

        if usrinput.lower() in ["doorl", "left door", "ldoor", "door left", "doortleft", "leftdoor", "dl", "d l"]:
            if self.doorl == False:
                print "Closed left door."
                self.doorl = True
                exec("gdoorl = True")
                self.secoffice()

            else:
                print "Opened left door."
                self.doorl = False
                exec("gdoorl = False")
                self.secoffice()
                
        if usrinput.lower() in ["doorr", "right door", "rdoor", "door right", "doortright", "rightdoor", "d r", "dr"]:
            if self.doorr == False:
                print "Closed right door."
                self.doorr = True
                exec("gdoorr = True")
                self.secoffice()

            else:
                print "Opened right door."
                self.doorl = False
                exec("gdoorr = False")
                self.secoffice()

        if usrinput.lower() in ["lightl", "left light", "llight", "light left", "lightleft", "leftlight", "ll", "l l"]:
            if self.lightl == True:
                print "Left light is now OFF."
                self.lightl = False
                self.secoffice()
            else:
                self.lightl = True
                self.lightr = False
                print "Left light is now ON."
                for animatronic in animatronics:
                    if animatronic.location == "leftdoor":
                        print "%s is at the left door, looking at you." % (animatronic.name)
                self.secoffice()

        if usrinput.lower() in ["lightr", "right light", "rlight", "light right", "lightright", "rightlight", "lr", "l r"]:
            if self.lightr == True:
                print "Right light is now OFF."
                self.lightr = False
                self.secoffice()
            else:
                self.lightr = True
                self.lightl = False
                print "Right light is now ON."
                for animatronic in animatronics:
                    if animatronic.location == "rightdoor":
                        print "%s is at the right door, looking at you." % (animatronic.name)
                self.secoffice()


        else:
            print "What was that? Try again, please!"
            self.secoffice()

            
    def camAsk(self):
        print ""
        print "Cam list:"
        print " -- ".join(camsl)
        usrinput = raw_input("> ")
        self.recalculatetime()
        self.recalculatePowUsage()
        if usrinput.lower() in camsl:
            self.infoCam(usrinput)
            self.camAsk()
        if usrinput.lower() in ["exit", "close", "x", "e", "c"]:
            self.secoffice()
        if usrinput.lower() in ["time", "hour"]:
            if self.time == 0:
                print "It's 12 PM"
                self.camAsk()
            else:
                print "It's %s AM" % (self.time)
                self.camAsk()

        if usrinput.lower() in ["pow", "power", "electricity"]:
            print "%s %s power left" % (self.power, "%")
            self.camAsk()
        
        else:
            print "Unknown cam"
            self.camAsk()
    

    def checkAnimCam(self, cam):
        if cam == "cam6":
            for animatronic in animatronics:
                if animatronic.location == "cam6":
                    print "You hear some noise."
        else:    
            for animatronic in animatronics:
                if animatronic.location == cam:
                    print "%s is here." % (animatronic.name)
                
    
    def infoCam(self, cam):
        if cam == "cam1a":
            print "-----"
            print "Show Stage"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam1b":
            print "-----"
            print "Dining Area"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam2a":
            print "-----"
            print "West Hall"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam2b":
            print "-----"
            print "West Hall Corner"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam3":
            print "-----"
            print "Supply Closet"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam4a":
            print "-----"
            print "East Hall"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam4b":
            print "-----"
            print "East Hall Corner"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam5":
            print "-----"
            print "Backstage"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam6":
            print "-----"
            print "Kitchen -CAMERA DISABLED- (Audio only)"
            print "-----"
            self.checkAnimCam(cam)
        if cam == "cam7":
            print "-----"
            print "Restroom"
            print "-----"
            self.checkAnimCam(cam)

            

chicken = animatronic("Chicken", "chicken")
rabbit = animatronic("Rabbit", "rabbit")
animatronics = [chicken, rabbit]
m = main()







