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
debug = True
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
        self.kind = kind         #Kinds: Chicken / Rabbit / Bear (WIP) / Fox
        self.ailvl = ailvl       #AI LVL. 1 - 20. (1 Doesn't disable at all the animatronics, but makes them very inactive.)
        self.location = location #Locations can be: "cam1a" "cam1b" "cam1c" "cam2a" "cam2b" "cam3" "cam4a" "cam4b" "cam5" "cam6" "cam7"
        if self.kind == "fox":   #Fox kind variables.
            self.foxstatus = 0 #0 = Hiding. 1 = Peeking. 2 = Looking thro. 3 = Out 4 = About to sprint 5 = Got ya'!
            self.foxtseen = 0
            self.foxsleep = 0

        if self.kind == "bear":
            self.bsum = 0
            self.bseen = False

        if self.ailvl <= 20:
            debugprnt("%s's AI started. -%s KIND-" % (self.name, self.kind.upper()))
            if self.kind == "bear":
                if self.ailvl > 5:
                    debugprnt("%s's AI IS NOW ACTIVE! -%s KIND-" % (self.name, self.kind))
                    threading.Timer(1, self.think).start()

            if self.kind == "fox":
                threading.Timer(1, self.think).start()
            else:
                thread.start_new_thread(self.think, ()) #Multithreading.
        else:
            debugprnt("%s's AI lvl is too high! Shutting down... -%s BEHAVIOR-" % (self.name, self.kind))
            self.dmove("off")



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
        if self.location == "off": #Shuts down the AI
            debugprnt("%s's AI is shutting down." % (self.name))
            os.system("exit")
            sys.exit(0)
            os._exit(0)
        else:
            #Chicken's AI
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
                if self.location == "inside":
                    pass
                return None


            #Rabbit's AI
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
                if self.location == "inside":
                    pass

                return None

            #Fox's AI
            if self.kind == "fox":
                debugprnt("%s is thinking... -FOX BEHAVIOR- -%s-" % (self.name, self.location))
                time.sleep(1)
                if self.foxstatus == 4:
                    self.foxstatus = 5
                    debugprnt("%s is sprinting towards you!" % (self.name))
                    time.sleep(2)
                    self.location = "cam2a"
                    time.sleep(random.randint(1, 2))
                    self.location = "leftdoor"

                if self.foxstatus >= 5:
                    pass

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

            #Bear's AI
            if self.kind == "bear":
                if self.location == "cam1a":
                    for animatronic in animatronics:
                        if animatronic.location != "cam1a" and animatronic.kind != "bear":
                            self.bsum += 1
                            if self.bsum == len(animatronics):
                                time.sleep(random.randint(0, 3))
                                if self.bseen == False:
                                    if random.randint(0, 2) == 0:
                                        print "A deep laugh can be heard."
                                    self.rmove("cam1b")
                                else:
                                    self.think()

                if self.location == "cam1b":
                    time.sleep(random.randint(0, 3))
                    if self.bseen == False:
                        if random.randint(0, 2) == 0:
                            print "A deep laugh can be heard."
                        self.rmove("cam7")
                    else:
                        time.sleep(3)
                        self.think()

                if self.location == "cam7":
                    time.sleep(random.randint(2, 4))
                    if self.bseen == False:
                        if random.randint(0, 2) == 0:
                            print "A deep laugh can be heard."
                        self.rmove("cam6")
                    else:
                        time.sleep(random.randint(0, 2))
                        self.think()

                if self.location == "cam4a":
                    time.sleep(random.randint(1, 2))
                    if self.bseen == False:
                        if random.randint(0, 2) == 0:
                            print "A deep laugh can be heard."
                        self.rmove("cam4b")

                if self.location == "cam4b":
                    time.sleep(random.randint(0, 1))
                    if self.bseen == False:
                        if self.randint(0, 2) == 0:
                            print "A deep laugh can be heard."
                        self.rmove("leftdoor")

                if self.location == "leftdoor":
                    pass

                return None



class main(object):
    def __init__(self, power=100, time=0, sectohour=43, usage=9.6):
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
        self.power = power #Power
        self.killed = False #Killed or not
        self.usrinput = "" #User input. Used in self.securityOffice() and self.cam()
        self.time = time - 1 #The "-1" is because automatically the timer sums 1.
        self.sectohour = sectohour #Seconds needed for a IN-GAME hour
        self.usage = usage #Amount of seconds that has to pass for draining 1% power
        self.camon = False #False = Not viewing cams / True = Viewing
        self.noh = 0 #"No one here" var. Used for saying if there's someone in a cam or not.
        self.powerTimer() #Initialize the timers
        self.hourTimer()  #^
        thread.start_new_thread(self.checkDoorTimer, ())
        thread.start_new_thread(self.foxkindDoorCheck, ())
        self.securityOffice() #The main gameplay aspect

    def shutdown(self):
        debugprnt("Shutting down")
        for animatronic in animatronics:
            animatronic.dmove("off")
        sys.exit(0)
        os._exit(0)
        os.system("exit")

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

    def blackout(self): #Blackout event. yay
        for animatronic in animatronics:
            if animatronic.kind == "bear":
                print "Power went out..."
                time.sleep(random.randint(1, 8))
                os.system("cls")
                print "%s is at the left door." % (animatronic.name)
                print "A music box starts playing."
                time.sleep(random.randint(0, random.randint(1, 10)))
                os.system("cls")
                print "You see nothing at all."
                print "You hear steps."
                time.sleep(random.randint(1, 8))
                os.system("cls")
                if self.time != 6:
                    self.killed = True
                    print "%s jumps at you. Game over!" % (animatronic.name)
                    self.shutdown()
                else:
                    pass
                break

    #TIMERS#
    #These two timers work like this. 1: Do the action. 2: Make a new timer that repeats itself.

    def powerTimer(self): #Timer for the power.
        if self.power <= 0 - 1:
            self.blackout()
        else:
            self.power -= 1
        threading.Timer(self.usage, self.powerTimer).start()

    def hourTimer(self): #Timer for the IN-GAME time.
        if self.time >= 6 and self.killed != True:
            print "5AM --> 6AM"
            print "You survived!"
            self.shutdown()
        else:
            self.time += 1

        threading.Timer(self.sectohour, self.hourTimer).start()

    def checkDoorTimer(self): #Timer that checks if there are animatronics at the doors
        self.someonethere = False
        for animatronic in animatronics:
            time.sleep(10)
            if animatronic.location == "leftdoor" and animatronic.kind != "fox":
                if self.leftdoor == False:
                    if random.randint(0, 40) in range(0, animatronic.ailvl):
                        self.leftlight = "broken"
                        self.leftdoor = "broken"
                        debugprnt("%s broke the left light and door -%s BEHAVIOR-" % (animatronic.name, animatronic.kind.upper()))
                    animatronic.location = "inside"
                    debugprnt("%s is inside... -%s BEHAVIOR- -%s-" % (animatronic.name, animatronic.kind.upper(), animatronic.location))

                elif self.leftdoor == True and animatronic.kind != "fox": #This is what happens when you have your door closed
                    animatronic.rmove(["cam1a", "cam1b"]) #Direct-moves the animatronic to the starting location
                    debugprnt("%s should have left -%s BEHAVIOR- -%s-" % (animatronic.name, animatronic.kind.upper(), animatronic.location))

                else: #self.cam() should handle what happens if you're in "cam mode"
                    pass

            if animatronic.location == "rightdoor" and animatronic.kind != "bear":
                if self.rightdoor == False:
                    animatronic.location == "inside"
                    debugprnt("%s is inside... -%s BEHAVIOR- -%s-" % (animatronic.name, animatronic.kind.upper(), animatronic.location))

                elif self.rightdoor == True and animatronic.kind != "fox": #Handles what happens if you aren't in camera mode and you have the door closed
                    animatronic.rmove(["cam1a", "cam1b"]) #Direct-moves the animatronic to the starting location
                    debugprnt("%s should have left -%s BEHAVIOR- -%s-" % (animatronic.name, animatronic.kind.upper(), animatronic.location))


            if animatronic.location == "rightdoor" and animatronic.kind == "bear":
                if self.rightdoor == True:
                    self.rmove(["cam1b", "cam6", "cam7"])
                    debugprnt("%s should have left -%s BEHAVIOR- -%s-" % (animatronic.name, animatronic.kind.upper(), animatronic.location))
                else:
                    self.killed == True
                    animatronic.location == "inside"
                    print "%s jumps at you! %s got you... Game over." % (animatronic.name, animatronic.name)
                    self.shutdown()

            if self.rightdoor == True and self.leftdoor == True:
                for animatronic in animatronics:
                    if animatronic.location == "leftdoor" or "rightdoor":
                        self.someonethere == True #Random variable so Bear doesn't kill you if you have both doors closed but no one is there. (Idling)

                    if animatronic.kind == "bear" and animatronic.location != "cam4b" and animatronic.location != "rightdoor":
                        self.killed = True
                        print "%s jumps at you! %s got you... Game over." % (animatronic.name, animatronic.name)
                        self.shutdown()



            else:
                if self.time >= 6 or self.power <= 0 - 1:
                    pass
                else:
                    threading.Timer(5.0, self.checkDoorTimer).start()


    def foxkindDoorCheck(self):
        #debugprnt("Foxkind door check.")
        if self.time >= 6 or self.power <= 0 - 1:
            pass

        else:
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
                        self.killed = True
                        print "%s enters the room. %s got you..." % (animatronic.name, animatronic.name)
                        self.shutdown()
            threading.Timer(3.0, self.foxkindDoorCheck).start()


        #GAMEPLAY#
#Basically the security office and the cameras.

    def securityOffice(self): #-Almost- the most important thing in main. From here you can do EVERYTHING.
        if self.power < 0 or self.time >= 6 or self.killed == True: #Checks if there's a blackout/You survived/You're dead
            pass
        else: #Prints power, time...
            print "----- %s %s power left. After %s seconds, 1 %s power is lost." % (self.power, "%", self.usage, "%")
            print "Security Office"
            if self.time == 0:
                print "----- 12 PM" #I hate this time format.
            else:
                print "----- %s AM" % (self.time)

            #This is where input is asked.

            #Debug mode#
            self.usrinput = raw_input("> ").lower()
            if self.usrinput in ["debug", "debugmode"]:
                global debug
                if debug == True:
                    debug = False
                else:
                    debug = True
                debugprnt("If you see this, debug mode is now enabled!")
                self.securityOffice()
                return None
            #Power
            if self.usrinput in ["power", "electricity", "energy"]:
                print "Power left: %s %s" % (self.power, "%")
                self.securityOffice()
                return None #"Closes" the current security office.

            #Cameras
            if self.usrinput in ["cam", "sec cam", "security cam", "camera", "cams", "cm", "camer"]:
                self.usage -= 2.4
                self.camon = True
                self.cam()
                return None

            #Clears the window.
            if self.usrinput in ["clear", "cls"]:
                os.system("cls")
                self.securityOffice()
                return None

            #Left door
            if self.usrinput in ["doorl", "left door", "ldoor", "door left", "doortleft", "leftdoor", "dl", "d l"]:
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

                if self.leftdoor == "broken":
                    print "Left door doesn't work..."
                    self.securityOffice()
                    return None


            #Right door
            if self.usrinput in ["doorr", "right door", "rdoor", "door right", "doortright", "rightdoor", "d r", "dr"]:
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

                if self.rightdoor == "broken":
                    print "Right door doesn't work..."
                    self.securityOffice()
                    return None

            #Left light
            if self.usrinput in ["lightl", "left light", "llight", "light left", "lightleft", "leftlight", "ll", "l l"]:
                if self.leftlight == True:
                    print "Left light is now OFF."
                    self.leftlight = False
                    self.usage += 1.2
                    self.securityOffice()
                    return None

                if self.leftlight == False:
                    self.leftlight = True
                    if self.rightlight == True:
                        print "Right light is now OFF."
                        self.rightlight = False
                        self.usage += 1.2
                    self.usage -= 1.2
                    print "Left light is now ON."
                    self.foxkindDoorCheck()
                    for animatronic in animatronics:
                        if animatronic.location == "leftdoor":
                            print "%s is at the left door, looking at you." % (animatronic.name)
                    self.securityOffice()
                    return None

                if self.leftlight == "broken":
                    print "Left light doesn't work..."
                    self.securityOffice()
                    return None

            #Right light
            if self.usrinput in ["lightr", "right light", "rlight", "light right", "lightright", "rightlight", "lr", "l r"]:
                if self.rightlight == True:
                    print "Right light is now OFF."
                    self.rightlight = False
                    self.usage += 1.2
                    self.securityOffice()
                    return None

                if self.rightlight == False:
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

                if self.rightlight == "broken":
                    print "Right light doesn't work..."
                    self.securityOffice()
                    return None
            #Help
            if self.usrinput in ["help", "what do i do?", "?"]:
                print "-----"
                print "Hi! Welcome to pyDLASYIAS (pyDon't let animatronics stuff you in a suit)"
                print "It looks like you're asking for help."
                print "I'll help you!"
                print "Here's a command list:"
                print "'door left' 'door right' 'light left' 'light right' 'help' 'cam' 'clear'"
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
                if self.killed == False:
                    print "What was that? Try again, please!"
                    self.securityOffice()
                    return None
                else:
                    print "You're dead. You can close the game"
                    print "...but you can't escape"
                    self.shutdown()

    def cam(self): #Camera mode. You can watch the animatronics from here.
        if self.killed == True or self.time >= 6 or self.power == 0 - 1:
            pass
        else:
            for animatronic in animatronics:
                if animatronic.kind == "bear":
                    animatronic.bseen = True
            print "Cam list:"
            print " -- ".join(sorted(list(camdic))) #Wow. Just don't change it, it's magical...
            self.usrinput = raw_input("> ").lower()  #User input

            #Looks at a certain camera to see if something or someone is there.
            if self.usrinput in camdic.keys():
                print "----- %s %s power left. After %s seconds, 1 %s power is lost." % (self.power, "%", self.usage, "%")
                print camdic[self.usrinput] + " [Camera Mode]"
                if self.time == 0:
                    print "----- 12 PM"
                else:
                    print "----- %s AM" % (self.time)

                self.checkAnimCam(self.usrinput)
                self.cam()
                return None

            #Clears the window.
            if self.usrinput in ["clear", "cls"]:
                os.system("cls")
                self.cam()
                return None

            #Closes camera mode. Also handles certains game overs.
            if self.usrinput in ["exit", "close", "x", "e", "c"]:
                for animatronic in animatronics:
                    if animatronic.location == "inside" and animatronic.kind != "bear":
                        self.killed = True
                        print "%s screams at your face. %s got you! Game over." % (animatronic.name, animatronic.name)
                        self.shutdown()

                    else:
                        self.usage += 2.4
                        self.securityOffice()
                        return None
                        for animatronic in animatronics:
                            if animatronic.kind == "bear":
                                animatronic.bseen = False



            else:
                if self.killed == False:
                    print "Unknown cam"
                    self.cam()
                    return None
                else:
                    print "You're dead. You can close the game"
                    print "...but you can't escape"
                    self.shutdown()




    def hallucination(self, kind):
        if kind == "camkind":
            self.randhall = random.randint(0, 80)
            if self.randhall in range(0, self.ailvl):
                print "IT'S ME   "
                if random.randint(0, 2) == 1:
                    print "            IT'S        ME"
                elif random.randint(0, 2) == 2:
                    for animatronic in animatronics:
                        print "%s        is h e r e...?" % (animatronic.name)
                        print ""
                        print ""

    def checkAnimCam(self, cam):
        self.lac = 0 #Location animatronic count. Counts how many animatronics aren't in one room
        self.bcount = 0 #How many bears are in a game
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
                elif animatronic.location == cam and animatronic.kind != "fox":
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

        if cam == "cam1a":
            for animatronic in animatronics:
                if animatronic.location == cam:
                    print "%s is here." % (animatronic.name)

        else:
            for animatronic in animatronics:
                if animatronic.location == cam:
                    if animatronic.kind == "bear":
                        self.bcount += 1
                        continue
                    else:
                        print "%s is here." % (animatronic.name)
                else:
                    self.lac += 1
                if animatronic.kind == "bear" and self.lac == len(animatronics) - self.bcount and animatronic.location == cam:
                    print "%s is here" % (animatronic.name)


##OBJECTS AND ANIMATRONIC LIST##
fox = animatronic("Fox", "fox", 1, "cam1c")
rabbit = animatronic("Rabbit", "rabbit", 5,)
chicken = animatronic("Chicken", "chicken", 5)
bear = animatronic("Bear", "bear", 6)
animatronics = [rabbit, fox, chicken, bear] #Please edit this list with new animatronics if you want them to work. ALSO BEAR KIND SHOULD GO LAST.
m = main()
