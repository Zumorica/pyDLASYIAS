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
    def __init__(self, gmode="custom", power=100, time=0, sectohour=86, width=1600, height=720, fps=120):
        debug.debugprint("pyDLASYIAS %s started. Setting up game variables..." % (Globals.version))

        sys.setrecursionlimit(5000) #Magic.
        threading.stack_size(128*4096) #Magic.

        self.animlvlsum = 0
        self.gmode = gmode #Game mode. Normal | Custom (custom animatronics AI) | Survival (No time, no energy) | ???

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

        self.font = pygame.font.Font(None, 30)

        self.allgroup = pygame.sprite.Group()
        self.officegroup = pygame.sprite.LayeredUpdates()
        self.camgroup = pygame.sprite.LayeredUpdates()
        self.scaregroup = pygame.sprite.LayeredUpdates()

        self.leftButton = sprite.Sprite(startpos=(0, 180), image="office\\button\\left\\0")
        self.leftButton.groups = self.allgroup, self.officegroup

        self.rightButton = sprite.Sprite(startpos=(1500, 180), image="office\\button\\right\\0")
        self.rightButton.groups = self.allgroup, self.officegroup

        self.camButton = sprite.Sprite(startpos=(530, 578), image="ui\\button\\camera")
        self.camButton.groups = self.allgroup, self.officegroup, self.camgroup

        self.map = sprite.Sprite(startpos=(1200, 350), image="ui\\map")
        self.map.groups = self.allgroup, self.camgroup

        self.camButtonOneA = sprite.Sprite(startpos=(1313,370), image="ui\\button\\cam1a")
        self.camButtonOneA.groups = self.allgroup, self.camgroup

        self.camButtonOneB = sprite.Sprite(startpos=(1300,510), image="ui\\button\\cam1b")
        self.camButtonOneB.groups = self.allgroup, self.camgroup

        self.camButtonOneC = sprite.Sprite(startpos=(1250,524), image="ui\\button\\cam1c")
        self.camButtonOneC.groups = self.allgroup, self.camgroup

        self.camButtonTwoA = sprite.Sprite(startpos=(1307,598), image="ui\\button\\cam2a")
        self.camButtonTwoA.groups = self.allgroup, self.camgroup

        self.camButtonTwoB = sprite.Sprite(startpos=(1307,648), image="ui\\button\\cam2b")
        self.camButtonTwoB.groups = self.allgroup, self.camgroup

        self.camButtonThree = sprite.Sprite(startpos=(1240,598), image="ui\\button\\cam3")
        self.camButtonThree.groups = self.allgroup, self.camgroup

        self.camButtonFourA = sprite.Sprite(startpos=(1400,598), image="ui\\button\\cam4a")
        self.camButtonFourA.groups = self.allgroup, self.camgroup

        self.camButtonFourB = sprite.Sprite(startpos=(1400,648), image="ui\\button\\cam4b")
        self.camButtonFourB.groups = self.allgroup, self.camgroup

        self.camButtonFive = sprite.Sprite(startpos=(1200, 430), image="ui\\button\\cam5")
        self.camButtonFive.groups = self.allgroup, self.camgroup

        self.camButtonSix = sprite.Sprite(startpos=(1520,600), image="ui\\button\\cam6")
        self.camButtonSix.groups = self.allgroup, self.camgroup

        self.camButtonSeven = sprite.Sprite(startpos=(1523,457), image="ui\\button\\cam7")
        self.camButtonSeven.groups = self.allgroup, self.camgroup

        self.chickenScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\chicken\\0.png", "office\\scarejump\\chicken\\1.png",
                                                                        "office\\scarejump\\chicken\\2.png", "office\\scarejump\\chicken\\3.png",
                                                                        "office\\scarejump\\chicken\\4.png", "office\\scarejump\\chicken\\5.png",
                                                                        "office\\scarejump\\chicken\\6.png", "office\\scarejump\\chicken\\7.png",
                                                                        "office\\scarejump\\chicken\\8.png", "office\\scarejump\\chicken\\9.png",
                                                                        "office\\scarejump\\chicken\\10.png", "office\\scarejump\\chicken\\11.png",
                                                                        "office\\scarejump\\chicken\\12.png"])

        self.rabbitScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\rabbit\\0.png", "office\\scarejump\\rabbit\\1.png",
                                                                       "office\\scarejump\\rabbit\\2.png", "office\\scarejump\\rabbit\\3.png",
                                                                       "office\\scarejump\\rabbit\\4.png", "office\\scarejump\\rabbit\\5.png",
                                                                       "office\\scarejump\\rabbit\\6.png", "office\\scarejump\\rabbit\\7.png",
                                                                       "office\\scarejump\\rabbit\\8.png", "office\\scarejump\\rabbit\\9.png",
                                                                       "office\\scarejump\\rabbit\\10.png"])

        self.foxScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\fox\\0.png", "office\\scarejump\\fox\\1.png",
                                                                    "office\\scarejump\\fox\\2.png", "office\\scarejump\\fox\\3.png",
                                                                    "office\\scarejump\\fox\\4.png", "office\\scarejump\\fox\\5.png",
                                                                    "office\\scarejump\\fox\\6.png", "office\\scarejump\\fox\\7.png",
                                                                    "office\\scarejump\\fox\\8.png", "office\\scarejump\\fox\\9.png",
                                                                    "office\\scarejump\\fox\\10.png", "office\\scarejump\\fox\\11.png",
                                                                    "office\\scarejump\\fox\\12.png", "office\\scarejump\\fox\\13.png",
                                                                    "office\\scarejump\\fox\\14.png", "office\\scarejump\\fox\\15.png",
                                                                    "office\\scarejump\\fox\\16.png", "office\\scarejump\\fox\\17.png",
                                                                    "office\\scarejump\\fox\\18.png"])

        self.bearNormalScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\bear\\normal\\0.png", "office\\scarejump\\bear\\normal\\1.png",
                                                                           "office\\scarejump\\bear\\normal\\2.png", "office\\scarejump\\bear\\normal\\3.png",
                                                                           "office\\scarejump\\bear\\normal\\4.png", "office\\scarejump\\bear\\normal\\5.png",
                                                                           "office\\scarejump\\bear\\normal\\6.png", "office\\scarejump\\bear\\normal\\7.png",
                                                                           "office\\scarejump\\bear\\normal\\8.png", "office\\scarejump\\bear\\normal\\9.png",
                                                                           "office\\scarejump\\bear\\normal\\10.png", "office\\scarejump\\bear\\normal\\11.png",
                                                                           "office\\scarejump\\bear\\normal\\12.png", "office\\scarejump\\bear\\normal\\13.png",
                                                                           "office\\scarejump\\bear\\normal\\14.png", "office\\scarejump\\bear\\normal\\15.png",
                                                                           "office\\scarejump\\bear\\normal\\16.png", "office\\scarejump\\bear\\normal\\17.png",
                                                                           "office\\scarejump\\bear\\normal\\18.png", "office\\scarejump\\bear\\normal\\19.png",
                                                                           "office\\scarejump\\bear\\normal\\20.png", "office\\scarejump\\bear\\normal\\21.png",
                                                                           "office\\scarejump\\bear\\normal\\22.png", "office\\scarejump\\bear\\normal\\23.png",
                                                                           "office\\scarejump\\bear\\normal\\24.png", "office\\scarejump\\bear\\normal\\25.png",
                                                                           "office\\scarejump\\bear\\normal\\26.png", "office\\scarejump\\bear\\normal\\27.png",
                                                                           "office\\scarejump\\bear\\normal\\28.png", "office\\scarejump\\bear\\normal\\29.png"])

        self.staticTransparent = sprite.Sprite(startpos=(0,0), image="cameras\\misc\\static\\transparent\\0")
        self.staticTransparent.groups = self.allgroup, self.officegroup, self.camgroup, self.scaregroup

        self.bg = sprite.Sprite("office\\0", (0,0))
        self.bg.groups = self.allgroup, self.officegroup, self.camgroup, self.scaregroup

        self.allgroup.add(self.leftButton)
        self.allgroup.add(self.rightButton)
        self.allgroup.add(self.camButton)
        self.allgroup.add(self.map)
        self.allgroup.add(self.bg)
        self.allgroup.add(self.camButtonOneA)
        self.allgroup.add(self.bearNormalScarejump)
        self.allgroup.add(self.foxScarejump)
        self.allgroup.add(self.rabbitScarejump)
        self.allgroup.add(self.chickenScarejump)
        self.allgroup.add(self.camButtonOneA)
        self.allgroup.add(self.camButtonOneB)
        self.allgroup.add(self.camButtonOneC)
        self.allgroup.add(self.camButtonTwoA)
        self.allgroup.add(self.camButtonTwoB)
        self.allgroup.add(self.camButtonThree)
        self.allgroup.add(self.camButtonFourA)
        self.allgroup.add(self.camButtonFourB)
        self.allgroup.add(self.camButtonFive)
        self.allgroup.add(self.camButtonSix)
        self.allgroup.add(self.camButtonSeven)
        self.allgroup.add(self.staticTransparent)

        self.xscream = pygame.mixer.Sound("sounds\\scary\\XSCREAM.wav")
        self.xscreamTwo = pygame.mixer.Sound("sounds\\scary\\XSCREAM2.wav")

        self.giggle = pygame.mixer.Sound("sounds\\scary\\giggle.wav")
        self.freddygiggle = pygame.mixer.Sound("sounds\\scary\\freddygiggle.wav")
        self.freddygiggleTwo = pygame.mixer.Sound("sounds\\scary\\freddygiggle2.wav")
        self.freddygiggleThree = pygame.mixer.Sound("sounds\\scary\\freddygiggle3.wav")

        self.windowscare = pygame.mixer.Sound("sounds\\scary\\windowscare.wav")

        self.breathing = pygame.mixer.Sound("sounds\\scary\\breathing.wav")
        self.breathingTwo = pygame.mixer.Sound("sounds\\scary\\breathing2.wav")
        self.breathingThree = pygame.mixer.Sound("sounds\\scary\\breathing3.wav")
        self.breathingFour = pygame.mixer.Sound("sounds\\scary\\breathing4.wav")

        self.chimes = pygame.mixer.Sound("sounds\\misc\\6AM.wav")
        self.children = pygame.mixer.Sound("sounds\\misc\\children.wav")

        self.doorSound = pygame.mixer.Sound("sounds\\misc\\door.wav")
        self.doorknocking = pygame.mixer.Sound("sounds\\misc\\doorknocking.wav")
        self.doorpundering = pygame.mixer.Sound("sounds\\misc\\doorpounding.wav")

        self.freddysNose = pygame.mixer.Sound("sounds\\misc\\honk.wav")
        self.musicbox = pygame.mixer.Sound("sounds\\misc\\musicbox.wav")
        self.powerdown = pygame.mixer.Sound("sounds\\misc\\powerdown.wav")

        self.lighthum = pygame.mixer.Sound("sounds\\misc\\lighthum.wav")
        self.buttonError = pygame.mixer.Sound("sounds\\misc\\error.wav")

        self.blip = pygame.mixer.Sound("sounds\\camera\\blip.wav")
        self.cameraSound = pygame.mixer.Sound("sounds\\camera\\camerasound.wav")
        self.cameraSoundTwo = pygame.mixer.Sound("sounds\\camera\\camerasound2.wav")

        self.computernoise = pygame.mixer.Sound("sounds\\camera\\computernoise.wav")
        self.garble = pygame.mixer.Sound("sounds\\camera\\garble.wav")
        self.garbleTwo = pygame.mixer.Sound("sounds\\camera\\garble2.wav")
        self.garbleThree = pygame.mixer.Sound("sounds\\camera\\garble3.wav")

        self.putdown = pygame.mixer.Sound("sounds\\camera\\putdown.wav")

        self.pots = pygame.mixer.Sound("sounds\\camera\\pots.wav")
        self.potsTwo = pygame.mixer.Sound("sounds\\camera\\pots2.wav")
        self.potsThree = pygame.mixer.Sound("sounds\\camera\\pots3.wav")
        self.potsFour = pygame.mixer.Sound("sounds\\camera\\pots4.wav")

        self.static = pygame.mixer.Sound("sounds\\camera\\static2.wav")

        self.fanSound = pygame.mixer.Sound("sounds\\ambience\\fan.wav")

        self.mousex = 0
        self.mousey = 0

        self.runonce = 0

        while self.running:

            Globals.mouseClick = False
            Globals.pos = self.mousex, self.mousey

            for event in pygame.event.get():

                print(event)

                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    self.shutdown()

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    self.mousex, self.mousey = event.pos
                    Globals.mouseClick = True

            if self.scene == "office":

                if self.power < 0:
                    self.runonce = 0
                    self.scene = "powerdown"

                if self.runonce == 0:
                    self.fanSound.play(-1)
                    self.runonce = 1

                self.officegroup.add(self.leftButton)
                self.officegroup.add(self.rightButton)
                self.officegroup.add(self.camButton)
                self.officegroup.add(self.bg)

                self.officegroup.change_layer(self.bg, 0)
                self.officegroup.change_layer(self.leftButton, 1)
                self.officegroup.change_layer(self.rightButton, 1)
                self.officegroup.change_layer(self.camButton, 2)

                if Globals.mouseClick:
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
                        self.freddysNose.play(0)

                    if self.mousex in range(532,1127) and self.mousey in range(588,630):
                        print("TBC WITH CAMERA!!! (%s, %s)" %(self.mousex,self.mousey))
                        self.openCamera()

                #BG

                if self.leftlight and not self.rightlight:
                    for animatronic in Globals.animatronics:
                        if animatronic.location == "leftdoor" and animatronic.kind == "rabbit":
                            self.bg.changeImg("office\\r")
                            break
                    else:
                        self.bg.changeImg("office\\1")

                elif not self.leftlight and self.rightlight:
                    for animatronic in Globals.animatronics:
                        if animatronic.location == "rightlight" and animatronic.kind == "chicken":
                            self.bg.changeImg("office\\c")
                            break
                    else:
                        self.bg.changeImg("office\\2")

                elif not self.leftlight and not self.rightlight:
                    self.bg.changeImg("office\\0")

                #BUTTONS

                #LEFT BUTTON

                if not self.leftlight and not self.leftdoor:
                    self.leftButton.changeImg("office\\button\\left\\0")

                elif self.leftlight and self.leftdoor:
                    self.leftButton.changeImg("office\\button\\left\\dl")

                elif self.leftlight and not self.leftdoor:
                    self.leftButton.changeImg("office\\button\\left\\l")

                elif not self.leftlight and self.leftdoor:
                    self.leftButton.changeImg("office\\button\\left\\d")

                #elif self.leftlight == "broken" or self.leftdoor == "broken":
                #    self.leftButton.changeImg("office\\button\\left\\0")

                #RIGHT BUTTON

                if not self.rightlight and not self.rightdoor:
                    self.rightButton.changeImg("office\\button\\right\\0")

                elif self.rightlight and self.rightdoor:
                    self.rightButton.changeImg("office\\button\\right\\dl")

                elif self.rightlight and not self.rightdoor:
                    self.rightButton.changeImg("office\\button\\right\\l")

                elif not self.rightlight and self.rightdoor:
                    self.rightButton.changeImg("office\\button\\right\\d")

                #elif self.rightlight == "broken" or self.rightdoor == "broken":
                #    self.rightButton.changeImg("office\\button\\right\\0")

                self.officegroup.draw(self.screen)
                self.officegroup.update()

                if self.time == 0:
                    self.timeLabel = self.font.render("12 PM", True, (255,255,255))
                    self.screen.blit(self.timeLabel, (1400,50))
                else:
                    self.timeLabel = self.font.render("%s AM" % (self.time), True, (255,255,255))
                    self.screen.blit(self.timeLabel, (1400,50))

                self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255,255,255))
                self.usageLabel = self.font.render("Usage: %s" %(self.usage), True, (255,255,255))

                self.screen.blit(self.powerLabel, (50,520))
                self.screen.blit(self.usageLabel, (50,550))

            elif self.scene == "cam":

                if self.power < 0:
                    self.securityOffice()

                if self.runonce == 0:
                    self.changeCamera(self.lastcam)
                    self.cameraSound.play(-1)
                    self.cameraSoundTwo.play(-1)
                    self.runonce = 1

                self.camgroup.add(self.camButton)
                self.camgroup.add(self.map)
                self.camgroup.add(self.camButtonOneA)
                self.camgroup.add(self.camButtonOneB)
                self.camgroup.add(self.camButtonOneC)
                self.camgroup.add(self.camButtonTwoA)
                self.camgroup.add(self.camButtonTwoB)
                self.camgroup.add(self.camButtonThree)
                self.camgroup.add(self.camButtonFourA)
                self.camgroup.add(self.camButtonFourB)
                self.camgroup.add(self.camButtonFive)
                self.camgroup.add(self.camButtonSix)
                self.camgroup.add(self.camButtonSeven)
                self.camgroup.add(self.bg)
                self.camgroup.add(self.staticTransparent)

                self.camgroup.change_layer(self.bg, 0)
                self.camgroup.change_layer(self.map, 8)
                self.camgroup.change_layer(self.camButtonOneA, 10)
                self.camgroup.change_layer(self.camButtonOneB, 10)
                self.camgroup.change_layer(self.camButtonOneC, 10)
                self.camgroup.change_layer(self.camButtonTwoA, 10)
                self.camgroup.change_layer(self.camButtonTwoB, 10)
                self.camgroup.change_layer(self.camButtonThree, 10)
                self.camgroup.change_layer(self.camButtonFourA, 10)
                self.camgroup.change_layer(self.camButtonFourB, 10)
                self.camgroup.change_layer(self.camButtonFive, 10)
                self.camgroup.change_layer(self.camButtonSix, 10)
                self.camgroup.change_layer(self.camButtonSeven, 10)
                self.camgroup.change_layer(self.camButton, 10)
                self.camgroup.change_layer(self.staticTransparent, 2)

                self.staticTransparent.changeImg(random.choice(["cameras\\misc\\static\\transparent\\0", "cameras\\misc\\static\\transparent\\1",
                                                               "cameras\\misc\\static\\transparent\\2", "cameras\\misc\\static\\transparent\\3",
                                                               "cameras\\misc\\static\\transparent\\4", "cameras\\misc\\static\\transparent\\5",
                                                               "cameras\\misc\\static\\transparent\\6", "cameras\\misc\\static\\transparent\\7"]))

                if self.camButtonOneA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                    "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                    "cameras\\misc\\static\\4", "cameras\\misc\\static\\5"]))
                    self.changeCamera("cam1a")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonOneB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                    "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                    "cameras\\misc\\static\\4", "cameras\\misc\\static\\5"]))
                    self.changeCamera("cam1b")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonOneC.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                    "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                    "cameras\\misc\\static\\4", "cameras\\misc\\static\\5"]))
                    self.changeCamera("cam1c")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonTwoA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                    "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                    "cameras\\misc\\static\\4", "cameras\\misc\\static\\5"]))
                    self.changeCamera("cam2a")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonTwoB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam2b")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonThree.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam3")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonFourA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam4a")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonFourB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam4b")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonFive.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam5")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonSix.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam6")
                    print("%s CLICKED" %(self.lastcam.upper()))

                if self.camButtonSeven.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam7")
                    print("%s CLICKED" %(self.lastcam.upper()))

                #------#

                if self.lastcam == "cam1a":

                    self.camButtonOneA.changeImg("ui\\button\\scam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[0].location == "cam1a" and Globals.animatronics[1].location == "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\brc")

                    if Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location == "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\bc")

                    if Globals.animatronics[0].location == "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\br")

                    if Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\b")

                    if Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location != "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\0")

                elif self.lastcam == "cam1b":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\scam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[0].location == "cam1b" and Globals.animatronics[1].location == "cam1b":
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",  "cameras\\misc\\static\\2", "cameras\\misc\\static\\3", "cameras\\misc\\static\\4", "cameras\\misc\\static\\5", "cameras\\misc\\static\\6"]))

                    if Globals.animatronics[0].location == "cam1b" and Globals.animatronics[1].location != "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\r")

                    if Globals.animatronics[0].location != "cam1b" and Globals.animatronics[1].location == "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\r")

                    if Globals.animatronics[0].location != "cam1b" and Globals.animatronics[1].location != "cam1b" and Globals.animatronics[3].location == "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\b")

                    if Globals.animatronics[0].location != "cam1b" and Globals.animatronics[1].location != "cam1b" and Globals.animatronics[3].location != "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\0")

                elif self.lastcam == "cam1c":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\scam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[2].foxstatus == 0:
                        self.bg.changeImg("cameras\\cam1c\\0")

                    if Globals.animatronics[2].foxstatus == 1:
                        self.bg.changeImg("cameras\\cam1c\\1")

                    if Globals.animatronics[2].foxstatus == 2:
                        self.bg.changeImg("cameras\\cam1c\\2")

                    if Globals.animatronics[2].foxstatus == 3:
                        self.bg.changeImg("cameras\\cam1c\\3")

                    if Globals.animatronics[2].foxstatus == 4:
                        self.bg.changeImg("cameras\\cam1c\\4")

                elif self.lastcam == "cam2a":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\scam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[0].location == "cam2a":
                        self.bg.changeImg(random.choice(["cameras\\cam2a\\0", "cameras\\cam2a\\r"]))

                    else:
                        self.bg.changeImg(random.choice(["cameras\\cam2a\\0", "cameras\\cam2a\\1"]))



                elif self.lastcam == "cam2b":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\scam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[0].location == "cam2b":
                        self.bg.changeImg(random.choice(["cameras\\cam2b\\r", "cameras\\cam2b\\r-1"]))

                    else:
                        self.bg.changeImg("cameras\\cam2b\\0")

                elif self.lastcam == "cam3":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\scam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[0].location == "cam3":
                        self.bg.changeImg("cameras\\cam3\\r")

                    else:
                        self.bg.changeImg("cameras\\cam3\\0")


                elif self.lastcam == "cam4a":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\scam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[1].location == "cam4a":
                        self.bg.changeImg("cameras\\cam4a\\c")

                    elif Globals.animatronics[1].location != "cam4a" and Globals.animatronics[3].location == "cam4a":
                        self.bg.changeImg("cameras\\cam4a\\b")

                    elif Globals.animatronics[1].location != "cam4a" and Globals.animatronics[3].location != "cam4a":
                        self.bg.changeImg("cameras\\cam4a\\0")


                elif self.lastcam == "cam4b":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\scam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[1].location == "cam4b":
                        self.bg.changeImg("cameras\\cam4b\\c")

                    elif Globals.animatronics[1].location != "cam4b" and Globals.animatronics[3].location == "cam4b":
                        self.bg.changeImg("cameras\\cam4b\\b")

                    elif Globals.animatronics[1].location != "cam4b" and Globals.animatronics[3].location != "cam4b":
                        self.bg.changeImg("cameras\\cam4b\\0")


                elif self.lastcam == "cam5":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\scam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    if Globals.animatronics[0].location == "cam5":
                        self.bg.changeImg("cameras\\cam5\\r")

                    else:
                        self.bg.changeImg("cameras\\cam5\\0")


                elif self.lastcam == "cam6":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\scam6")
                    self.camButtonSeven.changeImg("ui\\button\\cam7")

                    self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",  "cameras\\misc\\static\\2",
                                                     "cameras\\misc\\static\\3", "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                     "cameras\\misc\\static\\6"]))

                elif self.lastcam == "cam7":

                    self.camButtonOneA.changeImg("ui\\button\\cam1a")
                    self.camButtonOneB.changeImg("ui\\button\\cam1b")
                    self.camButtonOneC.changeImg("ui\\button\\cam1c")
                    self.camButtonTwoA.changeImg("ui\\button\\cam2a")
                    self.camButtonTwoB.changeImg("ui\\button\\cam2b")
                    self.camButtonThree.changeImg("ui\\button\\cam3")
                    self.camButtonFourA.changeImg("ui\\button\\cam4a")
                    self.camButtonFourB.changeImg("ui\\button\\cam4b")
                    self.camButtonFive.changeImg("ui\\button\\cam5")
                    self.camButtonSix.changeImg("ui\\button\\cam6")
                    self.camButtonSeven.changeImg("ui\\button\\scam7")

                    if Globals.animatronics[1].location == "cam7":
                        self.bg.changeImg("cameras\\cam7\\c")

                    elif Globals.animatronics[1].location != "cam7" and Globals.animatronics[2].location == "cam7":
                        self.bg.changeImg("cameras\\cam7\\b")

                    else:
                        self.bg.changeImg("cameras\\cam7\\0")




                if self.mousex in range(532,1127) and self.mousey in range(588,630) and Globals.mouseClick:
                    print("TBC WITH CAMERA!!! (%s, %s)" %(self.mousex,self.mousey))
                    self.securityOffice()

                self.camgroup.draw(self.screen)
                self.camgroup.update()

                if self.time == 0:
                    self.timeLabel = self.font.render("12 PM", True, (255,255,255))
                    self.screen.blit(self.timeLabel, (1400,50))
                else:
                    self.timeLabel = self.font.render("%s AM" % (self.time), True, (255,255,255))
                    self.screen.blit(self.timeLabel, (1400,50))

                self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255,255,255))
                self.usageLabel = self.font.render("Usage: %s" %(self.usage), True, (255,255,255))

                self.screen.blit(self.powerLabel, (50,520))
                self.screen.blit(self.usageLabel, (50,550))

            elif self.scene == "scarejump":

                self.scaregroup.add(self.bg)
                self.killed = True

                for animatronic in Globals.animatronics:
                    if animatronic.location == "inside":
                        if self.runonce == 0:
                            self.xscream.play(0)
                            self.runonce = 1
                        if animatronic.kind == "chicken":
                            self.scaregroup.add(self.chickenScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.chickenScarejump.has_Finished():
                                self.shutdown()


                        if animatronic.kind == "rabbit":
                            self.scaregroup.add(self.rabbitScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.rabbitScarejump.has_Finished():
                                self.shutdown()


                        if animatronic.kind == "bear":
                            self.scaregroup.add(self.bearNormalScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.bearNormalScarejump.has_Finished():
                                self.shutdown()


                        if animatronic.kind == "fox":
                            self.scaregroup.add(self.foxScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.foxScarejump.has_Finished():
                                self.shutdown()

                self.scaregroup.draw(self.screen)
                self.scaregroup.update()

            elif self.scene == "powerdown":
                self.scaregroup.add(self.bg)

                if self.runonce == 0:
                    pygame.mixer.stop()
                    self.bg.changeImg("office\\powerdown\\0")
                    self.scaregroup.draw()
                    self.powerdown.play(0)
                    self.runonce = 1

                self.freddyHere = 0

                if random.randint(0, 100) == 87 and self.freddyHere == 0:
                    self.musicbox.play(0)
                    self.freddyHere = 1
                    self.bg.changeImg(random.choice(["office\\powerdown\\0", "office\\powerdown\\0", "office\\powerdown\\0", "office\\powerdown\\1"]))
                    while 1:
                        if random.randint(0, 100) == 87 and self.freddyHere == 1:
                            pygame.mixer.stop()
                            self.bg.changeImg("office\\powerdown\\3")


                self.scaregroup.draw(self.screen)
                self.scaregroup.update()




            pygame.display.update()
            pygame.display.flip()
            self.FPSCLOCK.tick(self.fps)

    def shutdown(self): #Shuts down the whole game.
        debug.debugprint("Shutting down...")
        pygame.quit()
        for animatronic in Globals.animatronics:
            animatronic.dmove("off")
        sys.exit(0)
        os._exit(0)
        os.system("exit")

    def changeCamera(self, camera):
        self.blip.play(0)
        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",  "cameras\\misc\\static\\2",
                                             "cameras\\misc\\static\\3", "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                             "cameras\\misc\\static\\6"]))
        self.camgroup.draw(self.screen)
        self.camgroup.update()
        self.lastcam = camera


    def powerTimer(self): #Timer for the power.
        if self.killed == True or self.time >= 6 or self.power == 0 - 1: #Checks if the game has finished
            pass
        else:
            if self.power <= 0 - 1:
                pass
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
                time.sleep(random.randint(20, 30) / animatronic.ailvl)
                if self.leftdoor: #If leftdoor is closed
                    animatronic.rmove(["cam1b"]) #Go back to cam1b or not

                if not self.leftdoor: #Else if leftdoor is open
                    time.sleep(random.randint(20, 30) / animatronic.ailvl)
                    animatronic.rmove(["inside"]) #Random move the animatronic inside or not.
                    if self.ailvl > 12 and animatronic.location == "inside": #If AILVL is over 12 and the animatronic is inside...
                        #self.leftlight = "broken" #Break the light and door
                        #self.leftdoor = "broken"
                        pass

            if animatronic.location == "rightdoor":
                time.sleep(random.randint(20, 30) / animatronic.ailvl)
                if self.rightdoor == True:
                    animatronic.rmove(["cam1b"])


                else:
                    time.sleep(random.randint(20, 30) / animatronic.ailvl)
                    animatronic.rmove(["inside"])
                    if self.ailvl > 12 and animatronic.location == "inside":
                        #self.rightlight = "broken"
                        #self.rightdoor = "broken"
                        pass

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
            return None
        if self.leftdoor == True:
            print("Opened left door.")
            self.leftdoor = False
            self.usage -= 1
            return None

        if self.leftdoor == "broken":
            print("Left door doesn't work...")
            return None

    def leftLight(self):
        if self.leftlight == True:
            print("Left light is now OFF.")
            self.leftlight = False
            self.usage -= 1
            return None

        if self.leftlight == False:
            self.leftlight = True
            if self.rightlight == True:
                print("Right light is now OFF.")
                self.rightlight = False
                self.usage -= 1
            self.usage += 1
            print("Left light is now ON.")
            for animatronic in Globals.animatronics:
                if animatronic.location == "leftdoor":
                    print("%s is at the left door, looking at you." % (animatronic.name))
            return None

        if self.leftlight == "broken":
            print("Left light doesn't work...")
            return None

    def rightDoor(self):
        if self.rightdoor == False:
            print("Closed right door.")
            self.rightdoor = True
            self.usage += 1
            return None

        if self.rightdoor == True:
            print("Opened right door.")
            self.rightdoor = False
            self.usage -= 1
            return None

        if self.rightdoor == "broken":
            print("Right door doesn't work...")
            return None

    def rightLight(self):
        if self.rightlight == True:
            print("Right light is now OFF.")
            self.rightlight = False
            self.usage -= 1
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
            return None

        if self.rightlight == "broken":
            print("Right light doesn't work...")
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
        self.putdown.play(0)
        pygame.time.delay(1000)
        pygame.mixer.stop()
        self.runonce = 0
        self.scene = "cam"
        debug.debugprint("Camera opened")
        return None

    def securityOffice(self):
        debug.debugprint("Go back into office")
        self.usage -= 1
        self.putdown.play(0)
        pygame.time.delay(1000)
        pygame.mixer.stop()
        self.runonce = 0
        self.scene = "office"
        for animatronic in Globals.animatronics:
            if animatronic.location.lower() == "inside":
                debug.debugprint("%s was inside!" % (animatronic.name), animatronic)
                self.scene = "scarejump"

        debug.debugprint("Back into office")
        return None

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
