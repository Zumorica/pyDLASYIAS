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
import pyDLASYIAS.utils.functions as utils
from pygame.locals import *

class main(object):
    def __init__(self, gmode="custom", power=100, time=0, sectohour=86, width=1280, height=720, fps=40):
        utils.debugprint("pyDLASYIAS %s started. Setting up game variables..." % (Globals.version))

        sys.setrecursionlimit(5000)
        threading.stack_size(128*4096)

        self.animlvlsum = 0
        self.gmode = gmode                                                      # Game mode. Normal | Custom (custom animatronics AI) | Survival (No time, no energy) | ???

        for animatronic in Globals.animatronics:
            self.animlvlsum += animatronic.ailvl
            self.ailvl = self.animlvlsum / len(Globals.animatronics)            # This is the lvl of the night.
        del self.animlvlsum

        self.leftdoor = False
        self.rightdoor = False
        self.leftlight = False
        self.rightlight = False
        self.power = power
        self.killed = False
        self.time = time - 1                                                    # The "-1" is there because the timer automatically adds 1 to the variable.
        self.sectohour = sectohour
        self.usage = 1                                                          # 1 Usage: 9.6 / 2 Usage: 4.8 / 3 Usage: 2.8 - 2.9 - 3.9 / 4 Usage: 1.9 - 2.9
        self.scene = "office"                                                   # Scene. Used for knowing what sprites needs to be printed. SCENES: "office", "cam", "powerdown", "scarejump"
        self.lastcam = "cam1a"

        if self.gmode != "survival":                                            # Initializes the hour timer if the gamemode isn't survival.
            threading.Timer(0.1, self.hourTimer).start()

        threading.Timer(0.1, self.powerTimer).start()

        _thread.start_new_thread(self.checkDoorTimer, ())

        _thread.start_new_thread(self.foxkindDoorCheck, ())                     # This thread will be soon replaced.

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

        self.leftDoorButton = sprite.Sprite(startpos=(34, 232), image="office\\button\\collision")
        self.leftDoorButton.groups = self.allgroup, self.officegroup

        self.leftLightButton = sprite.Sprite(startpos=(34, 314), image="office\\button\\collision")
        self.leftLightButton.groups = self.allgroup, self.officegroup

        self.rightDoorButton = sprite.Sprite(startpos=(1525,232), image="office\\button\\collision")
        self.rightDoorButton.groups = self.allgroup, self.officegroup

        self.rightLightButton = sprite.Sprite(startpos=(1525,314), image="office\\button\\collision")
        self.rightLightButton.groups = self.allgroup, self.officegroup

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

        self.leftDoorSpr = sprite.Sprite(startpos=(72,-1), image="office\\doors\\left\\0")
        self.rightDoorSpr = sprite.Sprite(startpos=(1270,-2), image="office\\doors\\right\\0")

        self.foxSprinting = sprite.Animated(startpos=(0,0), images=["cameras\\cam2a\\animation\\0.png","cameras\\cam2a\\animation\\1.png",
                                                                    "cameras\\cam2a\\animation\\2.png", "cameras\\cam2a\\animation\\3.png",
                                                                    "cameras\\cam2a\\animation\\4.png", "cameras\\cam2a\\animation\\5.png",
                                                                    "cameras\\cam2a\\animation\\6.png", "cameras\\cam2a\\animation\\7.png",
                                                                    "cameras\\cam2a\\animation\\8.png", "cameras\\cam2a\\animation\\9.png",
                                                                    "cameras\\cam2a\\animation\\10.png", "cameras\\cam2a\\animation\\11.png",
                                                                    "cameras\\cam2a\\animation\\12.png", "cameras\\cam2a\\animation\\13.png",
                                                                    "cameras\\cam2a\\animation\\14.png", "cameras\\cam2a\\animation\\15.png",
                                                                    "cameras\\cam2a\\animation\\16.png", "cameras\\cam2a\\animation\\17.png",
                                                                    "cameras\\cam2a\\animation\\18.png", "cameras\\cam2a\\animation\\19.png",
                                                                    "cameras\\cam2a\\animation\\20.png", "cameras\\cam2a\\animation\\21.png",
                                                                    "cameras\\cam2a\\animation\\22.png", "cameras\\cam2a\\animation\\23.png",
                                                                    "cameras\\cam2a\\animation\\24.png", "cameras\\cam2a\\animation\\25.png",
                                                                    "cameras\\cam2a\\animation\\26.png"])

        self.leftDoorOpen = sprite.Animated(startpos=(72,-1), images=["office\\doors\\left\\0.png", "office\\doors\\left\\1.png",
                                                                       "office\\doors\\left\\2.png", "office\\doors\\left\\3.png",
                                                                       "office\\doors\\left\\4.png", "office\\doors\\left\\5.png",
                                                                       "office\\doors\\left\\6.png", "office\\doors\\left\\7.png",
                                                                       "office\\doors\\left\\8.png", "office\\doors\\left\\9.png",
                                                                       "office\\doors\\left\\10.png", "office\\doors\\left\\11.png",
                                                                       "office\\doors\\left\\12.png", "office\\doors\\left\\13.png",
                                                                       "office\\doors\\left\\14.png", "office\\doors\\left\\15.png"])

        self.leftDoorClose = sprite.Animated(startpos=(72,-1), images=["office\\doors\\left\\15.png", "office\\doors\\left\\14.png",
                                                                       "office\\doors\\left\\13.png", "office\\doors\\left\\12.png",
                                                                       "office\\doors\\left\\11.png", "office\\doors\\left\\10.png",
                                                                       "office\\doors\\left\\9.png", "office\\doors\\left\\8.png",
                                                                       "office\\doors\\left\\7.png", "office\\doors\\left\\6.png",
                                                                       "office\\doors\\left\\5.png", "office\\doors\\left\\4.png",
                                                                       "office\\doors\\left\\3.png", "office\\doors\\left\\2.png",
                                                                       "office\\doors\\left\\1.png", "office\\doors\\left\\0.png"])

        self.rightDoorOpen = sprite.Animated(startpos=(1270,-2), images=["office\\doors\\right\\0.png", "office\\doors\\right\\1.png",
                                                                       "office\\doors\\right\\2.png", "office\\doors\\right\\3.png",
                                                                       "office\\doors\\right\\4.png", "office\\doors\\right\\5.png",
                                                                       "office\\doors\\right\\6.png", "office\\doors\\right\\7.png",
                                                                       "office\\doors\\right\\8.png", "office\\doors\\right\\9.png",
                                                                       "office\\doors\\right\\10.png", "office\\doors\\right\\11.png",
                                                                       "office\\doors\\right\\12.png", "office\\doors\\right\\13.png",
                                                                       "office\\doors\\right\\14.png", "office\\doors\\right\\15.png"])

        self.rightDoorClose = sprite.Animated(startpos=(1270,-2), images=["office\\doors\\right\\15.png", "office\\doors\\right\\14.png",
                                                                       "office\\doors\\right\\13.png", "office\\doors\\right\\12.png",
                                                                       "office\\doors\\right\\11.png", "office\\doors\\right\\10.png",
                                                                       "office\\doors\\right\\9.png", "office\\doors\\right\\8.png",
                                                                       "office\\doors\\right\\7.png", "office\\doors\\right\\6.png",
                                                                       "office\\doors\\right\\5.png", "office\\doors\\right\\4.png",
                                                                       "office\\doors\\right\\3.png", "office\\doors\\right\\2.png",
                                                                       "office\\doors\\right\\1.png", "office\\doors\\right\\0.png"])

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
        self.allgroup.add(self.leftDoorButton)
        self.allgroup.add(self.leftLightButton)
        self.allgroup.add(self.rightDoorButton)
        self.allgroup.add(self.rightLightButton)
        self.allgroup.add(self.camButton)
        self.allgroup.add(self.map)
        self.allgroup.add(self.bg)
        self.allgroup.add(self.camButtonOneA)
        self.allgroup.add(self.bearNormalScarejump)
        self.allgroup.add(self.foxScarejump)
        self.allgroup.add(self.rabbitScarejump)
        self.allgroup.add(self.chickenScarejump)
        self.allgroup.add(self.leftDoorClose)
        self.allgroup.add(self.rightDoorOpen)
        self.allgroup.add(self.leftDoorOpen)
        self.allgroup.add(self.rightDoorClose)
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
        self.allgroup.add(self.leftDoorSpr)
        self.allgroup.add(self.rightDoorSpr)

        pygame.mixer.set_num_channels(31)
        self.channelZero = pygame.mixer.Channel(0)
        self.channelOne = pygame.mixer.Channel(1)
        self.channelTwo = pygame.mixer.Channel(2)
        self.channelThree = pygame.mixer.Channel(3)
        self.channelFour = pygame.mixer.Channel(4)
        self.channelFive = pygame.mixer.Channel(5)
        self.channelSix = pygame.mixer.Channel(6)
        self.channelSeven = pygame.mixer.Channel(7)
        self.channelEight = pygame.mixer.Channel(8)
        self.channelNine = pygame.mixer.Channel(9)
        self.channelTen = pygame.mixer.Channel(10)
        self.channelEleven = pygame.mixer.Channel(11)
        self.channelTwelve = pygame.mixer.Channel(12)
        self.channelThirteen = pygame.mixer.Channel(13)
        self.channelFourteen = pygame.mixer.Channel(14)
        self.channelFifteen = pygame.mixer.Channel(15)
        self.channelSixteen = pygame.mixer.Channel(16)
        self.channelSeventeen = pygame.mixer.Channel(17)
        self.channelEighteen = pygame.mixer.Channel(18)
        self.channelNineteen = pygame.mixer.Channel(19)
        self.channelTwenty = pygame.mixer.Channel(20)
        self.channelTwentyone = pygame.mixer.Channel(21)
        self.channelTwentytwo = pygame.mixer.Channel(22)
        self.channelTwentythree = pygame.mixer.Channel(23)
        self.channelTwentyfour = pygame.mixer.Channel(24)
        self.channelTwentyfive = pygame.mixer.Channel(25)
        self.channelTwentysix = pygame.mixer.Channel(26)
        self.channelTwentyseven = pygame.mixer.Channel(27)
        self.channelTwentyeight = pygame.mixer.Channel(28)
        self.channelTwentynine = pygame.mixer.Channel(29)
        self.channelThirty = pygame.mixer.Channel(30)

        self.xscream = pygame.mixer.Sound("sounds\\scary\\XSCREAM.wav")
        self.xscreamTwo = pygame.mixer.Sound("sounds\\scary\\XSCREAM2.wav")

        self.giggle = pygame.mixer.Sound("sounds\\scary\\giggle.wav")
        self.freddygiggle = pygame.mixer.Sound("sounds\\scary\\freddygiggle.wav")
        self.freddygiggleTwo = pygame.mixer.Sound("sounds\\scary\\freddygiggle2.wav")
        self.freddygiggleThree = pygame.mixer.Sound("sounds\\scary\\freddygiggle3.wav")

        self.windowscare = pygame.mixer.Sound("sounds\\scary\\windowscare.wav")

        self.robotvoice = pygame.mixer.Sound("sounds\\scary\\robotvoice.wav")

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

        self.computerNoise = pygame.mixer.Sound("sounds\\camera\\computernoise.wav")
        self.garble = pygame.mixer.Sound("sounds\\camera\\garble.wav")
        self.garbleTwo = pygame.mixer.Sound("sounds\\camera\\garble2.wav")
        self.garbleThree = pygame.mixer.Sound("sounds\\camera\\garble3.wav")

        self.putdown = pygame.mixer.Sound("sounds\\camera\\putdown.wav")

        self.pots = pygame.mixer.Sound("sounds\\camera\\pots.wav")
        self.potsTwo = pygame.mixer.Sound("sounds\\camera\\pots2.wav")
        self.potsThree = pygame.mixer.Sound("sounds\\camera\\pots3.wav")
        self.potsFour = pygame.mixer.Sound("sounds\\camera\\pots4.wav")

        self.static = pygame.mixer.Sound("sounds\\camera\\static2.wav")

        self.ambience = pygame.mixer.Sound("sounds\\ambience\\ambience.wav")
        self.ambienceTwo = pygame.mixer.Sound("sounds\\ambience\\ambience2.wav")

        self.fanSound = pygame.mixer.Sound("sounds\\ambience\\fan.wav")

        self.mousex = 0
        self.mousey = 0

        self.runAtSceneStart = 0
        self.runonce = 0

        self.oldTime = 0
        self.camMovement = "left"
        self.powerDownStage = 0
        self.lastBgPos = (0,0)
        self.lastLBPos = (0,0)
        self.lastRBPos = (0,0)

        while self.running:

            Globals.mouseClick = False
            Globals.pos = self.mousex, self.mousey

            for event in pygame.event.get():

                utils.debugprint(event, writetolog=False)

                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    self.shutdown()

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    self.mousex, self.mousey = event.pos
                    Globals.mouseClick = True

            if self.scene == "office":

                if self.runonce == 0:
                    pygame.mixer.stop()
                    self.channelOne.play(self.fanSound, -1)
                    self.channelTwo.play(self.ambience, -1)
                    self.channelThree.play(self.ambienceTwo, -1)

                    self.channelTwo.set_volume(0.5)
                    self.channelTwenty.set_volume(0.1)
                    self.channelTwentyone.set_volume(0)
                    self.channelTwentytwo.set_volume(0.25)

                    self.channelTwentyone.play(self.robotvoice, -1)

                    self.runonce = 1

                if self.time >= 6 :
                    self.scene = "6am"
                    self.runAtFrameStart = 0

                if self.power < 0:
                    self.scene = "powerdown"
                    self.runAtSceneStart = 0

                if self.runAtSceneStart == 0 and not self.power < 0:
                    self.bg.pos = self.lastBgPos
                    self.runAtSceneStart = 1

                self.lastBgPos = self.bg.pos
                #self.lastLBPos = self.leftButton.pos
                #self.LastRBPos = self.rightButton.pos

                self.officegroup.add(self.leftButton)
                self.officegroup.add(self.rightButton)
                self.officegroup.add(self.leftDoorButton)
                self.officegroup.add(self.leftLightButton)
                self.officegroup.add(self.rightDoorButton)
                self.officegroup.add(self.rightLightButton)
                #self.officegroup.add(self.rightDoorSpr)
                #self.officegroup.add(self.leftDoorSpr)
                self.officegroup.add(self.camButton)
                self.officegroup.add(self.bg)

                self.officegroup.change_layer(self.bg, 0)
                self.officegroup.change_layer(self.leftButton, 1)
                self.officegroup.change_layer(self.rightButton, 1)
                self.officegroup.change_layer(self.leftDoorButton, 2)
                self.officegroup.change_layer(self.leftLightButton, 2)
                self.officegroup.change_layer(self.rightDoorButton, 2)
                self.officegroup.change_layer(self.rightLightButton, 2)
                #self.officegroup.change_layer(self.rightDoorSpr, 3)
                #self.officegroup.change_layer(self.leftDoorSpr, 3)
                self.officegroup.change_layer(self.camButton, 5)

                self.movingleft = False
                self.movingright = False

                if self.mousex in range(0, 150) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 20, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 20, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 20, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 20, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] + 20, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] + 20, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 20, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] + 20, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] + 20, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] + 20, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] + 20, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] + 20, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] + 20, list(self.rightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(150, 315) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 10, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 10, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 10, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 10, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] + 10, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] + 10, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 10, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] + 10, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] + 10, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] + 10, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] + 10, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] + 10, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] + 10, list(self.rightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(315, 540) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 5, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 5, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 5, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 5, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] + 5, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] + 5, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 5, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] + 5, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] + 5, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] + 5, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] + 5, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] + 5, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] + 5, list(self.rightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(1140, 1280) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 20, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 20, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 20, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 20, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] - 20, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] - 20, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 20, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] - 20, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] - 20, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] - 20, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] - 20, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] - 20, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] - 20, list(self.rightLightButton.pos)[1])

                    self.movingright = True

                if self.mousex in range(1000, 1140) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 10, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 10, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 10, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 10, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] - 10, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] - 10, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 10, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] - 10, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] - 10, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] - 10, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] - 10, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] - 10, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] - 10, list(self.rightLightButton.pos)[1])

                    self.movingright = True

                if self.mousex in range(750, 1000) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 5, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 5, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 5, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 5, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] - 5, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] - 5, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 5, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] - 5, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] - 5, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] - 5, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] - 5, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] - 5, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] - 5, list(self.rightLightButton.pos)[1])

                    self.movingright = True

                #print(self.bg.rect.topleft, "top left")
                #print(self.bg.rect.topright, "top right")


                if self.leftLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.leftLight()

                if self.leftDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.leftDoor()

                if self.rightLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.rightLight()

                if self.rightDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
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

                if self.time >= 6 :
                    self.scene = "6am"
                    self.runAtFrameStart = 0

                if self.power < 0:
                    self.securityOffice()

                if self.runAtSceneStart == 0 and not self.power < 0:
                    self.bg.pos = (0,0)
                    self.changeCamera(self.lastcam)
                    self.channelSeven.play(self.cameraSoundTwo, -1)
                    self.runAtSceneStart = 1

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
                self.camgroup.add(self.staticTransparent)

                if Globals.animatronics[2].foxstatus != 4:
                    self.camgroup.add(self.bg)

                if Globals.animatronics[2].foxstatus != 4:
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

                    if Globals.animatronics[2].foxstatus != 4:
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
                    else:
                        self.camgroup.remove(self.bg)
                        self.camgroup.add(self.foxSprinting)
                        self.camgroup.change_layer(self.foxSprinting, 0)
                        if self.foxSprinting.has_Finished():
                            self.securityOffice
                            self.camgroup.remove(self.foxSprinting)

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
                self.screen.blit(self.font.render(Globals.camdic[self.lastcam], True, (255,255,255)), (832,292))

            elif self.scene == "scarejump":

                self.scaregroup.add(self.bg)

                if self.time >= 6 :
                    self.scene = "6am"
                    self.runAtFrameStart = 0

                for animatronic in Globals.animatronics:
                    if animatronic.location == "inside":
                        if self.runAtSceneStart == 0:
                            self.xscream.play(0)
                            self.runAtSceneStart = 1
                        if animatronic.kind == "chicken":
                            self.scaregroup.add(self.chickenScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.chickenScarejump.has_Finished():
                                self.killed = True
                                self.shutdown()


                        if animatronic.kind == "rabbit":
                            self.scaregroup.add(self.rabbitScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.rabbitScarejump.has_Finished():
                                self.killed = True
                                self.shutdown()


                        if animatronic.kind == "bear":
                            self.scaregroup.add(self.bearNormalScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.bearNormalScarejump.has_Finished():
                                self.killed = True
                                self.shutdown()


                        if animatronic.kind == "fox":
                            self.scaregroup.add(self.foxScarejump)
                            self.scaregroup.update()
                            self.scaregroup.draw(self.screen)
                            if self.foxScarejump.has_Finished():
                                self.killed = True
                                self.shutdown()

                self.scaregroup.draw(self.screen)
                self.scaregroup.update()

            elif self.scene == "powerdown":

                self.scaregroup.add(self.bg)

                self.movingleft = False
                self.movingright = False

                if self.time >= 6:
                    self.scene = "6am"

                if self.mousex in range(0, 150) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 20, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 20, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 20, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 20, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] + 20, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] + 20, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 20, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] + 20, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] + 20, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] + 20, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] + 20, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] + 20, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] + 20, list(self.rightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(150, 315) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 10, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 10, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 10, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 10, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] + 10, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] + 10, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 10, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] + 10, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] + 10, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] + 10, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] + 10, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] + 10, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] + 10, list(self.rightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(315, 540) and list(self.bg.rect.topleft)[0] in range(-400, -10) and not self.movingright:
                    self.bg.pos = (list(self.bg.pos)[0] + 5, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] + 5, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] + 5, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 5, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] + 5, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] + 5, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] + 5, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] + 5, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] + 5, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] + 5, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] + 5, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] + 5, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] + 5, list(self.rightLightButton.pos)[1])

                    self.movingleft = True

                if self.mousex in range(1140, 1280) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 20, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 20, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 20, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 20, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] - 20, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] - 20, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 20, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] - 20, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] - 20, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] - 20, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] - 20, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] - 20, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] - 20, list(self.rightLightButton.pos)[1])

                    self.movingright = True

                if self.mousex in range(1000, 1140) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 10, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 10, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 10, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 10, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] - 10, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] - 10, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 10, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] - 10, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] - 10, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] - 10, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] - 10, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] - 10, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] - 10, list(self.rightLightButton.pos)[1])

                    self.movingright = True

                if self.mousex in range(750, 1000) and not list(self.bg.rect.topright)[0] < 1300 and not self.movingleft:
                    self.bg.pos = (list(self.bg.pos)[0] - 5, list(self.bg.pos)[1])

                    self.rightButton.pos = (list(self.rightButton.pos)[0] - 5, list(self.rightButton.pos)[1])
                    self.leftButton.pos = (list(self.leftButton.pos)[0] - 5, list(self.leftButton.pos)[1])

                    self.leftDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 5, list(self.leftDoorOpen.pos)[1])
                    self.leftDoorClose.pos = (list(self.leftDoorClose.pos)[0] - 5, list(self.leftDoorClose.pos)[1])
                    self.leftDoorSpr.pos = (list(self.leftDoorSpr.pos)[0] - 5, list(self.leftDoorSpr.pos)[1])

                    self.rightDoorOpen.pos = (list(self.leftDoorOpen.pos)[0] - 5, list(self.leftDoorOpen.pos)[1])
                    self.rightDoorClose.pos = (list(self.rightDoorClose.pos)[0] - 5, list(self.rightDoorClose.pos)[1])
                    self.rightDoorSpr.pos = (list(self.rightDoorSpr.pos)[0] - 5, list(self.rightDoorSpr.pos)[1])

                    self.leftDoorButton.pos = (list(self.leftDoorButton.pos)[0] - 5, list(self.leftDoorButton.pos)[1])
                    self.leftLightButton.pos = (list(self.leftLightButton.pos)[0] - 5, list(self.leftLightButton.pos)[1])
                    self.rightDoorButton.pos = (list(self.rightDoorButton.pos)[0] - 5, list(self.rightDoorButton.pos)[1])
                    self.rightLightButton.pos = (list(self.rightLightButton.pos)[0] - 5, list(self.rightLightButton.pos)[1])

                    self.movingright = True

                self.bg.changeImg("office\\powerdown\\0")

                # if self.runAtSceneStart == 0:  #self.powerDownStage == 0 and
                #     pygame.mixer.stop()
                #     self.powerdown.play(0, maxtime=random.randint(8000, 15000))
                #     self.runAtSceneStart = 1
                #     if not pygame.mixer.get_busy():
                #         self.musicbox.play(0, maxtime=random.randint(5000, self.musicbox.get_lenght() * 1000))
                #
                #
                # #if self.powerDownStage == 1 and self.runAtSceneStart == 0:

                self.scaregroup.update()
                self.scaregroup.draw(self.screen)

            elif self.scene == "6am":
                if self.runAtFrameStart == 0:
                    pygame.mixer.stop()
                    self.screen.fill((0,0,0))
                    self.screen.blit(pygame.font.Font(None, 80).render("5 AM", True, (255,255,255)), (544,298))
                    self.channelOne.set_volume(1.0)
                    self.channelOne.play(self.chimes, loops=0)
                    self.oldTime = self.current_Milliseconds()
                    self.runAtFrameStart = 1
                try:
                    if self.current_Milliseconds() >= self.oldTime + 4500:
                        self.channelTwo.play(self.children, loops=0)
                        self.screen.fill((0,0,0))
                        self.screen.blit(pygame.font.Font(None, 80).render("6 AM", True, (255,255,255)), (544,298))
                        del self.oldTime
                except:
                    pass

                if not self.channelOne.get_busy() and self.runAtFrameStart == 1:
                    self.scene = "end"
                    self.runAtFrameStart = 0

            elif self.scene == "end":

                self.scaregroup.add(self.bg)

                if self.runAtFrameStart == 0:
                    pygame.mixer.stop()
                    self.channelOne.set_volume(1.0)
                    self.channelOne.play(self.musicbox, loops=-1)
                    self.runAtFrameStart = 1

                if self.gmode == "normal":
                    self.bg.changeImg("ending\\normal")

                elif self.gmode == "overtime":
                    self.bg.changeImg("ending\\overtime")

                elif self.gmode == "custom":
                    self.bg.changeImg("ending\\custom")

                self.scaregroup.update()
                self.scaregroup.draw(self.screen)

            if Globals.animatronics[2].foxstatus == 3 and self.lastcam == "cam2a":
                Globals.animatronics[2].foxstatus = 4

            if Globals.animatronics[2].foxstatus == 4 and not self.leftdoor:
                self.securityOffice()
                Globals.animatronics[2].foxstatus = 5

            if self.scene == "office" and not self.leftlight and not self.rightlight and Globals.animatronics[2].foxstatus != 5:
                self.channelThree.set_volume(0.0)

            if self.scene == "office" and (self.leftlight or self.rightlight):
                self.channelThree.set_volume(1.0)

            pygame.display.update()
            pygame.display.flip()
            self.FPSCLOCK.tick(self.fps)

    def shutdown(self): #Shuts down the whole game.
        utils.debugprint("Shutting down...")
        pygame.quit()
        for animatronic in Globals.animatronics:
            animatronic.dmove("off")
        del self
        sys.exit(0)
        os._exit(0)
        os.system("exit")

    def changeCamera(self, camera):
        self.channelNine.play(self.blip, 0)
        self.camgroup.draw(self.screen)
        self.camgroup.update()
        if camera == "cam1c":
            Globals.animatronics[2].foxviewing = True

        else:
            Globals.animatronics[2].foxviewing = False

        if camera == "cam2a" and Globals.animatronics[2].foxstatus == 3:
            Globals.animatronics[2].foxstatus = 4

        pygame.time.wait(100)
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
        if self.time >= 6 or self.time == "win" and self.killed != True: #This is what happens after 6AM. Yay!
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
        #utils.debugprint(("Foxkind door check.")
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
            self.channelFour.play(self.doorSound, 0)
            self.leftdoor = True
            self.usage += 1
            return None

        if self.leftdoor == True:
            self.channelFour.play(self.doorSound, 0)
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
            self.channelFour.play(self.doorSound, 0)
            self.rightdoor = True
            self.usage += 1
            return None

        if self.rightdoor == True:
            self.channelFour.play(self.doorSound, 0)
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
        utils.debugprint("Open camera")
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
        self.runAtSceneStart = 0
        utils.debugprint("Camera opened")
        return None

    def securityOffice(self):
        utils.debugprint("Go back into office")
        Globals.animatronics[2].foxviewing = False
        self.usage -= 1
        self.putdown.play(0)
        pygame.time.delay(1000)
        pygame.mixer.stop()
        self.scene = "office"
        self.runAtSceneStart = 0
        for animatronic in Globals.animatronics:
            if animatronic.location == "inside":
                utils.debugprint("%s was inside!" % (animatronic.name), animatronic)
                self.scene = "scarejump"
        utils.debugprint("Back into office")
        return None

    def current_Milliseconds(self): return int(round(time.time() * 1000))

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
