import sys, os, time, random, thread, threading

'''To be worked on:
-Better Hallucinations
-Better Bear kind.
-Better AI -?-
To be bugfixed:
-???
'''

##VARS##
debug = False
f = open("log.txt", "a")
f.write(time.strftime("\n %d/%m/%Y - %H:%M:%S \n"))

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

adjcam = {"cam1a" : ["cam1b"],                                #A dictionary for adjacent rooms.
          "cam1b" : ["cam1a", "cam1c", "cam5", "cam6", "cam7", "cam2a", "cam4a"],
          "cam5" : ["cam1b"],
          "cam6" : ["cam1b"],
          "cam7" : ["cam1b"],
          "cam2a" : ["cam2b", "cam3"],
          "cam3" : ["cam2a"],
          "cam2b" : ["inside", "cam2a"],
          "cam4a" : ["cam1b", "cam4b"],
          "cam4b" : ["cam4a", "inside"]}




##FUNCTIONS##
#Debug print. Prints a text if var debug is true.
def debugprnt(text):
    f.write(text + "\n")
    if debug == True:
        print text + "\n"
    else:
        pass

    return None

#CLS. Clears the window.
def cls():
    os.system("cls")
    return None

##CLASSES##
class animatronic(object):
    def __init__(self, name, kind, ailvl=20, location="cam1a"):
        self.name = name         #Obvious
        self.kind = kind         #Kinds: Chicken / Rabbit / Bear (WIP) / Fox
        self.ailvl = ailvl       #AI LVL. 1 - 20. (1 Doesn't disable at all the animatronics, but makes them very inactive.)
        self.location = location #Locations can be: "cam1a" "cam1b" "cam1c" "cam2a" "cam2b" "cam3" "cam4a" "cam4b" "cam5" "cam6" "cam7"
        self.slocation = location #Starting location
        if self.kind == "fox":   #Fox kind variables.
            self.foxstatus = 0 #0 = Hiding. 1 = Peeking. 2 = Looking thro. 3 = Out 4 = About to sprint 5 = Sprinting
            self.foxtseen = 0
            self.foxsleep = 0

        if self.kind == "bear":
            self.bsum = 0
            self.bseen = False

        if self.ailvl <= 20:
            debugprnt("%s's AI started. -%s KIND-" % (self.name, self.kind.upper()))
            if self.kind == "bear":
                if self.ailvl > 5:
                    debugprnt("%s's AI IS NOW ACTIVE! -%s KIND-" % (self.name, self.kind.upper()))
                    self.dmove("cam1a")
                    thread.start_new_thread(self.think, ())

            if self.kind == "fox":
                thread.start_new_thread(self.think, ())
            else:
                thread.start_new_thread(self.think, ()) #Multithreading.
        else:
            debugprnt("%s's AI lvl is too high! Shutting down... -%s BEHAVIOR-" % (self.name, self.kind.upper()))
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
                    debugprnt("%s is at rightdoor." % (self.name))
                    time.sleep(random.randint(15, 20))
                    self.rmove(["cam1a", "cam1b"])
                if self.location == "inside":
                    pass
                return None


            #Rabbit's AI
            if self.kind == "rabbit":
                debugprnt("%s is thinking... -RABBIT BEHAVIOR- -%s-" % (self.name, self.location))
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
                    debugprnt("%s is at leftdoor." % (self.name))
                if self.location == "inside":
                    pass
                return None

            #Fox's AI
            if self.kind == "fox":
                debugprnt("%s is thinking... -FOX BEHAVIOR- -%s-" % (self.name, self.location))
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.foxstatus == 4:
                    time.sleep(100 / self.ailvl)
                    self.foxstatus = 5


                if self.foxstatus >= 5:
                    debugprnt("%s is sprinting towards you! -FOX BEHAVIOR- -%s-" % (self.name, self.location))
                    time.sleep(20 / self.ailvl)
                    self.location = "cam2a"
                    time.sleep(20 / self.ailvl)
                    self.location = "leftdoor"

                if self.foxtseen >= 1:
                    debugprnt("%s status remains at %s -FOX BEHAVIOR- -%s-" % (self.name, self.foxstatus, self.location))
                    self.foxsleep += self.foxtseen
                    self.basesleep = random.randint(150, 200) / self.ailvl
                    self.foxtseen = 0
                    time.sleep(self.basesleep + self.foxsleep)
                    if random.randint(0, 1) == 1:
                        self.foxstatus += 1
                        debugprnt("%s status is now %s -FOX BEHAVIOR- -%s-" % (self.name, self.foxstatus, self.location))
                        self.think()
                    else:
                        debugprnt("%s status remains at %s -FOX BEHAVIOR- -%s-" % (self.name, self.foxstatus, self.location))
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
                debugprnt("FYI: Bear behavior doesn't *really* work. Be careful around this.")
                time.sleep(random.randint(20, 25) / self.ailvl)
                if self.location == "cam1a":
                    if self.someoneThere("cam1a") == True:
                        debugprnt("%s.bseen = %s -%s BEHAVIOR-" % (self.name, self.bseen, self.kind.upper()))
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


                return None


    def someoneThere(self, cam): #Function for bearkind. Duh.
        for animatronic in animatronics:
            if animatronic.kind == "bear":
                pass
            elif animatronic.location == cam:
                return True
        return False



class main(object):
    def __init__(self, gmode="custom", power=100, time=0, sectohour=43, usage=9.6):
        sys.setrecursionlimit(5000) #Magic.
        threading.stack_size(128*4096) #Magic.
        self.animlvlsum = 0
        self.gmode = gmode #Game mode. Normal / Custom (custom animatronics AI) / Survival (No time, no energy) / ???
        for animatronic in animatronics:
            self.animlvlsum += animatronic.ailvl
            self.ailvl = self.animlvlsum / len(animatronics) #This is the lvl of the night.
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
        if self.gmode != "survival": #Initialize the timers
            self.hourTimer()
        self.powerTimer()
        thread.start_new_thread(self.checkDoorTimer, ())
        thread.start_new_thread(self.foxkindDoorCheck, ())
        self.securityOffice() #The main gameplay aspect

    def shutdown(self): #Shuts down the whole game/Restarts it.
        debugprnt("Shutting down")
        for animatronic in animatronics:
            animatronic.dmove("off")
        sys.exit(0)
        os._exit(0)
        os.system("exit")

    def blackout(self): #Blackout event. yay
        for animatronic in animatronics:
            if animatronic.kind == "bear":
                print "Power went out..."
                time.sleep(random.randint(1, 8))
                cls()
                print "%s is at the left door." % (animatronic.name)
                print "A music box starts playing."
                time.sleep(random.randint(0, random.randint(1, 10)))
                cls()
                print "You see nothing at all."
                print "You hear steps."
                time.sleep(random.randint(1, random.randint(3, 8)))
                cls()
                if self.time != 6:
                    self.die(animatronic)
                    break

                else:
                    pass

        print "Power went out..."
        time.sleep(random.randint(1, 8))
        cls()
        print "Bear is at the left door."
        print "A music box starts playing."
        time.sleep(random.randint(0, random.randint(1, 10)))
        cls()
        print "You see nothing at all."
        print "You hear steps."
        time.sleep(random.randint(1, random.randint(3, 8)))
        cls()
        if self.time != 6:
            bear = "Bear", "bear"
            self.die(bear)


    #TIMERS#
    #These two timers work like this. 1: Do the action. 2: Make a new timer that repeats itself.

    def powerTimer(self): #Timer for the power.
        if self.power <= 0 - 1:
            self.blackout()
        else:
            self.power -= random.randint(1, 3) #Sorry for this. Power is too OP and I needed to nerf it.
            threading.Timer(self.usage, self.powerTimer).start()

    def hourTimer(self): #Timer for the IN-GAME time.
        if self.time >= 6 and self.killed != True:
            time.sleep(1)
            cls()
            print "5AM --> 6AM"
            print "You survived!"
            time.sleep(5)
            cls()
            if self.gmode == "custom":
                print "NOTICE OF TERMINATION:"
                print "Reason: Tampering with the animatronics."
                print "General unproffesionalism. Odor."
                print ""
                print "Thanks, mngmnt."
            if self.gmode == "overtime":
                print "Good job, sport!"
                print "(You've earned some overtime.)"
                print "You get 120.50$"
            else:
                print "Good job, sport!"
                print "(See you next week!)"
                print "You get 120$."
            self.shutdown()
        else:
            self.time += 1
            threading.Timer(self.sectohour, self.hourTimer).start()

    def checkDoorTimer(self): #"Timer" that checks if there are animatronics at the doors
            for animatronic in animatronics: #Checks for animatronics.
                time.sleep(20 / self.ailvl) #Waits an random amount of time.
                if animatronic.location in ["leftdoor", "rightdoor"] and animatronic.kind in ["rabbit", "chicken"]: #Checks if the animatronic is at leftdoor or at rightdoor and its kind isn't fox or bear.
                    if animatronic.location == "leftdoor" and self.leftdoor == False: #This is what happens if left door is open.
                        animatronic.dmove("inside") #Direct-moves the animatronic to "inside" location.
                        if self.ailvl > 12: #Checks if night level is over 12.
                            self.leftlight = "broken" #If so, brokes the left light and left door.
                            self.leftdoor = "broken"
                            debugprnt("%s broke the left light and door -%s BEHAVIOR-" % (animatronic.name, animatronic.kind.upper()))

                    if animatronic.location == "leftdoor" and self.leftdoor == True: #And this is what happens if the door is closed.
                        animatronic.rmove(["cam1a", "cam1b"]) #Random-moves the animatronic to cam1a or cam1b
                        debugprnt("%s should have left -%s BEHAVIOR- -%s-" % (animatronic.name, animatronic.kind.upper(), animatronic.location))

                    if animatronic.location == "rightdoor" and self.rightdoor == False: #All is the same as above.
                        animatronic.dmove("inside")
                        if self.ailvl > 12:
                            self.rightlight = "broken"
                            self.rightdoor = "broken"
                            debugprnt("%s broke the left light and door -%s BEHAVIOR-" % (animatronic.name, animatronic.kind.upper()))

                    if animatronic.location == "rightdoor" and self.rightdoor == True:
                        animatronic.rmove(["cam1a", "cam1b"])
                        debugprnt("%s should have left -%s BEHAVIOR- -%s-" % (animatronic.name, animatronic.kind.upper(), animatronic.location))

                    if self.time >= 6 or self.power <= 0:
                        pass
                    else:
                        self.checkDoorTimer()



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
                        self.die(animatronic)

            threading.Timer(3.0, self.foxkindDoorCheck).start()


        #GAMEPLAY#
#Basically the security office and the cameras.

    def securityOffice(self): #-Almost- the most important thing in main. From here you can do EVERYTHING.
        if self.power < 0 or self.time >= 6 or self.killed == True: #Checks if there's a blackout/You survived/You're dead
            pass
        else: #Prints power, time...
            print "----- %s %s power left. After %s seconds, 1 %s power is lost." % (self.power, "%", self.usage, "%")
            print "Security Office"
            if self.gmode == "survival":
                print "----- SURVIVAL MODE"

            if self.gmode != "survival" and self.time == 0:
                print "----- 12 PM" #I hate this time format

            if self.gmode != "survival" and self.time == 0:
                "----- %s AM" % (self.time)

        for animatronic in animatronics: #This for loop sets bearkind's bseen variable on false.
            if animatronic.kind == "bear":
                animatronic.bseen = False

            #This is where input is asked
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
                time.sleep(1)
                self.usage -= 2.4
                self.camon = True
                self.cam()
                return None

            #Clears the window.
            if self.usrinput in ["clear", "cls"]:
                cls()
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
                print "'door left' 'door right' 'light left' 'light right' 'help' 'cam' 'clear' 'state'"
                print "There's a few more commands (Similar words that do the same as the words above)"
                print "Oh and about the 'camera mode'"
                print "It's very easy to use. You type the camera name and you see if something or someone is there!"
                print "You can also use some commands there, like 'exit'"
                print "And that's all. Except for how to play, but you should know how to play already, so..."
                print "Good night!"
                print "-----"
                self.securityOffice()
                return None

            if self.usrinput in ["state", "doors", "lights", "door state", "light state"]:
                if self.leftdoor == True:
                    print "Left door is closed."
                else:
                    print "Left door is open."

                if self.rightdoor == True:
                    print "Right door is closed."
                else:
                    print "Right door is open."

                if self.leftlight == True:
                    print "Left light is on."
                else:
                    print "Left light is off."

                if self.rightlight == True:
                    print "Right light is on."
                else:
                    print "Right light is off."

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
                if self.gmode == "survival":
                    print "----- SURVIVAL MODE"

                if self.gmode != "survival" and self.time == 0:
                    print "----- 12 PM" #I hate this time format

                if self.gmode != "survival" and self.time != 0:
                    print "----- %s AM" % (self.time)

                self.checkAnimCam(self.usrinput)
                self.cam()
                return None

            #Clears the window.
            if self.usrinput in ["clear", "cls"]:
                cls()
                self.cam()
                return None

            #Closes camera mode. Also handles certains game overs.
            if self.usrinput in ["exit", "close", "x", "e", "c"]:
                time.sleep(1)
                for animatronic in animatronics: #Checks if there's "someone" inside...
                    if animatronic.location == "inside" and animatronic.kind != "bear":
                        self.die(animatronic)

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
                    print "...but the animatronics will wait for you"
                    self.shutdown()


    def die(self, animatronic):
        if animatronic.kind == "rabbit" or animatronic.kind == "chicken":
            self.killed = True
            time.sleep(1)
            cls()
            print "%s jumps at your face as a loud screech comes from the animatronic." % (animatronic.name)
            print "%s got you..." % (animatronic.name)
            print "Game over."
            self.shutdown()

        if animatronic.kind == "bear":
            self.killed = True
            time.sleep(1)
            cls()
            print "%s grabs you and jumps at your face. A really loud screech can be heard." % (animatronic.name)
            print "%s got you..." % (animatronic.name)
            print "Game over..."
            self.shutdown()

        if animatronic.kind == "fox":
            self.killed = True
            time.sleep(1)
            cls()
            print "%s enters the room as a loud screech can be heard." % (animatronic.name)
            print "%s got you..." % (animatronic.name)
            print "Game over..."
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
                        if random.randint(0, 1) == 1:
                            break
                        else:
                            print "%s        is h e r e...?" % (animatronic.name)
                            print "IT'S"
                            print "ME"


    def someoneThere(self, cam):
        for animatronic in animatronics:
            if animatronic.location == cam:
                return True
        return False


    def checkAnimCam(self, cam):
        if cam == "cam2a":
            for animatronic in animatronics:
                if animatronic.kind == "fox" and animatronic.foxstatus >= 4:
                    animatronic.foxstatus = 5
                    animatronic.think()
                    print "You see %s sprinting down the hall." % (animatronic.name)
                    time.sleep(1)
                    self.securityOffice()
                    return None
                if animatronic.location == cam and animatronic.kind != "fox":
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

                    if animatronic.foxstatus == 4:
                        print "%s is gone." % (animatronic.name)

        if cam == "cam1a":
            for animatronic in animatronics:
                if animatronic.location == cam:
                    print "%s is here." % (animatronic.name)

        if cam == "cam4b":
            for animatronic in animatronics:
                if animatronic.location == cam and animatronic.kind != "bear":
                    print "%s is here." % (animatronic.name)

                if animatronic.location == cam and animatronic.kind == "bear":
                    print "%s is looking directly to the camera." % (animatronic.name)

        elif cam not in ["cam1c", "cam1a", "cam4b", "cam6", "cam2a"]:
            for animatronic in animatronics:
                if animatronic.location == cam:
                    print "%s is here." % (animatronic.name)

def launcher():
    debug = False
    global animatronics
    print "pyDon't let animatronics stuff you in a suit -pyDLASYIAS-"
    print "1 - Custom night"
    print "2 - 20/20/20/20 mode"
    print "3 - Test option please ignore"
    inp = raw_input("> ")
    if inp == "1":
        belvl = raw_input("Input Bear's AI LVL: ")
        if belvl > 20:
            belvl = 20
        ralvl = raw_input("Input Rabbit's AI LVL: ")
        if ralvl > 20:
            ralvl = 20
        chilvl = raw_input("Input Chicken's AI LVL: ")
        if chilvl > 20:
            chilvl = 20
        folvl = raw_input("Input Fox's AI LVL: ")
        if folvl > 20:
            folvl = 20
        rabbit = animatronic("Rabbit", "rabbit", int(ralvl))
        chicken = animatronic("Chicken", "chicken", int(chilvl))
        fox = animatronic("Fox", "fox", int(folvl), "cam1c")
        bear = animatronic("Bear", "bear", int(belvl))
        animatronics = [rabbit, chicken, fox, bear]
        m = main("custom", 100, 0)

    if inp == "2":
        rabbit = animatronic("Rabbit", "rabbit", 20)
        chicken = animatronic("Chicken", "chicken", 20)
        fox = animatronic("Fox", "fox", 20, "cam1c")
        bear = animatronic("Bear", "bear", 20)
        animatronics = [rabbit, chicken, fox, bear]
        m = main("custom", 100, 0)

    if inp == "3":
        inp = raw_input("Input test mode code: ")
        if inp == "1": #Death debugging.
            rabbit = animatronic("Rabbit", "rabbit", 20, "inside")
            animatronics = [rabbit]
            m = main("custom", 10, 0)

        if inp == "2": #Bear behavior debugging.
            bear = animatronic("Bear", "bear", 20, "cam1a")
            animatronics = [bear]
            m = main("survival", 100, 0)

        else:
            print "Code invalid. Going back to the menu..."
            launcher()

    else:
        launcher()

launcher()
