import sys, os, time, random, thread, threading

'''To be worked on:
-Better Hallucinations
-Bear kind.
-"Inside" location. (So they don't automatically kill you) (Maybe I'll work in something like a branch. Dunno)
-Better AI -?-
To be bugfixed:
-???
'''

##VARS##
debug = False
camdic = {"cam1a" : "Stage Show",                             #A dictionary containing all cameras and their names."
          "cam1b" : "Dinning Area",
          "cam1c" : "Pirate Cove",
          "cam2a" : "West Hall",
          "cam2b" : "West Hall Corner",
          "cam3" : "Supply Closet",
          "cam4a" : "East Hall",
          "cam4b" : "East Hall Corner",
          "cam5" : "Backstage",
          "cam6" : "Kitchen -Camera Disabled- (AUDIO ONLY)",
          "cam7" : "Restrooms"}




##FUNCTIONS##
#Debug print. Prints a text if var debug is true.
def debugprnt(text):
    if debug == True:
        print text + "\n"
    else:
        pass




##CLASSES##
class animatronic(object):
    def __init__(self, name, kind, ailvl=20, location="cam1a"):
        self.name = name         #Obvious
        self.kind = kind         #Kinds: Chicken / Rabbit / Bear (Not functional yet) / Fox (Not functional yet)
        self.ailvl = ailvl       #AI LVL. 1 - 20. (1 Doesn't disable at all the animatronics, but makes them very inactive.)
        self.location = location #Locations can be: "cam1a" "cam1b" "cam1c" "cam2a" "cam2b" "cam3" "cam4a" "cam4b" "cam5" "cam6" "cam7"
        if self.kind == "fox":   #Fox kind variables.
            self.foxstatus = 0 #0 = Hiding. 1 = Peeking. 2 = Looking thro. 3 = Out 4 = About to sprint 5 = Got ya'!
            self.foxtseen = 0
            self.foxsleep = 0

        debugprnt("%s's AI started. -%s KIND-" % (self.name, self.kind.upper()))
        if self.kind != "fox":
            thread.start_new_thread(self.think, ()) #Multithreading.
        else:
            threading.Timer(1, self.think).start()


    def dmove(self, room): #Direct move / Debug move. Moves an animatronic to a location.
        self.location = room
        debugprnt("DMoved %s to %s" % (self.name, room))

    def rmove(self, adyacent): #Random move. Moves an animatronic to a random (adyacent) location.
        self.choice = random.choice(adyacent)
        debugprnt("%s's choice was %s" % (self.name, self.choice))
        if random.randint(0, 20) in range(0, self.ailvl):
            self.location = self.choice
            debugprnt("%s moved to %s" % (self.name, self.location))
            self.think()
            return None

        else:
            debugprnt("%s didn't move at all" % (self.name))
            self.think()
            return None


    def think(self):
        #Chicken's AI / Also, this is very confusing
        if self.kind == "chicken":
            debugprnt("%s is thinking... -CHICKEN BEHAVIOR- -%s-" % (self.name, self.location))
            time.sleep(3)
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
                debugprnt("%s is at rightdoor." % (self.name))
                time.sleep(random.randint(15, 20))
                self.dmove("cam1a")
            return None


        #Rabbit's AI / Confusing.
        if self.kind == "rabbit":
            debugprnt("%s is thinking... -RABBIT BEHAVIOR- -%s-" % (self.name, self.location))
            time.sleep(2)
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
                debugprnt("%s is at leftdoor." % (self.name))
                time.sleep(random.randint(15, 20))
                self.dmove("cam1a")
            return None

        #Fox's AI
        if self.kind == "fox":
            debugprnt("%s is thinking... -FOX BEHAVIOR- -%s-" % (self.name, self.location))
            time.sleep(1)
            if self.foxstatus == 4 or self.foxstatus == 5:
                self.foxstatus = 5
                debugprnt("%s is sprinting towards you!" % (self.name))
                time.sleep(2)
                self.location = "cam2a"
                time.sleep(random.randint(1, 2))
                self.location = "leftdoor"

            if self.foxtseen >= 1:
                debugprnt("%s status remains at %s" % (self.name, self.foxstatus))
                self.foxsleep += self.foxtseen
                self.basesleep = random.randint(150, 200) / self.ailvl
                self.foxtseen = 0
                time.sleep(self.basesleep + self.foxsleep)
                if random.randint(0, 1) == 1:
                    self.foxstatus += 1
                    debugprnt("%s status is now %s" % (self.name, self.foxstatus))
                    self.think()
                else:
                    debugprnt("%s status remains at %s" % (self.name, self.foxstatus))
                    self.think()



            else:
                if random.randint(0, 1) == 1:
                    self.foxstatus +=1
                    debugprnt("%s status is now %s" % (self.name, self.foxstatus))
                else:
                    debugprnt("%s status remains at %s" % (self.name, self.foxstatus))
                time.sleep(random.randint(150, 200) / self.ailvl)
                self.think()

            return None



class main(object):
    def __init__(self, power=100, time=0, sectohour=21.5, usage=9.6):
        sys.setrecursionlimit(5000) #Magic.
        threading.stack_size(128*4096) #Magic.
        self.animlvlsum = 0
        for animatronic in animatronics:
            self.animlvlsum += animatronic.ailvl
            self.ailvl = self.animlvlsum / len(animatronics)
        self.leftdoor = False #False = Open / True = Closed
        self.rightdoor = False #Same ^^^^^^^^^^^^^^
        self.leftlight = False #False = Off / True = On
        self.rightlight = False #Same ^^^^^^^^^^^^^
        self.power = power
        self.time = time - 1 #The "-1" is because automatically the timer sums 1.
        self.sectohour = sectohour #Seconds needed for a IN-GAME hour
        self.usage = usage #Amount of seconds that has to pass for draining 1% power
        self.camon = False #False = Not viewing cams / True = Viewing cams
        self.powerTimer() #Initialize the timers
        self.hourTimer()  #^
        thread.start_new_thread(self.checkDoorTimer, ())
        thread.start_new_thread(self.foxkindDoorCheck, ())
        self.securityOffice() #The main gameplay aspect


        #ETC#
        def blackout(self): #Not a timer but well...
            print "Power went out..."
            time.sleep(1, 5)
            print "Bear is at the left door."
            print "A music box starts playing."
            time.sleep(1, 20)
            print "You see nothing at all."
            print "You hear steps."
            time.sleep(1, 5)
            if self.time != 6:
                print "Bear jumps at you. Game over!"
                sys.exit(0)
                os._exit(0)



        #TIMERS#
#These two timers work like this. 1: Do the action. 2: Make a new timer that repeats itself.




    def powerTimer(self): #Timer for the power.
        self.power -= 1
        if self.power == 0 - 1:
            self.blackout()
        threading.Timer(self.usage, self.powerTimer).start()

    def hourTimer(self): #Timer for the IN-GAME time.
        self.time += 1
        if self.time == 6:
            print "5AM --> 6AM"
            print "You survived!"
            sys.exit(0)
            os._exit(0)
        threading.Timer(self.sectohour, self.hourTimer).start()

#This timer is different. This one is for checking if there are animatronics at the doors

    def checkDoorTimer(self): #Timer that checks if there are animatronics at the doors
        for animatronic in animatronics:
            time.sleep(10)
            if animatronic.location == "leftdoor" and animatronic.kind != "fox":
                if self.camon == False and self.leftdoor == False:
                    print "%s enters the security office. %s got you! Game over" % (animatronic.name, animatronic.name)
                    os.system('exit')
                    sys.exit(0)
                    os._exit(0)

                elif self.leftdoor == True and self.camon == False and animatronic.kind != "fox": #Handles what happens if you aren't in camera mode and you have the door closed
                    debugprnt("%s should have left" % (animatronic.name))
                    animatronic.dmove("cam1a") #Direct-moves the animatronic to the starting location

                else: #self.cam() should handle what happens if you're in "cam mode"
                    pass

            if animatronic.location == "rightdoor" and animatronic.kind != "fox":
                if self.camon == False and self.rightdoor == False:
                    print "%s enters the security office. %s got you! Game over" % (animatronic.name, animatronic.name)
                    sys.exit(0)
                    os._exit(0)

                elif self.rightdoor == True and self.camon == False and animatronic.kind != "fox": #Handles what happens if you aren't in camera mode and you have the door closed
                    animatronic.dmove("cam1a") #Direct-moves the animatronic to the starting location

                else: #self.cam() should handle what happens if you're in "cam mode"
                    pass
            else:
                threading.Timer(5.0, self.checkDoorTimer).start()

    def foxkindDoorCheck(self):
        debugprnt("Foxkind door check.")
        for animatronic in animatronics:
            if animatronic.location == "leftdoor" and animatronic.kind == "fox":
                if self.leftdoor == True:
                    print "%s bangs your door" % (animatronic.name)
                    self.powlost = random.randint(1, 15)
                    self.power -= self.powlost
                    print "You lost %s power" % (self.powlost)
                    animatronic.location = "cam1c"
                    animatronic.foxstatus = 0
                    animatronic.foxtseen = 0
                    time.sleep(1)
                    self.foxkindDoorCheck()
                else:
                    print "%s enters the room. %s got you..." % (animatronic.name, animatronic.name)
                    os.system('exit')
                    os._exit(0)
                    sys.exit(0)
            else:
                time.sleep(1)
                self.foxkindDoorCheck()


        #GAMEPLAY#
#Basically the security office and the cameras.

    def securityOffice(self): #-Almost- the most important thing in main. From here you can do EVERYTHING.
        #Prints power, time...

        print "----- %s %s power left. After %s seconds, 1 %s power is lost." % (self.power, "%", self.usage, "%")
        print "Security Office"
        if self.time == 0:
            print "----- 12 PM" #I hate this time format.
        else:
            print "----- %s AM" % (self.time)

        #Confusing part. This is where input is asked.

        usrinput = raw_input("> ")
        #Power
        if usrinput.lower() in ["power", "electricity", "energy"]:
            print "Power left: %s %s" % (self.power, "%")
            self.securityOffice()
            return None #"Closes" the current security office.

        #Cameras
        if usrinput.lower() in ["cam", "sec cam", "security cam", "camera", "cams", "cm", "camer"]:
            self.usage -= 2.4
            self.camon = True
            self.cam()
            return None

        #Left door
        if usrinput.lower() in ["doorl", "left door", "ldoor", "door left", "doortleft", "leftdoor", "dl", "d l"]:
            if self.leftdoor == False:
                print "Closed left door."
                self.leftdoor = True
                self.usage -= 2.4
                self.securityOffice()
                return None

            if self.leftdoor == True:
                print "Opened left door."
                self.leftdoor = False
                self.usage += 2.4
                self.securityOffice()
                return None

        #Right door
        if usrinput.lower() in ["doorr", "right door", "rdoor", "door right", "doortright", "rightdoor", "d r", "dr"]:
            if self.rightdoor == False:
                print "Closed right door."
                self.rightdoor = True
                self.usage -= 2.4
                self.securityOffice()
                return None

            if self.rightdoor == True:
                print "Opened right door."
                self.rightdoor = False
                self.usage += 2.4
                self.securityOffice()
                return None

        #Left light
        if usrinput.lower() in ["lightl", "left light", "llight", "light left", "lightleft", "leftlight", "ll", "l l"]:
            if self.leftlight == True:
                print "Left light is now OFF."
                self.leftlight = False
                self.usage += 1.2
                self.securityOffice()
                return None

            else:
                self.leftlight = True
                if self.rightlight == True:
                    print "Right light is now OFF."
                    self.rightlight = False
                    self.usage += 1.2
                self.usage -= 1.2
                print "Left light is now ON."
                for animatronic in animatronics:
                    if animatronic.location == "leftdoor":
                        print "%s is at the left door, looking at you." % (animatronic.name)
                self.securityOffice()
                return None

        #Right light
        if usrinput.lower() in ["lightr", "right light", "rlight", "light right", "lightright", "rightlight", "lr", "l r"]:
            if self.rightlight == True:
                print "Right light is now OFF."
                self.rightlight = False
                self.usage += 1.2
                self.securityOffice()
                return None

            else:
                self.rightlight = True
                if self.leftlight == True:
                    print "Left light is now OFF."
                    self.leftlight = False
                    self.usage += 1.2
                self.usage -= 1.2
                print "Right light is now ON."
                for animatronic in animatronics:
                    if animatronic.location == "rightdoor":
                        print "%s is at the right door, looking at you." % (animatronic.name)
                self.securityOffice()
                return None
        #Help
        if usrinput.lower() in ["help", "what do i do?", "?"]:
            print "-----"
            print "Hi! Welcome to pyDLASYIAS (pyDon't let animatronics stuff you in a suit)"
            print "It looks like you're asking for help."
            print "I'll help you!"
            print "Here's a command list:"
            print "'door left' 'door right' 'light left' 'light right' 'help' 'cam'"
            print "There's a few more commands (Similar words that do the same as the words above)"
            print "Oh and about the 'camera mode'"
            print "It's very easy to use. You type the camera name and you see if something or someone is there!"
            print "You can also use some commands there, like 'exit'"
            print "And that's all. Except for how to play, but you should know how to play already, so..."
            print "Good night!"
            print "-----"
            self.securityOffice()
            return None

        #Unknown command.
        else:
            print "What was that? Try again, please!"
            self.securityOffice()

    def cam(self): #Camera mode. You can watch the animatronics from here.
        print "Cam list:"
        print " -- ".join(sorted(list(camdic))) #Wow. Just don't change it, it's magical...
        usrinput = raw_input("> ").lower()  #User input

        #Looks at a certain camera to see if something or someone is there.
        if usrinput in camdic.keys():
            print "----- %s %s power left. After %s seconds, 1 %s power is lost." % (self.power, "%", self.usage, "%")
            print camdic[usrinput] + " [Camera Mode]"
            if self.time == 0:
                print "----- 12 PM"
            else:
                print "----- %s AM" % (self.time)

            self.checkAnimCam(usrinput)
            self.cam()
            return None

        #Closes camera mode. Also handles certains game overs.
        if usrinput in ["exit", "close", "x", "e", "c"]:
            for animatronic in animatronics:
                if animatronic.location == "leftdoor" and self.leftdoor == False:
                    print "%s screams at your face. %s got you! Game over." % (animatronic.name, animatronic.name)
                    sys.exit(0)
                    os._exit(0)

                if animatronic.location == "rightdoor" and self.rightdoor == False:
                    print "%s screams at your face. %s got you! Game over." % (animatronic.name, animatronic.name)
                    sys.exit(0)
                    os._exit(0)

                else:
                    self.usage += 2.4
                    self.securityOffice()
                    return None

        else:
            print "Unknown cam"
            self.cam()




    def hallucination(self, kind):
        if kind == "camkind":
            self.randhall = random.randint(0, 80)
            if self.randhall in range(0, self.ailvl):
                print "IT'S ME"
                if random.randint(0, 2) == 1:
                    print "IT'S        ME"
                elif random.randint(0, 2) == 2:
                    for animatronic in animatronics:
                        print "%s        is" % (animatronic.name)
                        print "h e r e...?"
                        print ""

    def checkAnimCam(self, cam):
        if cam == "cam6":
            for animatronic in animatronics:
                if animatronic.location == "cam6":
                    if animatronic.kind == "bear": #Yes. Not even implemented
                        print "A music box is playing."
                    else:
                        print "You hear some noise."

        if cam == "cam2a":
            for animatronic in animatronics:
                if animatronic.kind == "fox" and animatronic.foxstatus >= 4:
                    print "You see %s sprinting down the hall." % (animatronic.name)
                elif animatronic.location == cam and self.kind != "fox":
                    self.hallucination("camkind")
                    print "%s is here." % (animatronic.name)

        if cam == "cam1c":
            for animatronic in animatronics:
                if animatronic.location == cam and animatronic.kind == "fox":
                    animatronic.foxtseen += 1
                    if animatronic.foxstatus <= 0:
                        print "%s is hiding behind the curtain." % (animatronic.name)

                    if animatronic.foxstatus == 1:
                        print "%s is peeking through the curtain." % (animatronic.name)

                    if animatronic.foxstatus == 2:
                        print "%s is looking through the curtain." % (animatronic.name)

                    if animatronic.foxstatus == 3:
                        print "%s is out." % (animatronic.name)

        else:
            for animatronic in animatronics:
                if animatronic.location == cam:
                    self.hallucination("camkind")
                    print "%s is here." % (animatronic.name)





##OBJECTS AND ANIMATRONIC LIST##
fox = animatronic("Fox", "fox", 1, "cam1c")
rabbit = animatronic("Rabbit", "rabbit", 1)
chicken = animatronic("Chicken", "chicken", 1)


animatronics = [fox, rabbit, chicken] #Please edit this list with new animatronics if you want them to work.

m = main()
