import util, sys, os, time, random
from threading import Timer

class animatronic(object):
    def __init__(self, name, kind, ailvl=0, location="cam1a"): #Only change location for special animatronics
        self.name = name
        self.ailvl = ailvl
        self.location = location
        self.kind = kind
        #Special locations: leftdoor / rightdoor

    def move(self, adyacent=[]):
        self.choice = random.choice(adyacent)
        util.debugprnt("%s's choice was %s" % (self.name, self.choice))
        if random.randint(0, 25) in range(0, self.ailvl):
            self.location = self.choice
            util.debugprnt("%s moved to %s" % (self.name, self.location))
        else:
            util.debugprnt("%s didn't move at all" % (self.name))
            return None
        
    def think(self):
        #Chicken's AI / Also, this is very confusing
        if self.kind == "chicken":
            util.debugprnt("%s is thinking..." % (self.name))
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
            util.debugprnt("%s is thinking..." % (self.name))
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

chicken = animatronic("Chicken", "chicken")
rabbit = animatronic("Rabbit", "rabbit")

animatronics = [chicken, rabbit]
camsl = ["cam1a", "cam1b", "cam2a", "cam2b", "cam3", "cam4a", "cam4b", "cam5", "cam6", "cam7"]

#Above this comment: Animatronics' AI
#Below this comment: Main game / etc

class main(object):
    def __init__(self, doorl=False, doorr=False, lightl=False, lightr=False, power=100, usage=9.6):
        self.doorl = doorl
        self.doorr = doorr
        self.lightl = lightl
        self.lightr = lightr
        self.power = power
        self.usage = usage
        self.powTimer()
        self.secoffice()

    def powUsage(self):
        self.power -= 1
    
    def powTimer(self):
        t = Timer(long(self.usage), self.powUsage)
        t.start()
        
    def secoffice(self):
        usrinput = raw_input("> ")
        if usrinput.lower() in ["power", "electricity", "energy"]:
            print "Power %s %" % (self.power)
            self.secoffice()

        if usrinput.lower() in ["cam", "sec cam", "security cam", "camera", "cams"]:
            self.camAsk()


        else:
            print "What was that? Try again, please!"
            self.secoffice()

            
    def camAsk(self):
        print ""
        print "Cam list:"
        print " -- ".join(camsl)
        usrinput = raw_input("> ")
        if usrinput.lower() in camsl:
            self.infoCam(usrinput)
            camAsk()
        elif usrinput.lower() in ["exit", "close", "x", "e", "c"]:
            self.secoffice()
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





m = main()







