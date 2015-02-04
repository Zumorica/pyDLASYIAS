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
    def __init__(self, gmode="custom", power=100, time=0, sectohour=86, width=1280, height=720, fps=60):
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

        self.LeftDoorButton = sprite.Sprite(startpos=(34, 232), image="office\\button\\collision")
        self.LeftDoorButton.groups = self.allgroup, self.officegroup

        self.LeftLightButton = sprite.Sprite(startpos=(34, 314), image="office\\button\\collision")
        self.LeftLightButton.groups = self.allgroup, self.officegroup

        self.RightDoorButton = sprite.Sprite(startpos=(1525,232), image="office\\button\\collision")
        self.RightDoorButton.groups = self.allgroup, self.officegroup

        self.RightLightButton = sprite.Sprite(startpos=(1525,314), image="office\\button\\collision")
        self.RightLightButton.groups = self.allgroup, self.officegroup

        self.camButton = sprite.Sprite(startpos=(245, 635), image="ui\\button\\camera")
        self.camButton.groups = self.allgroup, self.officegroup, self.camgroup

        self.map = sprite.Sprite(startpos=(848, 313), image="ui\\map")
        self.map.groups = self.allgroup, self.camgroup

        self.camButtonOneA = sprite.Sprite(startpos=(983,353), image="ui\\button\\cam1a")
        self.camButtonOneA.groups = self.allgroup, self.camgroup

        self.camButtonOneB = sprite.Sprite(startpos=(963,409), image="ui\\button\\cam1b")
        self.camButtonOneB.groups = self.allgroup, self.camgroup

        self.camButtonOneC = sprite.Sprite(startpos=(931,487), image="ui\\button\\cam1c")
        self.camButtonOneC.groups = self.allgroup, self.camgroup

        self.camButtonTwoA = sprite.Sprite(startpos=(954,574), image="ui\\button\\cam2a")
        self.camButtonTwoA.groups = self.allgroup, self.camgroup

        self.camButtonTwoB = sprite.Sprite(startpos=(954,626), image="ui\\button\\cam2b")
        self.camButtonTwoB.groups = self.allgroup, self.camgroup

        self.camButtonThree = sprite.Sprite(startpos=(877,574), image="ui\\button\\cam3")
        self.camButtonThree.groups = self.allgroup, self.camgroup

        self.camButtonFourA = sprite.Sprite(startpos=(1060,574), image="ui\\button\\cam4a")
        self.camButtonFourA.groups = self.allgroup, self.camgroup

        self.camButtonFourB = sprite.Sprite(startpos=(1060,626), image="ui\\button\\cam4b")
        self.camButtonFourB.groups = self.allgroup, self.camgroup

        self.camButtonFive = sprite.Sprite(startpos=(857,436), image="ui\\button\\cam5")
        self.camButtonFive.groups = self.allgroup, self.camgroup

        self.camButtonSix = sprite.Sprite(startpos=(1163,556), image="ui\\button\\cam6")
        self.camButtonSix.groups = self.allgroup, self.camgroup

        self.camButtonSeven = sprite.Sprite(startpos=(1172,424), image="ui\\button\\cam7")
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
        self.allgroup.add(self.LeftDoorButton)
        self.allgroup.add(self.LeftLightButton)
        self.allgroup.add(self.RightDoorButton)
        self.allgroup.add(self.RightLightButton)
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

        self.camMovement = "left"
        self.lastBgPos = (0,0)
        self.lastLBPos = (0,0)
        self.lastRBPos = (0,0)

        while self.running:

            Globals.mouseClick = False
            Globals.pos = self.mousex, self.mousey

            for event in pygame.event.get():

                debug.debugprint(event, writetolog=False)

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
                    self.freddyHere = 0
                    self.powerDown()


                if self.runonce == 0:
                    self.bg.pos = self.lastBgPos
                    self.fanSound.play(-1)
                    self.runonce = 1


                self.lastBgPos = self.bg.pos
                self.lastLBPos = self.leftButton.pos
                self.LastRBPos = self.rightButton.pos

                self.officegroup.add(self.leftButton)
                self.officegroup.add(self.rightButton)
                self.officegroup.add(self.LeftDoorButton)
                self.officegroup.add(self.LeftLightButton)
                self.officegroup.add(self.RightDoorButton)
                self.officegroup.add(self.RightLightButton)
                self.officegroup.add(self.camButton)
                self.officegroup.add(self.bg)

                self.officegroup.change_layer(self.bg, 0)
                self.officegroup.change_layer(self.leftButton, 1)
                self.officegroup.change_layer(self.rightButton, 1)
                self.officegroup.change_layer(self.LeftDoorButton, 2)
                self.officegroup.change_layer(self.LeftLightButton, 2)
                self.officegroup.change_layer(self.RightDoorButton, 2)
                self.officegroup.change_layer(self.RightLightButton, 2)
                self.officegroup.change_layer(self.camButton, 2)

                self.movingleft = False
                self.movingright = False


                if self.mousex in range(0, 150) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 20, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 20, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 20, list(self.leftButton.pos)[1])

                    self.LeftDoorButton.pos = (list(self.LeftDoorButton.pos)[0] + 20, list(self.LeftDoorButton.pos)[1])
                    self.LeftLightButton.pos = (list(self.LeftLightButton.pos)[0] + 20, list(self.LeftLightButton.pos)[1])
                    self.RightDoorButton.pos = (list(self.RightDoorButton.pos)[0] + 20, list(self.RightDoorButton.pos)[1])
                    self.RightLightButton.pos = (list(self.RightLightButton.pos)[0] + 20, list(self.RightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(150, 315) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 10, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 10, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 10, list(self.leftButton.pos)[1])

                    self.LeftDoorButton.pos = (list(self.LeftDoorButton.pos)[0] + 10, list(self.LeftDoorButton.pos)[1])
                    self.LeftLightButton.pos = (list(self.LeftLightButton.pos)[0] + 10, list(self.LeftLightButton.pos)[1])
                    self.RightDoorButton.pos = (list(self.RightDoorButton.pos)[0] + 10, list(self.RightDoorButton.pos)[1])
                    self.RightLightButton.pos = (list(self.RightLightButton.pos)[0] + 10, list(self.RightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(315, 540) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 5, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 5, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 5, list(self.leftButton.pos)[1])

                    self.LeftDoorButton.pos = (list(self.LeftDoorButton.pos)[0] + 5, list(self.LeftDoorButton.pos)[1])
                    self.LeftLightButton.pos = (list(self.LeftLightButton.pos)[0] + 5, list(self.LeftLightButton.pos)[1])
                    self.RightDoorButton.pos = (list(self.RightDoorButton.pos)[0] + 5, list(self.RightDoorButton.pos)[1])
                    self.RightLightButton.pos = (list(self.RightLightButton.pos)[0] + 5, list(self.RightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(1140, 1280) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 20, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 20, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 20, list(self.leftButton.pos)[1])

                    self.LeftDoorButton.pos = (list(self.LeftDoorButton.pos)[0] - 20, list(self.LeftDoorButton.pos)[1])
                    self.LeftLightButton.pos = (list(self.LeftLightButton.pos)[0] - 20, list(self.LeftLightButton.pos)[1])
                    self.RightDoorButton.pos = (list(self.RightDoorButton.pos)[0] - 20, list(self.RightDoorButton.pos)[1])
                    self.RightLightButton.pos = (list(self.RightLightButton.pos)[0] - 20, list(self.RightLightButton.pos)[1])

                    self.movingright = True

                if self.mousex in range(1000, 1140) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 10, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 10, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 10, list(self.leftButton.pos)[1])

                    self.LeftDoorButton.pos = (list(self.LeftDoorButton.pos)[0] - 10, list(self.LeftDoorButton.pos)[1])
                    self.LeftLightButton.pos = (list(self.LeftLightButton.pos)[0] - 10, list(self.LeftLightButton.pos)[1])
                    self.RightDoorButton.pos = (list(self.RightDoorButton.pos)[0] - 10, list(self.RightDoorButton.pos)[1])
                    self.RightLightButton.pos = (list(self.RightLightButton.pos)[0] - 10, list(self.RightLightButton.pos)[1])

                    self.movingright = True

                if self.mousex in range(750, 1000) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 5, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 5, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 5, list(self.leftButton.pos)[1])

                    self.LeftDoorButton.pos = (list(self.LeftDoorButton.pos)[0] - 5, list(self.LeftDoorButton.pos)[1])
                    self.LeftLightButton.pos = (list(self.LeftLightButton.pos)[0] - 5, list(self.LeftLightButton.pos)[1])
                    self.RightDoorButton.pos = (list(self.RightDoorButton.pos)[0] - 5, list(self.RightDoorButton.pos)[1])
                    self.RightLightButton.pos = (list(self.RightLightButton.pos)[0] - 5, list(self.RightLightButton.pos)[1])

                    self.movingright = True

                #print(self.bg.rect.topleft, "top left")
                #print(self.bg.rect.topright, "top right")


                if self.LeftLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.leftLight()

                if self.LeftDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.leftDoor()

                if self.RightLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.rightLight()

                if self.RightDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.rightDoor()

                if self.camButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.openCamera()

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
                    self.screen.blit(self.timeLabel, (1040,60))
                else:
                    self.timeLabel = self.font.render("%s AM" % (self.time), True, (255,255,255))
                    self.screen.blit(self.timeLabel, (1040,60))

                self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255,255,255))
                self.usageLabel = self.font.render("Usage: %s" %(self.usage), True, (255,255,255))

                self.screen.blit(self.powerLabel, (50,520))
                self.screen.blit(self.usageLabel, (50,550))

            elif self.scene == "cam":

                self.notStatic = True

                if self.power < 0:
                    self.securityOffice()

                if self.runonce == 0 and self.power > 0:
                    pygame.mixer.stop()
                    self.bg.pos = (0,0)
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
                    self.changeCamera("cam1a")

                if self.camButtonOneB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam1b")

                if self.camButtonOneC.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam1c")

                if self.camButtonTwoA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam2a")

                if self.camButtonTwoB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam2b")

                if self.camButtonThree.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam3")

                if self.camButtonFourA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam4a")

                if self.camButtonFourB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam4b")

                if self.camButtonFive.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam5")

                if self.camButtonSix.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam6")

                if self.camButtonSeven.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam7")

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

                    elif Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location == "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\bc")

                    elif Globals.animatronics[0].location == "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\br")

                    elif Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location == "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\b")

                    elif Globals.animatronics[0].location != "cam1a" and Globals.animatronics[1].location != "cam1a" and Globals.animatronics[3].location != "cam1a":
                        self.bg.changeImg("cameras\\cam1a\\0")

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))


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

                    elif Globals.animatronics[0].location == "cam1b" and Globals.animatronics[1].location != "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\r")

                    elif Globals.animatronics[0].location != "cam1b" and Globals.animatronics[1].location == "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\r")

                    elif Globals.animatronics[0].location != "cam1b" and Globals.animatronics[1].location != "cam1b" and Globals.animatronics[3].location == "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\b")

                    elif Globals.animatronics[0].location != "cam1b" and Globals.animatronics[1].location != "cam1b" and Globals.animatronics[3].location != "cam1b":
                        self.bg.changeImg("cameras\\cam1b\\0")

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

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

                    elif Globals.animatronics[2].foxstatus == 1:
                        self.bg.changeImg("cameras\\cam1c\\1")

                    elif Globals.animatronics[2].foxstatus == 2:
                        self.bg.changeImg("cameras\\cam1c\\2")

                    elif Globals.animatronics[2].foxstatus == 3:
                        self.bg.changeImg("cameras\\cam1c\\3")

                    elif Globals.animatronics[2].foxstatus == 4:
                        self.bg.changeImg("cameras\\cam1c\\4")

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

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

                    elif Globals.animatronics[0].location != "cam2a":
                        self.bg.changeImg(random.choice(["cameras\\cam2a\\0", "cameras\\cam2a\\1"]))

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

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

                    elif Globals.animatronics[0].location != "cam2b":
                        self.bg.changeImg("cameras\\cam2b\\0")

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

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

                    elif Globals.animatronics[0].location != "cam3":
                        self.bg.changeImg("cameras\\cam3\\0")

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

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

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

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

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))


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

                    elif Globals.animatronics[0].location != "cam5":
                        self.bg.changeImg("cameras\\cam5\\0")

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))


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

                    self.notStatic = False
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

                    if Globals.animatronics[1].location == "cam7" and Globals.animatronics[2].location != "cam7":
                        self.bg.changeImg("cameras\\cam7\\c")

                    elif Globals.animatronics[1].location != "cam7" and Globals.animatronics[2].location == "cam7":
                        self.bg.changeImg("cameras\\cam7\\b")

                    elif Globals.animatronics[1].location != "cam7" and Globals.animatronics[2].location != "cam7":
                        self.bg.changeImg("cameras\\cam7\\0")

                    else:
                        self.notStatic = False
                        self.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

                if self.camButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.securityOffice()

                if list(self.bg.rect.topright)[0] == 1280 and self.notStatic:
                    self.camMovement = "right"

                if list(self.bg.rect.topleft)[0] == 0 and self.notStatic:
                    self.camMovement = "left"

                if self.camMovement == "right" and self.notStatic:
                    self.bg.pos = (list(self.bg.pos)[0] + 5, list(self.bg.pos)[1])

                if self.camMovement == "left" and self.notStatic:
                    self.bg.pos = (list(self.bg.pos)[0] - 5, list(self.bg.pos)[1])

                if not self.notStatic:
                    self.bg.pos = (0,0)


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

                pygame.mixer.stop()
                self.bg.changeImg("office\\powerdown\\0")
                if self.runoncePD == 0:
                    self.powerdown.play(0)
                    self.runoncePD = 1

                self.scaregroup.update()
                self.scaregroup.draw(self.screen)

            pygame.display.update()
            pygame.display.flip()
            self.FPSCLOCK.tick(self.fps)

    def shutdown(self): #Shuts down the whole game.
        debug.debugprint("Shutting down...")
        pygame.quit()
        for animatronic in Globals.animatronics:
            animatronic.dmove("off")
        del self
        sys.exit(0)
        os._exit(0)
        os.system("exit")

    def changeCamera(self, camera):
        self.blip.play(0)
        self.camgroup.draw(self.screen)
        self.camgroup.update()
        if camera == "cam1c":
            Globals.animatronics[2].foxtseen += 1
        pygame.time.wait(150)
        self.lastcam = camera


    def powerTimer(self): #Timer for the power.
        if self.killed == True or self.time >= 6 or self.power == 0 - 1: #Checks if the game has finished
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
            pass

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
                        self.powlost = random.randint(1, 15)
                        self.power -= self.powlost
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
            self.leftdoor = True
            self.usage += 1
            return None

        if self.leftdoor == True:
            self.leftdoor = False
            self.usage -= 1
            return None

    def leftLight(self):
        if self.leftlight == True:
            self.leftlight = False
            self.usage -= 1
            return None

        if self.leftlight == False:
            self.leftlight = True
            if self.rightlight == True:
                self.rightlight = False
                self.usage -= 1
            self.usage += 1
            return None

    def rightDoor(self):
        if self.rightdoor == False:
            self.rightdoor = True
            self.usage += 1
            return None

        if self.rightdoor == True:
            self.rightdoor = False
            self.usage -= 1
            return None

    def rightLight(self):
        if self.rightlight == True:
            self.rightlight = False
            self.usage -= 1
            return None

        if self.rightlight == False:
            self.rightlight = True
            if self.leftlight == True:
                self.leftlight = False
                self.usage -= 1
            self.usage += 1
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
        self.scene = "cam"
        self.runonce = 0
        debug.debugprint("Camera opened")
        return None

    def securityOffice(self):
        debug.debugprint("Go back into office")
        self.usage -= 1
        self.putdown.play(0)
        pygame.time.delay(1000)
        pygame.mixer.stop()
        self.scene = "office"
        self.runonce = 0
        for animatronic in Globals.animatronics:
            if animatronic.location == "inside":
                debug.debugprint("%s was inside!" % (animatronic.name), animatronic)
                self.scene = "scarejump"
        debug.debugprint("Back into office")
        return None

    def powerDown(self):
        pygame.mixer.stop()
        self.scene = "powerdown"
        self.runoncePD = 0
        return None

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
