#!/usr/bin/env python
import sys
import os
import time
import random
import _thread
import threading
import pygame
import pyDLASYIAS.sprite as sprite
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.utils.debug as debug
import pyDLASYIAS.utils.cls as cls
from pygame.locals import *

class main(object):
    def __init__(self, gmode="custom", power=100, time=0, sectohour=86, width=1600, height=720, fps=30):
        debug.debugprint("pyDLASYIAS %s started. Setting up game variables..." % (Globals.version))

        sys.setrecursionlimit(5000) #Magic.
        threading.stack_size(128*4096) #Magic.

        self.animlvlsum = 0
        self.gmode = gmode #Game mode. Normal / Custom (custom animatronics AI) / Survival (No time, no energy) / ???

        for animatronic in Globals.animatronics:
            self.animlvlsum += animatronic.ailvl
            self.ailvl = self.animlvlsum / len(Globals.animatronics) #This is the lvl of the night.
        del self.animlvlsum

        self.leftdoor = False #False = Open / True = Closed
        self.rightdoor = False #Same ^^^^^^^^^^^^^^
        self.leftlight = False #False = Off / True = On
        self.rightlight = False #Same ^^^^^^^^^^^^^
        self.power = power #Power. Int variable
        self.killed = False #False = Alive / True = Dead.
        self.usrinput = "" #User input. Used in self.securityOffice() and self.cam()
        self.time = time - 1 #The "-1" is there because the timer automatically sums 1 to the variable.
        self.sectohour = sectohour #Seconds needed for a IN-GAME hour
        self.usage = 1 #1 Usage: 9.6 / 2 Usage: 4.8 / 3 Usage: 2.8 - 2.9 - 3.9 / 4 Usage: 1.9 - 2.9
        self.scene = "office" #Scene. Used for knowing what sprites needs to be printed. SCENES: "office", "cam"
        self.lastcam = "cam1a"

        if self.gmode != "survival": #Initializes the hour timer if the gamemode isn't survival.
            threading.Timer(0.1, self.hourTimer).start()

        threading.Timer(0.1, self.powerTimer).start() #Power timer.

        _thread.start_new_thread(self.checkDoorTimer, ()) #These two threads checks if there's animatronics at the left or right doors and moves them into your office.

        _thread.start_new_thread(self.foxkindDoorCheck, ())


        self.width = width
        self.height = height
        self.running = True
        self.fps = fps

        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption("--pyDLASYIAS %s--" %(Globals.version))

        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()

        self.allgroup = pygame.sprite.Group()
        self.officegroup = pygame.sprite.Group()
        self.camgroup = pygame.sprite.Group()

        self.leftButton = sprite.Sprite(startpos=(1, 180), image="lb")
        self.leftButton.groups = self.allgroup, self.officegroup

        self.rightButton = sprite.Sprite(startpos=(1500, 180), image="rb")
        self.rightButton.groups = self.allgroup, self.officegroup

        self.camButton = sprite.Sprite(startpos=(530, 578), image="cambutton")
        self.camButton.groups = self.allgroup, self.officegroup, self.camgroup

        self.map = sprite.Sprite(startpos=(1200, 350), image="map")
        self.map.groups = self.allgroup, self.camgroup

        self.bg = sprite.Sprite("office", (0,0))

        self.mousex = 0
        self.mousey = 0
        self.mouseClick = False

        while self.running:

            self.mouseClick = False

            for event in pygame.event.get():

                print(event)

                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    self.shutdown()

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    self.mousex, self.mousey = event.pos
                    self.mouseClick = True

            if self.scene == "office":

                self.allgroup.add(self.leftButton)
                self.allgroup.add(self.rightButton)
                self.allgroup.add(self.camButton)

                self.officegroup.add(self.leftButton)
                self.officegroup.add(self.rightButton)
                self.officegroup.add(self.camButton)

                if self.mouseClick:
                    if self.mousex in range(32,69) and self.mousey in range(314,362):
                        print("TBC WITH PYDLASYIAS' LEFT LIGHT FUNCT. (%s, %s)" %(self.mousex,self.mousey))
                        self.leftLight()

                    if self.mousex in range(34,69) and self.mousey in range(232,285):
                        print("TBC WITH PYDLASYIAS' LEFT DOOR FUNCT. (%s, %s)" %(self.mousex,self.mousey))
                        self.leftDoor()

                    if self.mousex in range(1525,1559) and self.mousey in range(313,364):
                        print("TBC WITH PYDLASYIAS' RIGHT LIGHT FUNCT. (%s, %s)" %(self.mousex,self.mousey))
                        self.rightLight()

                    if self.mousex in range(1524,1559) and self.mousey in range(236,283):
                        print("TBC WITH PYDLASYIAS' RIGHT DOOR FUNCT. (%s, %s)" %(self.mousex,self.mousey))
                        self.rightDoor()

                    if self.mousex in range(674,683) and self.mousey in range(236,240):
                        print("Honk! (%s, %s)" % (self.mousex,self.mousey))

                if self.mousex in range(532,1127) and self.mousey in range(588,630):
                    print("TBC WITH CAMERA!!! (%s, %s)" %(self.mousex,self.mousey))
                    self.openCamera()

                if not self.leftlight and not self.rightlight:
                    self.bg.changeImg("office")
                    self.screen.blit(self.bg.image, self.bg.rect)

                elif self.leftlight and not self.rightlight or self.rightlight == "broken":
                    if self.somebodyThere("leftdoor") == True:
                        self.bg.changeImg("officela")
                        self.screen.blit(self.bg.image, self.bg.rect)
                    else:
                        self.bg.changeImg("officel")
                        self.screen.blit(self.bg.image, self.bg.rect)

                elif not self.leftlight and self.rightlight or self.leftlight == "broken":
                    if self.somebodyThere("rightdoor"):
                        self.bg.changeImg("officera")
                        self.screen.blit(self.bg.image, self.bg.rect)
                    elif not self.somebodyThere("rightdoor"):
                        self.bg.changeImg("officer")
                        self.screen.blit(self.bg.image, self.bg.rect)




                self.officegroup.draw(self.screen)
                self.officegroup.update()

                if self.leftdoor == "broken" or self.leftlight == "broken":
                    self.leftButton.changeImg("lb")
                    self.bg.changeImg("office")
                    self.screen.blit(self.bg.image, self.bg.rect)
                    self.officegroup.draw(self.screen)
                elif self.leftdoor and self.leftlight:
                    self.leftButton.changeImg("lbb")
                elif self.leftdoor and not self.leftlight:
                    self.leftButton.changeImg("lbdc")
                elif self.leftlight and not self.leftdoor:
                    self.leftButton.changeImg("lbl")
                elif not self.leftdoor and not self.leftlight:
                    self.leftButton.changeImg("lb")

                if self.rightdoor == "broken" or self.rightlight == "broken":
                    self.rightButton.changeImg("rb")
                    self.bg.changeImg("office")
                    self.screen.blit(self.bg.image, self.bg.rect)
                    self.officegroup.draw(self.screen)
                elif self.rightdoor and self.rightlight:
                    self.rightButton.changeImg("rbb")
                elif self.rightdoor and not self.rightlight:
                    self.rightButton.changeImg("rbdc")
                elif self.rightlight and not self.rightdoor:
                    self.rightButton.changeImg("rbl")
                elif not self.rightdoor and not self.rightlight:
                    self.rightButton.changeImg("rb")


            elif self.scene == "cam":
                self.camgroup.add(self.camButton)
                self.camgroup.add(self.map)

                self.camgroup.draw(self.screen)
                self.camgroup.update()

                if self.lastcam == "cam1a":
                    if Globals.animatronics[0].location == "cam1a" and Globals.animatronics[1].location == "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cam1aA-1")
                        self.screen.blit(self.bg.image, self.bg.rect)
                        pygame.display.flip()

                    if Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location == "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cam1aBC")
                        self.screen.blit(self.bg.image, self.bg.rect)
                        pygame.display.flip()

                    if Globals.animatronics[0].location == "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cam1aBR")
                        self.screen.blit(self.bg.image, self.bg.rect)
                        pygame.display.flip()

                    if Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cam1aB-1")
                        self.screen.blit(self.bg.image, self.bg.rect)
                        pygame.display.flip()

                if self.mousex in range(532,1127) and self.mousey in range(588,630):
                    print("TBC WITH CAMERA!!! (%s, %s)" %(self.mousex,self.mousey))
                    self.securityOffice()

            pygame.display.update()
            pygame.display.flip()
            self.FPSCLOCK.tick(self.fps)

    def shutdown(self): #Shuts down the whole game.
        debug.debugprint("Shutting down...")
        for animatronic in Globals.animatronics:
            animatronic.dmove("off")
        sys.exit(0)
        os._exit(0)
        pygame.quit()
        os.system("exit")

    def blackout(self): #Blackout event. yay
        for animatronic in Globals.animatronics:
            if animatronic.kind == "bear":
                print("")
                print("Power went out...")
                cls.cls(random.randint(2, 7), random.randint(0, 2))
                print("%s is at the left door." % (animatronic.name))
                print("A music box starts playing.")
                cls.cls(random.randint(2, 10))
                print("You see nothing at all.")
                print("You hear steps.")
                cls.cls(random.randint(3, 8))
                if self.time != 6:
                    self.die(animatronic)
                    break
                else:
                    pass

    def powerTimer(self): #Timer for the power.
        if self.killed == True or self.time >= 6 or self.power == 0 - 1: #Checks if the game has finished
            pass
        else:
            if self.power <= 0 - 1:
                self.blackout()
            else:
                if self.power < 30:
                    for animatronic in Globals.animatronics:
                        if animatronic.agressiveness != 3:
                            animatronic.agressiveness = 2
                if self.power < 15:
                    for animatronic in Globals.animatronics:
                        animatronic.agressiveness = 3
                self.power -= 1
                #threading.Timer(int(self.usage), self.powerTimer).start()
                if self.usage == 1:
                    threading.Timer(9.6, self.powerTimer).start()
                elif self.usage == 2:
                    threading.Timer(4.8, self.powerTimer).start()
                elif self.usage == 3:
                    threading.Timer(random.choice([2.8, 2.9, 3.9]), self.powerTimer).start()
                elif self.usage >= 4:
                    threading.Timer(random.choice([1.9, 2.9]), self.powerTimer).start()
        return None

    def hourTimer(self): #Timer for the IN-GAME time.
        if self.time >= 6 and self.killed != True: #This is what happens after 6AM. Yay!
            cls.cls(0.5, 0.5)
            print("5AM --> 6AM")
            print("You survived!")
            cls.cls(4.5, 0.5)
            if self.gmode == "custom":
                print("NOTICE OF TERMINATION:")
                print("(You're fired)")
                print("Reason: Tampering with the animatronics.")
                print("General unproffesionalism. Odor.")
                print("")
                print("Thanks, mngmnt.")
            elif self.gmode == "overtime":
                print("Good job, sport!")
                print("(You've earned some overtime.)")
                print("You get 120.50$")
            else:
                print("Good job, sport!")
                print("(See you next week!)")
                print("You get 120$")
            self.shutdown()

        else:
            self.time += 1
            if self.time == 1:
                for animatronic in Globals.animatronics:
                    if animatronic.agressiveness < 2:
                        animatronic.agressiveness = 1

            if self.time == 3:
                for animatronic in Globals.animatronics:
                    if animatronic.agressiveness < 3:
                        animatronic.agressiveness = 2

            if self.time == 5:
                for animatronic in Globals.animatronics:
                    animatronic.agressiveness = 3
            threading.Timer(self.sectohour, self.hourTimer).start()
        return None

    def checkDoorTimer(self): #"Timer" that checks if there are animatronics at the doors
        for animatronic in Globals.animatronics: #Checks for animatronics
            if animatronic.location == "leftdoor": #If animatronic is at left door
                time.sleep(20 / animatronic.ailvl)
                if self.leftdoor: #If leftdoor is closed
                    animatronic.rmove(["cam1b"]) #Go back to cam1b or not

                if not self.leftdoor: #Else if leftdoor is open
                    time.sleep(20 / animatronic.ailvl)
                    animatronic.rmove(["inside"]) #Random move the animatronic inside or not.
                    if self.ailvl > 12 and animatronic.location == "inside": #If AILVL is over 12 and the animatronic is inside...
                        self.leftlight = "broken" #Break the light and door
                        self.leftdoor = "broken"

            if animatronic.location == "rightdoor":
                time.sleep(20 / animatronic.ailvl)
                if self.rightdoor == True:
                    animatronic.rmove(["cam1b"])


                else:
                    time.sleep(20 / animatronic.ailvl)
                    animatronic.rmove(["inside"])
                    if self.ailvl > 12 and animatronic.location == "inside":
                        self.rightlight = "broken"
                        self.rightdoor = "broken"

        if self.time >= 6 or self.power <= 0:
            pass
        else:
            time.sleep(20 / self.ailvl)
            self.checkDoorTimer()
        return None


    def foxkindDoorCheck(self):
        #debug.debugprint(("Foxkind door check.")
        if self.time >= 6 or self.power <= 0 - 1:
            pass

        else:
            for animatronic in Globals.animatronics:
                if animatronic.location == "leftdoor" and animatronic.kind == "fox":
                    if self.leftdoor == True:
                        print("%s bangs your door" % (animatronic.name))
                        self.powlost = random.randint(1, 15)
                        self.power -= self.powlost
                        print("You lost %s power" % (self.powlost))
                        animatronic.location = "cam1c"
                        animatronic.foxstatus = 0
                        animatronic.foxtseen = 0
                        time.sleep(1)
                        self.foxkindDoorCheck()
                    else:
                        self.die(animatronic)

            threading.Timer(3.0, self.foxkindDoorCheck).start()

    def leftDoor(self):
        if self.leftdoor == False:
            print("Closed left door.")
            self.leftdoor = True
            self.usage += 1
            self.securityOffice()
            return None
            #
        if self.leftdoor == True:
            print("Opened left door.")
            self.leftdoor = False
            self.usage -= 1
            self.securityOffice()
            return None
            #
        if self.leftdoor == "broken":
            print("Left door doesn't work...")
            self.securityOffice()
            return None

    def leftLight(self):
        if self.leftlight == True:
            print("Left light is now OFF.")
            self.leftlight = False
            self.usage -= 1
            self.securityOffice()
            return None

        if self.leftlight == False:
            self.leftlight = True
            if self.rightlight == True:
                print("Right light is now OFF.")
                self.rightlight = False
                self.usage -= 1
            self.usage += 1
            print("Left light is now ON.")
            self.foxkindDoorCheck()
            for animatronic in Globals.animatronics:
                if animatronic.location == "leftdoor":
                    print("%s is at the left door, looking at you." % (animatronic.name))
            self.securityOffice()
            return None

        if self.leftlight == "broken":
            print("Left light doesn't work...")
            self.securityOffice()
            return None

    def rightDoor(self):
        if self.rightdoor == False:
            print("Closed right door.")
            self.rightdoor = True
            self.usage += 1
            self.securityOffice()
            return None

        if self.rightdoor == True:
            print("Opened right door.")
            self.rightdoor = False
            self.usage -= 1
            self.securityOffice()
            return None

        if self.rightdoor == "broken":
            print("Right door doesn't work...")
            self.securityOffice()
            return None

    def rightLight(self):
        if self.rightlight == True:
            print("Right light is now OFF.")
            self.rightlight = False
            self.usage -= 1
            self.securityOffice()
            return None

        if self.rightlight == False:
            self.rightlight = True
            if self.leftlight == True:
                print("Left light is now OFF.")
                self.leftlight = False
                self.usage -= 1
            self.usage += 1
            print("Right light is now ON.")
            for animatronic in Globals.animatronics:
                if animatronic.location == "rightdoor":
                    print("%s is at the right door, looking at you." % (animatronic.name))
            self.securityOffice()
            return None

        if self.rightlight == "broken":
            print("Right light doesn't work...")
            self.securityOffice()
            return None

    def openCamera(self):
        debug.debugprint("Open camera")
        if self.leftlight:
            self.usage -= 1
            self.leftlight = False
        if self.rightlight:
            self.usage -= 1
            self.rightlight = False
        self.usage += 1
        self.scene = "cam"
        debug.debugprint("Camera opened")
        return None

    def somebodyThere(self, camera):
        for animatronic in Globals.animatronics:
            if animatronic.location == str(camera):
                return True
        return False

    def securityOffice(self):
        debug.debugprint("Go back into office")
        self.usage -= 1
        self.scene = "office"
        debug.debugprint("Back into office")
        return None


    # def securityOffice(self): #-Almost- the most important thing in main. From here you can do EVERYTHING.
    #     if self.power < 0 or self.time >= 6 or self.killed == True: #Checks if there's a blackout/You survived/You're dead
    #         pass
    #     else: #Prints power, time...
    #         print("----- %s %s power left. Usage: %s" % (self.power, "%", self.usage))
    #         print("Security Office")
    #         if self.gmode == "survival":
    #             print("----- SURVIVAL MODE")
    #
    #         else:
    #             if self.time == 0:
    #                 print("----- 12 PM") #I hate this time format
    #
    #             else:
    #                 print("----- %s AM" % (self.time))
    #
    #         for animatronic in Globals.animatronics: #This for loop sets bearkind's bseen variable on false.
    #             if animatronic.kind == "bear":
    #                 animatronic.bseen = False
    #
    #         self.usrinput = input("> ").lower()
    #
    #         if self.usrinput in ["debug", "debugmode"]:
    #             if Globals.debug == True:
    #                 Globals.debug = False
    #             else:
    #                 Globals.debug = True
    #             self.securityOffice()
    #             return None
    #         #Power
    #         if self.usrinput in ["power", "electricity", "energy"]:
    #             print("Power left: %s %s" % (self.power, "%"))
    #             self.securityOffice()
    #             return None #"Closes" the current security office.
    #
    #         #Cameras
    #         if self.usrinput in ["cam", "sec cam", "security cam", "camera", "cams", "cm", "cameras"]:
    #             if self.leftlight == True:
    #                 self.usage -= 1
    #                 self.leftlight = False
    #             if self.rightlight == True:
    #                 self.usage -= 1
    #                 self.rightlight = False
    #             cls.cls(0.5, 0.5)
    #             self.usage += 1
    #             self.camon = True
    #             self.cam()
    #             return None
    #
    #         #Clears the window.
    #         if self.usrinput in ["clear", "cls"]:
    #             cls.cls()
    #             self.securityOffice()
    #             return None
    #
    #         #Left door
    #         if self.usrinput in ["doorl", "left door", "ldoor", "door left", "doortleft", "leftdoor", "dl", "d l"]:
    #             if self.leftdoor == False:
    #                 print("Closed left door.")
    #                 self.leftdoor = True
    #                 self.usage += 1
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.leftdoor == True:
    #                 print("Opened left door.")
    #                 self.leftdoor = False
    #                 self.usage -= 1
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.leftdoor == "broken":
    #                 print("Left door doesn't work...")
    #                 self.securityOffice()
    #                 return None
    #
    #
    #         #Right door
    #         if self.usrinput in ["doorr", "right door", "rdoor", "door right", "doortright", "rightdoor", "d r", "dr"]:
    #             if self.rightdoor == False:
    #                 print("Closed right door.")
    #                 self.rightdoor = True
    #                 self.usage += 1
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.rightdoor == True:
    #                 print("Opened right door.")
    #                 self.rightdoor = False
    #                 self.usage -= 1
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.rightdoor == "broken":
    #                 print("Right door doesn't work...")
    #                 self.securityOffice()
    #                 return None
    #
    #         #Left light
    #         if self.usrinput in ["lightl", "left light", "llight", "light left", "lightleft", "leftlight", "ll", "l l"]:
    #             if self.leftlight == True:
    #                 print("Left light is now OFF.")
    #                 self.leftlight = False
    #                 self.usage -= 1
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.leftlight == False:
    #                 self.leftlight = True
    #                 if self.rightlight == True:
    #                     print("Right light is now OFF.")
    #                     self.rightlight = False
    #                     self.usage -= 1
    #                 self.usage += 1
    #                 print("Left light is now ON.")
    #                 self.foxkindDoorCheck()
    #                 for animatronic in Globals.animatronics:
    #                     if animatronic.location == "leftdoor":
    #                         print("%s is at the left door, looking at you." % (animatronic.name))
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.leftlight == "broken":
    #                 print("Left light doesn't work...")
    #                 self.securityOffice()
    #                 return None
    #
    #         #Right light
    #         if self.usrinput in ["lightr", "right light", "rlight", "light right", "lightright", "rightlight", "lr", "l r"]:
    #             if self.rightlight == True:
    #                 print("Right light is now OFF.")
    #                 self.rightlight = False
    #                 self.usage -= 1
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.rightlight == False:
    #                 self.rightlight = True
    #                 if self.leftlight == True:
    #                     print("Left light is now OFF.")
    #                     self.leftlight = False
    #                     self.usage -= 1
    #                 self.usage += 1
    #                 print("Right light is now ON.")
    #                 for animatronic in Globals.animatronics:
    #                     if animatronic.location == "rightdoor":
    #                         print("%s is at the right door, looking at you." % (animatronic.name))
    #                 self.securityOffice()
    #                 return None
    #
    #             if self.rightlight == "broken":
    #                 print("Right light doesn't work...")
    #                 self.securityOffice()
    #                 return None
    #         #Help
    #         if self.usrinput in ["help", "what do i do?", "?"]:
    #             print("-----")
    #             print("Hi! Welcome to pyDLASYIAS (pyDon't let animatronics stuff you in a suit)")
    #             print("It looks like you're asking for help.")
    #             print("I'll help you!")
    #             print("Here's a command list:")
    #             print("'door left' 'door right' 'light left' 'light right' 'help' 'cam' 'clear' 'state'")
    #             print("There's a few more commands (Similar words that do the same as the words above)")
    #             print("Oh and about the 'camera mode'")
    #             print("It's very easy to use. You type the camera name and you see if something or someone is there!")
    #             print("You can also use some commands there, like 'exit'")
    #             print("And that's all. Except for how to play, but you should know how to play already, so...")
    #             print("Good night!")
    #             print("-----")
    #             self.securityOffice()
    #             return None
    #
    #         if self.usrinput in ["state", "doors", "lights", "door state", "light state"]:
    #             if self.leftdoor == True:
    #                 print("Left door is closed.")
    #             else:
    #                 print("Left door is open.")
    #
    #             if self.rightdoor == True:
    #                 print("Right door is closed.")
    #             else:
    #                 print("Right door is open.")
    #
    #             if self.leftlight == True:
    #                 print("Left light is on.")
    #             else:
    #                 print("Left light is off.")
    #
    #             if self.rightlight == True:
    #                 print("Right light is on.")
    #             else:
    #                 print("Right light is off.")
    #
    #             self.securityOffice()
    #             return None
    #
    #         #Unknown command.
    #         else:
    #             if self.killed == False:
    #                 print("What was that? Try again, please!")
    #                 self.securityOffice()
    #                 return None
    #             else:
    #                 print("You're dead. You can close the game now.")
    #                 print("...but you can't escape")
    #                 self.shutdown()
    #
    # def cam(self): #Camera mode. You can watch the animatronics from here.
    #     if self.killed == True or self.time >= 6 or self.power == 0 - 1:
    #         pass
    #     else:
    #         for animatronic in Globals.animatronics:
    #             if animatronic.kind == "bear":
    #                 animatronic.bseen = True
    #         print("Cam list:")
    #         print(" -- ".join(sorted(list(Globals.camdic)))) #Wow. Just don't change it, it's magical...
    #         self.usrinput = input("> ").lower()  #User input
    #
    #         #Looks at a certain camera to see if something or someone is there.
    #         if self.usrinput in list(Globals.camdic.keys()):
    #             print("----- %s %s power left. Usage: %s" % (self.power, "%", self.usage))
    #             print(Globals.camdic[self.usrinput] + " [Camera Mode]")
    #             if self.gmode == "survival":
    #                 print("----- SURVIVAL MODE")
    #
    #             if self.gmode != "survival" and self.time == 0:
    #                 print("----- 12 PM") #I hate this time format
    #
    #             if self.gmode != "survival" and self.time != 0:
    #                 print("----- %s AM" % (self.time))
    #
    #             self.checkAnimCam(self.usrinput)
    #             self.cam()
    #             return None
    #
    #         #Clears the window.
    #         if self.usrinput in ["clear", "cls"]:
    #             cls.cls()
    #             self.cam()
    #             return None
    #
    #         #Closes camera mode. Also handles certains game overs.
    #         if self.usrinput in ["exit", "close", "x", "e", "c"]:
    #             cls.cls(0.5, 0.5)
    #             for animatronic in Globals.animatronics: #Checks if there's "someone" inside...
    #                 if animatronic.location.lower() == "inside":
    #                     debug.debugprint("%s was inside!" % (animatronic.name), animatronic)
    #                     self.die(animatronic)
    #                     return None
    #
    #             for animatronic in Globals.animatronics:
    #                 if animatronic.kind == "bear":
    #                     animatronic.bseen = False
    #                 self.usage -= 1
    #                 self.securityOffice()
    #                 return None
    #
    #
    #
    #
    #         else:
    #             if self.killed == False:
    #                 print("Unknown cam")
    #                 self.cam()
    #                 return None
    #             else:
    #                 print("You're dead. You can close the game")
    #                 print("...but the animatronics will wait for you")
    #                 self.shutdown()


    def die(self, animatronic):
        if animatronic.kind == "chicken":
            self.killed = True
            cls.cls(0.5, 0.5)
            print("%s jumps at your face as a loud screech comes from the animatronic." % (animatronic.name))
            print("%s got you..." % (animatronic.name))
            print("Game over.")
            self.shutdown()

        if animatronic.kind == "rabbit":
            self.killed = True
            cls.cls(0.5, 0.5)
            print("%s jumps at your face as a loud screech comes from the animatronic." % (animatronic.name))
            print("%s got you..." % (animatronic.name))
            print("Game over.")
            self.shutdown()

        if animatronic.kind == "bear":
            self.killed = True
            cls.cls(0.5, 0.5)
            print("%s grabs you and jumps at your face. A really loud screech can be heard." % (animatronic.name))
            print("%s got you..." % (animatronic.name))
            print("Game over...")
            self.shutdown()

        if animatronic.kind == "fox":
            self.killed = True
            cls.cls(0.5, 0.5)
            print("%s enters the room as a loud screech can be heard." % (animatronic.name))
            print("%s got you..." % (animatronic.name))
            print("Game over...")
            self.shutdown()



    def hallucination(self, kind):
        if kind == "camkind":
            self.randhall = random.randint(0, 80)
            if self.randhall in range(0, self.ailvl):
                print("IT'S ME   ")
                if random.randint(0, 2) == 1:
                    print("            IT'S        ME")

    def someoneThere(self, cam):
        for animatronic in Globals.animatronics:
            if animatronic.location == cam:
                return True
        return False


    def checkAnimCam(self, cam):
        if cam == "cam2a":
            for animatronic in Globals.animatronics:
                if animatronic.kind == "fox" and animatronic.foxstatus >= 4:
                    animatronic.foxstatus = 5
                    animatronic.think()
                    print("You see %s sprinting down the hall." % (animatronic.name))
                    self.usage -= 1
                    self.securityOffice()
                    return None
                if animatronic.location == cam and animatronic.kind != "fox":
                    self.hallucination("camkind")
                    print("%s is here." % (animatronic.name))

        if cam == "cam1c":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam and animatronic.kind == "fox":
                    animatronic.foxtseen += 1
                    if animatronic.foxstatus <= 0:
                        print("%s is hiding behind the curtain." % (animatronic.name))

                    if animatronic.foxstatus == 1:
                        print("%s is peeking through the curtain." % (animatronic.name))

                    if animatronic.foxstatus == 2:
                        print("%s is looking through the curtain." % (animatronic.name))

                    if animatronic.foxstatus == 3:
                        print("%s is out." % (animatronic.name))

                    if animatronic.foxstatus == 4:
                        print("%s is gone." % (animatronic.name))

        if cam == "cam1a":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam:
                    if random.randint(0, 1) == 1:
                        print("%s is here." % (animatronic.name))
                    else:
                        print("%s is looking directly to the camera." % (animatronic.name))

        if cam == "cam4b":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam and animatronic.kind != "bear":
                    print("%s is here." % (animatronic.name))

                if animatronic.location == cam and animatronic.kind == "bear":
                    print("%s is looking directly to the camera." % (animatronic.name))

        if cam == "cam6":
            for animatronic in Globals.animatronics:
                if animatronic.location == cam:
                    if animatronic.kind == "bear":
                        print("A music box can be heard.")
                    else:
                        print("Noise can be heard.")

        elif cam not in ["cam1c", "cam1a", "cam4b", "cam6", "cam2a"]:
            for animatronic in Globals.animatronics:
                if animatronic.location == cam and animatronic.kind != "bear":
                    print("%s is here." % (animatronic.name))
                if animatronic.location == cam and animatronic.kind == "bear":
                    print("%s" % (random.choice(["...huh?", "W-What's that?", "..."])))

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
