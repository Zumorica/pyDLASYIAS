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
import pyDLASYIAS.spr as spr
import pyDLASYIAS.snd as snd
import pyDLASYIAS.utils.functions as utils
import pyDLASYIAS.pyganim as pyganim
from pygame.locals import *

class animatronic():
    '''Class for the other players.'''
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        if self.kind != "fox":
            self.location = "cam1a"
        else:
            self.location = "cam1c"
            self.status = 1

class guardMain():
    '''Class for the guard game.'''
    def __init__(self, gmode="custom", power=100, time=0, sectohour=86,
                 width=1280, height=720, fps=40, socket=None):

        Globals.main = self
        self.gmode = gmode
        self.leftdoor = False
        self.rightdoor = False
        self.leftlight = False
        self.rightlight = False
        self.power = power
        self.killed = False
        self.time = time - 1
        self.sectohour = sectohour
        self.usage = 2  # Compensate for runAtSceneStart in office.
        self.scene = "office"
        self.lastcam = "cam1a"
        self.width = width
        self.height = height
        self.running = True
        self.fps = fps
        self.FPSCLOCK = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.mousex = 0
        self.mousey = 0
        self.runAtSceneStart = 0
        self.runonce = 0
        self.oldTime = 0
        self.staticTime = 0
        self.camMovement = "left"
        self.powerDownStage = 0
        self.camButtonCooldown = False
        self.leftDoorReversed = False
        self.rightDoorReversed = False
        self.cameraAnimReversed = False
        self.lastBgPos = (0, 0)
        self.lastLBPos = (0, 0)
        self.lastRBPos = (0, 0)
        self.alphaStatic = True
        self.static = False
        self.fullscreen = False
        self.rabbit = animatronic("Rabbit", "rabbit")
        self.chicken = animatronic("Chicken", "chicken")
        self.fox = animatronic("Fox", "fox")
        self.bear = animatronic("Bear", "bear")
        self.leftDiscovered = False
        self.rightDiscovered = False
        self.movingleft = False
        self.movingright = False
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.movable = [spr.bg, spr.rightButton, spr.leftButton, spr.leftDoor, \
                        spr.rightDoor, spr.leftDoorButton, spr.rightDoorButton,\
                        spr.leftLightButton, spr.rightLightButton]
        self.mainLoop()

    def mainLoop(self):
        '''Main game loop.'''

        spr.cameraAnim.state = pyganim.PAUSED
        pygame.init()

        while self.running:

            Globals.mouseClick = False
            Globals.pos = self.mousex, self.mousey
            pygame.display.set_caption("--pyDLASYIAS %s-- -%s FPS-" %(Globals.version, round(self.FPSCLOCK.get_fps())))

            for event in pygame.event.get():

                # utils.debugprint(event, writetolog=False)

                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    self.shutdown()

                if event.type == KEYUP and event.key == K_F11:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((self.width, self.height), FULLSCREEN, 32)
                        self.fullscreen = True

                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
                        self.fullscreen = False

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    self.mousex, self.mousey = event.pos
                    Globals.mouseClick = True

            if self.scene == "office":

                if self.runonce == 0:

                    pygame.mixer.stop()
                    snd.channelOne.play(snd.fanSound, -1)
                    snd.channelTwo.play(snd.ambience, -1)
                    snd.channelThree.play(snd.lightHum, -1)
                    snd.channelEighteen.play(snd.eerieAmbience, -1)
                    snd.channelTwentyone.play(snd.robotVoice, -1)

                    snd.channelTwo.set_volume(0.5)
                    snd.channelEighteen.set_volume(0.0)
                    snd.channelTwenty.set_volume(0.1)
                    snd.channelTwentyone.set_volume(0.0)
                    snd.channelTwentytwo.set_volume(0.25)
                    snd.channelEleven.set_volume(0.05)
                    snd.channelTen.set_volume(0.0)
                    snd.channelFour.set_volume(0.5)

                    if self.gmode != "survival":
                        threading.Timer(0.01, self.hourTimer).start()
                    threading.Timer(0.01, self.powerTimer).start()
                    self.runonce = 1

                if self.runAtSceneStart == 0 and not self.power < 0:
                    spr.bg.pos = self.lastBgPos
                    snd.channelOne.set_volume(float(round(((-spr.bg.rect.topleft[0] / 1000) + 0.3), 3)), float(round((0.7 + (spr.bg.rect.topleft[0] / 1000)), 3)))
                    snd.channelEleven.set_volume(0.05)
                    snd.channelSeven.set_volume(0.0)
                    snd.channelTwentyone.set_volume(0.0)
                    snd.channelTen.set_volume(0.0)
                    self.usage -= 1
                    self.runAtSceneStart = 1

                if self.movingright and self.bear.location == "inside":
                    self.changeScene("scarejump")

                if self.fox.status == 5 and self.leftdoor != True:
                    self.changeScene("scarejump")

                if self.time >= 6:
                    self.changeScene("6am")

                if self.power < 0:
                    self.changeScene("powerdown")

                spr.officegroup.add(spr.bg)
                spr.officegroup.change_layer(spr.bg, 0)

                if spr.leftButton.rect.colliderect(self.screen.get_rect()):
                    spr.officegroup.add(spr.leftButton, layer=1)
                    spr.officegroup.add(spr.leftDoorButton, layer=2)
                    spr.officegroup.add(spr.leftLightButton, layer=2)

                elif spr.officegroup.has(spr.leftButton):
                    spr.officegroup.remove(spr.leftButton)

                if spr.rightButton.rect.colliderect(self.screen.get_rect()):
                    spr.officegroup.add(spr.rightButton, layer=1)
                    spr.officegroup.add(spr.rightDoorButton, layer=2)
                    spr.officegroup.add(spr.rightLightButton, layer=2)

                elif spr.officegroup.has(spr.rightButton):
                    spr.officegroup.remove(spr.rightButton)

                if spr.camButton.rect.colliderect(self.screen.get_rect()):
                    spr.officegroup.add(spr.camButton, layer=4)

                elif spr.officegroup.has(spr.camButton):
                    spr.officegroup.remove(spr.camButton)

                if spr.leftDoor.rect.colliderect(self.screen.get_rect()):
                    spr.officegroup.add(spr.leftDoor, layer=3)

                elif spr.officegroup.has(spr.leftDoor):
                    spr.officegroup.remove(spr.leftDoor)

                if spr.rightDoor.rect.colliderect(self.screen.get_rect()):
                    spr.officegroup.add(spr.rightDoor, layer=3)

                elif spr.officegroup.has(spr.rightDoor):
                    spr.officegroup.remove(spr.rightDoor)

                self.movingleft = False
                self.movingright = False

                if self.mousex in range(0, 150) and spr.bg.rect.topleft[0] in range(-400, -5) and not self.movingright:
                    for s in self.movable:
                        s.pos = (s.pos[0] + 15, s.pos[1])
                        s.update()

                    self.movingleft = True

                if self.mousex in range(150, 315) and spr.bg.rect.topleft[0] in range(-400, -5) and not self.movingright:
                    for s in self.movable:
                        s.pos = (s.pos[0] + 10, s.pos[1])
                        s.update()

                    self.movingleft = True

                if self.mousex in range(315, 540) and spr.bg.rect.topleft[0] in range(-400, -5) and not self.movingright:
                    for s in self.movable:
                        s.pos = (s.pos[0] + 5, s.pos[1])
                        s.update()

                    self.movingleft = True

                if self.mousex in range(1140, 1280) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
                    for s in self.movable:
                        s.pos = (s.pos[0] - 15, s.pos[1])
                        s.update()

                    self.movingright = True

                if self.mousex in range(1000, 1140) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
                    for s in self.movable:
                        s.pos = (s.pos[0] - 10, s.pos[1])
                        s.update()

                    self.movingright = True

                if self.mousex in range(750, 1000) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
                    for s in self.movable:
                        s.pos = (s.pos[0] - 5, s.pos[1])
                        s.update()

                    self.movingright = True

                if spr.leftLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.leftLight()

                if spr.leftDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.leftDoor()

                if spr.rightLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.rightLight()

                if spr.rightDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.rightDoor()

                if spr.camButton.rect.collidepoint(Globals.pos) and not self.camButtonCooldown:
                    self.camButtonCooldown = True
                    self.changeScene("cam")

                if not spr.camButton.rect.collidepoint(Globals.pos) and not spr.cameraAnim.state == pyganim.PLAYING:
                    self.camButtonCooldown = False

                if self.leftlight and not self.rightlight:
                    if self.rabbit.location == "leftdoor":
                        spr.bg.changeImg("office\\r")

                    else:
                        spr.bg.changeImg(random.choice(["office\\1", "office\\0"]))

                elif not self.leftlight and self.rightlight:
                    if self.chicken.location == "rightdoor":
                        spr.bg.changeImg("office\\c")

                    else:
                        spr.bg.changeImg(random.choice(["office\\2", "office\\0"]))

                elif not self.leftlight and not self.rightlight:
                    spr.bg.changeImg("office\\0")

                if not self.leftlight and not self.leftdoor:
                    spr.leftButton.changeImg("office\\button\\left\\0")

                elif self.leftlight and self.leftdoor:
                    spr.leftButton.changeImg("office\\button\\left\\dl")

                elif self.leftlight and not self.leftdoor:
                    spr.leftButton.changeImg("office\\button\\left\\l")

                elif not self.leftlight and self.leftdoor:
                    spr.leftButton.changeImg("office\\button\\left\\d")

                if not self.rightlight and not self.rightdoor:
                    spr.rightButton.changeImg("office\\button\\right\\0")

                elif self.rightlight and self.rightdoor:
                    spr.rightButton.changeImg("office\\button\\right\\dl")

                elif self.rightlight and not self.rightdoor:
                    spr.rightButton.changeImg("office\\button\\right\\l")

                elif not self.rightlight and self.rightdoor:
                    spr.rightButton.changeImg("office\\button\\right\\d")

                self.lastBgPos = spr.bg.pos

                snd.channelOne.set_volume(float(round(((-spr.bg.rect.topleft[0] / 1000) + 0.3), 3)), float(round((0.7 + (spr.bg.rect.topleft[0] / 1000)), 3)))

                spr.officegroup.draw(self.screen)
                spr.officegroup.update()

                for animatronic in Globals.animatronics:
                    animatronic.beingWatched = False

                if self.time == 0:
                    self.timeLabel = self.font.render("12 PM", True, (255, 255, 255))
                    self.screen.blit(self.timeLabel, (1040, 60))
                else:
                    self.timeLabel = self.font.render("%s AM" % (self.time), True, (255, 255, 255))
                    self.screen.blit(self.timeLabel, (1040, 60))

                self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255, 255, 255))
                self.usageLabel = self.font.render("Usage: %s" %(self.usage), True, (255, 255, 255))

                self.screen.blit(self.powerLabel, (50, 520))
                self.screen.blit(self.usageLabel, (50, 550))

            elif self.scene == "cam":

                self.alphaStatic = True
                self.static = False
                snd.channelTen.set_volume(0.0)

                if self.static:
                    spr.bg.pos = [0, 0]

                if self.staticTime:
                    self.static = True
                    self.alphaStatic = False
                    self.staticTime -= 1
                    snd.channelTen.set_volume(0.5)

                if self.time >= 6:
                    self.changeScene("6am")

                if self.power < 0:
                    self.changeScene("office")

                if self.runAtSceneStart == 0 and not self.power < 0:
                    spr.bg.pos = [0, 0]
                    snd.channelSeven.play(snd.cameraSoundTwo, -1)
                    snd.channelTen.play(random.choice([snd.garble, snd.garbleTwo, snd.garbleThree]), -1)
                    snd.channelSeven.set_volume(1.0)
                    snd.channelOne.set_volume(0.03, 0.07)
                    self.changeCamera(self.lastcam)
                    self.usage += 1
                    self.runAtSceneStart = 1

                spr.camgroup.add(spr.camButton, layer=10)
                spr.camgroup.add(spr.map, layer=8)
                spr.camgroup.add(spr.camButtonOneA, layer=10)
                spr.camgroup.add(spr.camButtonOneB, layer=10)
                spr.camgroup.add(spr.camButtonOneC, layer=10)
                spr.camgroup.add(spr.camButtonTwoA, layer=10)
                spr.camgroup.add(spr.camButtonTwoB, layer=10)
                spr.camgroup.add(spr.camButtonThree, layer=10)
                spr.camgroup.add(spr.camButtonFourA, layer=10)
                spr.camgroup.add(spr.camButtonFourB, layer=10)
                spr.camgroup.add(spr.camButtonFive, layer=10)
                spr.camgroup.add(spr.camButtonSix, layer=10)
                spr.camgroup.add(spr.camButtonSeven, layer=10)

                if self.fox.status != 4:
                    spr.camgroup.add(spr.bg, layer=0)


                if spr.camButtonOneA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam1a")

                if spr.camButtonOneB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam1b")

                if spr.camButtonOneC.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam1c")

                if spr.camButtonTwoA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam2a")

                if spr.camButtonTwoB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam2b")

                if spr.camButtonThree.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam3")

                if spr.camButtonFourA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam4a")

                if spr.camButtonFourB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam4b")

                if spr.camButtonFive.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam5")

                if spr.camButtonSix.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam6")

                if spr.camButtonSeven.rect.collidepoint(Globals.pos) and Globals.mouseClick:
                    self.changeCamera("cam7")

                if self.lastcam == "cam1a":

                    if self.rabbit.location == "cam1a" and self.chicken.location == "cam1a" and self.bear.location == "cam1a":
                        spr.bg.changeImg("cameras\\cam1a\\brc")

                    elif self.rabbit.location != "cam1a" and self.chicken.location == "cam1a" and self.bear.location == "cam1a":
                        spr.bg.changeImg("cameras\\cam1a\\bc")

                    elif self.rabbit.location == "cam1a" and self.chicken.location != "cam1a" and self.bear.location == "cam1a":
                        spr.bg.changeImg("cameras\\cam1a\\br")

                    elif self.rabbit.location != "cam1a" and self.chicken.location != "cam1a" and self.bear.location == "cam1a":
                        spr.bg.changeImg("cameras\\cam1a\\b")

                    elif self.rabbit.location != "cam1a" and self.chicken.location != "cam1a" and self.bear.location != "cam1a":
                        spr.bg.changeImg("cameras\\cam1a\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam1b":

                    if self.rabbit.location == "cam1b" and self.chicken.location == "cam1b":
                        spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",  "cameras\\misc\\static\\2", "cameras\\misc\\static\\3", "cameras\\misc\\static\\4", "cameras\\misc\\static\\5", "cameras\\misc\\static\\6"]))

                    elif self.rabbit.location == "cam1b" and self.chicken.location != "cam1b":
                        spr.bg.changeImg("cameras\\cam1b\\r")

                    elif self.rabbit.location != "cam1b" and self.chicken.location == "cam1b":
                        spr.bg.changeImg("cameras\\cam1b\\c")

                    elif self.rabbit.location != "cam1b" and self.chicken.location != "cam1b" and self.bear.location == "cam1b":
                        spr.bg.changeImg("cameras\\cam1b\\b")

                    elif self.rabbit.location != "cam1b" and self.chicken.location != "cam1b" and self.bear.location != "cam1b":
                        spr.bg.changeImg("cameras\\cam1b\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam1c":

                    if self.fox.status == 0:
                        spr.bg.changeImg("cameras\\cam1c\\0")

                    elif self.fox.status == 1:
                        spr.bg.changeImg("cameras\\cam1c\\2")

                    elif self.fox.status == 2:
                        spr.bg.changeImg("cameras\\cam1c\\3")

                    elif self.fox.status == 3:
                        spr.bg.changeImg("cameras\\cam1c\\4")

                    elif self.fox.status == 4:
                        spr.bg.changeImg("cameras\\cam1c\\4")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam2a":

                    if self.fox.status != 4:
                        if self.rabbit.location == "cam2a":
                            spr.bg.changeImg(random.choice(["cameras\\cam2a\\0", "cameras\\cam2a\\r"]))

                        elif self.rabbit.location != "cam2a":
                            spr.bg.changeImg(random.choice(["cameras\\cam2a\\0", "cameras\\cam2a\\1"]))

                        else:
                            self.alphaStatic = False
                            self.static = True

                    else:
                        spr.camgroup.remove(spr.bg)
                        spr.camgroup.add(spr.foxSprinting, layer=0)
                        if spr.foxSprinting.has_Finished():
                            self.fox.status = 5
                            spr.camgroup.remove(spr.foxSprinting)
                            spr.camgroup.add(spr.bg)
                            self.changeScene("office")
                            self.changeCamera("cam1a")

                elif self.lastcam == "cam2b":

                    if self.rabbit.location == "cam2b":
                        snd.channelTwentyone.set_volume(random.uniform(0.1, 1.0))
                        spr.bg.changeImg(random.choice(["cameras\\cam2b\\r", "cameras\\cam2b\\r-1"]))

                    elif self.rabbit.location != "cam2b":
                        spr.bg.changeImg("cameras\\cam2b\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam3":

                    if self.rabbit.location == "cam3":
                        spr.bg.changeImg("cameras\\cam3\\r")

                    elif self.rabbit.location != "cam3":
                        spr.bg.changeImg("cameras\\cam3\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam4a":

                    if self.chicken.location == "cam4a":
                        spr.bg.changeImg("cameras\\cam4a\\c")

                    elif self.chicken.location != "cam4a" and self.bear.location == "cam4a":
                        spr.bg.changeImg("cameras\\cam4a\\b")

                    elif self.chicken.location != "cam4a" and self.bear.location != "cam4a":
                        spr.bg.changeImg("cameras\\cam4a\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam4b":

                    if self.chicken.location == "cam4b":
                        snd.channelTwentyone.set_volume(random.uniform(0.1, 1.0))
                        spr.bg.changeImg(random.choice(["cameras\\cam4b\\c", "cameras\\cam4b\\c-1", "cameras\\cam4b\\c-2"]))

                    elif self.chicken.location != "cam4b" and self.bear.location == "cam4b":
                        snd.channelTwentyone.set_volume(random.uniform(0.1, 1.0))
                        spr.bg.changeImg("cameras\\cam4b\\b")

                    elif self.chicken.location != "cam4b" and self.bear.location != "cam4b":
                        spr.bg.changeImg("cameras\\cam4b\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam5":

                    if self.rabbit.location == "cam5":
                        spr.bg.changeImg("cameras\\cam5\\r")

                    elif self.rabbit.location != "cam5":
                        spr.bg.changeImg("cameras\\cam5\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                elif self.lastcam == "cam6":

                    spr.bg.pos = [0,0]
                    self.alphaStatic = False
                    self.static = False

                    if self.chicken.location == "cam6":
                        snd.channelEleven.queue(random.choice([snd.pots, snd.potsTwo, snd.potsThree, snd.potsFour]))

                    if self.bear.location == "cam6":
                        snd.channelEleven.queue(snd.musicBox)

                    snd.channelEleven.set_volume(random.uniform(0.6, 0.8))

                    spr.bg.changeImg("cameras\\misc\\black")

                elif self.lastcam == "cam7":

                    if self.chicken.location == "cam7" and self.bear.location != "cam7":
                        spr.bg.changeImg("cameras\\cam7\\c")

                    elif self.chicken.location != "cam7" and self.bear.location == "cam7":
                        spr.bg.changeImg("cameras\\cam7\\b")

                    elif self.chicken.location != "cam7" and self.bear.location != "cam7":
                        spr.bg.changeImg("cameras\\cam7\\0")

                    else:
                        self.alphaStatic = False
                        self.static = True

                if spr.camButton.rect.collidepoint(Globals.pos) and not self.camButtonCooldown:
                    self.camButtonCooldown = True
                    self.changeScene("office")

                if not spr.camButton.rect.collidepoint(Globals.pos):
                    self.camButtonCooldown = False

                if spr.bg.rect.topright[0] == 1270 and not self.static and self.alphaStatic:
                    self.camMovement = "right"

                if spr.bg.rect.topleft[0] == 10 and not self.static and self.alphaStatic:
                    self.camMovement = "left"

                if self.camMovement == "right" and not self.static and self.alphaStatic:
                    spr.bg.pos = (spr.bg.pos[0] + 2, spr.bg.pos[1])

                if self.camMovement == "left" and not self.static and self.alphaStatic:
                    spr.bg.pos = (spr.bg.pos[0] - 2, spr.bg.pos[1])

                for animatronic in Globals.animatronics:
                    if animatronic.location == self.lastcam:
                        animatronic.beingWatched = True

                    else:
                        animatronic.beingWatched = False

                if self.alphaStatic:
                    spr.camgroup.add(spr.staticTransparent, layer=2)
                    spr.staticTransparent.changeImg(random.choice(["cameras\\misc\\static\\transparent\\0", "cameras\\misc\\static\\transparent\\1",
                                                                   "cameras\\misc\\static\\transparent\\2", "cameras\\misc\\static\\transparent\\3",
                                                                   "cameras\\misc\\static\\transparent\\4", "cameras\\misc\\static\\transparent\\5",
                                                                   "cameras\\misc\\static\\transparent\\6", "cameras\\misc\\static\\transparent\\7"]))
                if not self.alphaStatic:
                    spr.camgroup.remove(spr.staticTransparent)

                if self.static:
                    spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                    "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                    "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                    "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

                spr.camgroup.draw(self.screen)
                spr.camgroup.update()

                if self.time == 0:
                    self.timeLabel = self.font.render("12 PM", True, (255, 255, 255))
                    self.screen.blit(self.timeLabel, (1040, 60))
                else:
                    self.timeLabel = self.font.render("%s AM" % (self.time), True, (255, 255, 255))
                    self.screen.blit(self.timeLabel, (1040, 60))

                self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255, 255, 255))
                self.usageLabel = self.font.render("Usage: %s" %(self.usage), True, (255, 255, 255))

                self.screen.blit(self.powerLabel, (50, 520))
                self.screen.blit(self.usageLabel, (50, 550))
                self.screen.blit(self.font.render(Globals.camdic[self.lastcam], True, (255,255,255)), (832,292))

            elif self.scene == "scarejump":

                if self.time >= 6:
                    self.changeScene("6am")

                if self.powerDownStage == 4:
                    if self.runAtSceneStart == 0:
                        pygame.mixer.stop()
                        spr.bearPowerdownScarejump.play()
                        snd.channelNine.play(snd.xscream, 0)
                        self.runAtSceneStart = 1

                    spr.bearPowerdownScarejump.blit(self.screen, (0,0))

                    if spr.bearPowerdownScarejump.isFinished():
                        self.killed = True
                        self.shutdown()

                for animatronic in Globals.animatronics:
                    if (animatronic.location == "inside" or animatronic.status == 5) and (self.power > 0 and not self.killed):
                        if self.runAtSceneStart == 0:
                            snd.channelNine.play(snd.xscream, 0)
                            spr.chickenScarejump.play()
                            spr.rabbitScarejump.play()
                            spr.bearNormalScarejump.play()
                            spr.foxScarejump.play()
                            self.runAtSceneStart = 1

                        if animatronic.kind == "chicken":
                            spr.chickenScarejump.blit(self.screen, (0, 0))
                            if spr.chickenScarejump.isFinished():
                                self.killed = True
                                self.shutdown()

                        if animatronic.kind == "rabbit":
                            spr.rabbitScarejump.blit(self.screen, (0, 0))
                            if spr.rabbitScarejump.isFinished():
                                self.killed = True
                                self.shutdown()

                        if animatronic.kind == "bear":
                            spr.bearNormalScarejump.blit(self.screen, (0, 0))
                            if spr.bearNormalScarejump.isFinished():
                                self.killed = True
                                self.shutdown()

                        if animatronic.kind == "fox":
                            spr.foxScarejump.blit(self.screen, (0, 0))
                            if spr.foxScarejump.isFinished():
                                self.killed = True
                                self.shutdown()

            elif self.scene == "powerdown":

                spr.scaregroup.add(spr.bg)

                if self.time >= 6:
                    self.changeScene("6am")

                self.movingleft = False
                self.movingright = False

                if self.mousex in range(0, 150) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
                    for s in self.movable:
                        s.pos = (s.pos[0] + 15, s.pos[1])
                        s.update()

                    self.movingleft = True

                if self.mousex in range(150, 315) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
                    for s in self.movable:
                        s.pos = (s.pos[0] + 10, s.pos[1])
                        s.update()

                    self.movingleft = True

                if self.mousex in range(315, 540) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
                    for s in self.movable:
                        s.pos = (s.pos[0] + 5, s.pos[1])
                        s.update()

                    self.movingleft = True

                if self.mousex in range(1140, 1280) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
                    for s in self.movable:
                        s.pos = (s.pos[0] - 15, s.pos[1])
                        s.update()

                    self.movingright = True

                if self.mousex in range(1000, 1140) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
                    for s in self.movable:
                        s.pos = (s.pos[0] - 10, s.pos[1])
                        s.update()

                    self.movingright = True

                if self.mousex in range(750, 1000) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
                    for s in self.movable:
                        s.pos = (s.pos[0] - 5, s.pos[1])
                        s.update()

                    self.movingright = True

                if self.runAtSceneStart == 0:
                    pygame.mixer.stop()
                    spr.bg.changeImg("office\\powerdown\\0")
                    snd.channelOne.set_volume(1.0)
                    snd.channelTwo.set_volume(0.5)
                    snd.channelFour.set_volume(1.0)

                    if self.leftdoor:
                        if not self.leftDoorReversed:
                            spr.leftDoorAnim.reverse()
                            self.leftDoorReversed = True
                        spr.leftDoorAnim.play()
                        snd.channelFour.play(snd.doorSound, 0)
                        self.leftdoor = False

                    if self.rightdoor:
                        if not self.rightDoorReversed:
                            spr.rightDoorAnim.reverse()
                            self.rightDoorReversed = True
                        spr.rightDoorAnim.play()
                        snd.channelFour.play(snd.doorSound, 0)
                        self.rightdoor = False

                    snd.channelOne.play(snd.powerDown, loops=0)
                    snd.channelOne.fadeout(random.randint(5000, 15000))

                    snd.channelTwo.play(snd.ambienceTwo, loops=0)
                    self.powerDownStage = 1
                    self.runAtSceneStart = 1

                if not snd.channelOne.get_busy() and not snd.channelThirty.get_busy() and self.powerDownStage == 1:
                    snd.channelThirty.set_volume(0.7, 0.3)
                    if random.randint(1, 5) == 1:
                        snd.channelThirty.play(snd.musicBox, loops=0, maxtime=20000)
                    else:
                        snd.channelThirty.play(snd.musicBox, loops=0, maxtime=random.randint(3000, int(snd.musicBox.get_length() * 1000)))
                    self.powerDownStage = 2

                if self.powerDownStage == 2:
                    spr.bg.changeImg(random.choice(["office\\powerdown\\0", "office\\powerdown\\1", "office\\powerdown\\0", "office\\powerdown\\0"]))

                if not snd.channelThirty.get_busy() and self.powerDownStage == 2:
                    self.powerDownStage = 3

                if self.powerDownStage == 3:
                    spr.bg.changeImg("office\\powerdown\\2")
                    self.oldTime = self.current_Milliseconds()
                    self.powerDownStage += 1

                if self.current_Milliseconds() >= self.oldTime + 6000 and self.powerDownStage == 4:
                    self.changeScene("scarejump")

                spr.scaregroup.update()
                spr.scaregroup.draw(self.screen)

            elif self.scene == "6am":
                if self.runAtSceneStart == 0:
                    pygame.mixer.stop()
                    self.screen.fill((0, 0, 0))
                    self.screen.blit(pygame.font.Font(None, 80).render("5 AM", True, (255, 255, 255)), (544, 298))
                    snd.channelOne.set_volume(1.0)
                    snd.channelOne.play(snd.chimes, loops=0)
                    self.oldTime = self.current_Milliseconds()
                    self.runAtSceneStart = 2
                try:
                    if self.current_Milliseconds() >= self.oldTime + 4500:#
                        snd.channelTwo.play(snd.children, loops=0)
                        self.screen.fill((0, 0, 0))
                        self.screen.blit(pygame.font.Font(None, 80).render("6 AM", True, (255, 255, 255)), (544, 298))
                        del self.oldTime
                except:
                    pass

                if not snd.channelOne.get_busy() and self.runAtSceneStart == 2:
                    self.changeScene("end")

            elif self.scene == "end":

                spr.scaregroup.add(spr.bg)

                if self.runAtSceneStart == 0:
                    pygame.mixer.stop()
                    spr.bg.pos = (0, 0)
                    snd.channelOne.set_volume(1.0)
                    snd.channelOne.play(snd.musicBox, loops=-1)
                    self.runAtSceneStart = 1

                if self.gmode == "normal":
                    spr.bg.changeImg("ending\\normal")

                elif self.gmode == "overtime":
                    spr.bg.changeImg("ending\\overtime")

                elif self.gmode == "custom":
                    spr.bg.changeImg("ending\\custom")

                spr.scaregroup.update()
                spr.scaregroup.draw(self.screen)

            if self.fox.cooldown and self.fox.location != "off":
                self.fox.cooldown -= 1

            if self.scene == "office" and not self.leftlight and not self.rightlight and self.fox.status != 5:
                snd.channelThree.set_volume(0.0)

            if self.scene == "office" and self.leftlight:
                snd.channelThree.set_volume(0.7, 0.3)

            if self.scene == "office" and self.rightlight:
                snd.channelThree.set_volume(0.3, 0.7)

            if spr.leftDoorAnim.getCurrentFrame() == spr.leftDoorAnim.getFrame(15) and self.leftdoor:
                spr.leftDoor.changeImg("office\\doors\\left\\15")

            if spr.leftDoorAnim.state == pyganim.PLAYING:
                if not self.leftdoor:
                    spr.leftDoor.changeImg("office\\doors\\left\\0")

                spr.leftDoorAnim.blit(self.screen, tuple(spr.leftDoor.pos))
                self.screen.blit(self.powerLabel, (50, 520))
                self.screen.blit(self.usageLabel, (50, 550))
                self.screen.blit(spr.camButton.image, tuple(spr.camButton.pos))

            if spr.rightDoorAnim.getCurrentFrame() == spr.rightDoorAnim.getFrame(15) and self.rightdoor:
                spr.rightDoor.changeImg("office\\doors\\right\\15")

            if spr.rightDoorAnim.state == pyganim.PLAYING:
                if not self.rightdoor:
                    spr.rightDoor.changeImg("office\\doors\\right\\0")

                spr.rightDoorAnim.blit(self.screen, tuple(spr.rightDoor.pos))
                self.screen.blit(self.powerLabel, (50, 520))
                self.screen.blit(self.usageLabel, (50, 550))
                self.screen.blit(self.timeLabel, (1400, 50))

            if spr.cameraAnim.state == pyganim.PLAYING:
                spr.cameraAnim.blit(self.screen, (0, 0))

            if spr.cameraAnim.getCurrentFrame() == spr.cameraAnim.getFrame(10) and not self.cameraAnimReversed and self.scene == "office":
                self.scene = "cam"
                spr.cameraAnim.state = pyganim.PAUSED
                self.runAtSceneStart = 0
                self.oldtime = 0

            # self.screen.blit(self.font.render("%s FPS" % round(self.FPSCLOCK.get_fps()), True, (0,255,0)), (10,10))

            pygame.display.update(spr.bg.rect)

            self.FPSCLOCK.tick(self.fps)

    def shutdown(self):
        utils.debugprint("Shutting down...")
        pygame.quit()
        for animatronic in Globals.animatronics:
            animatronic.move("off", True)
        del self
        sys.exit(0)
        os._exit(0)
        os.system("exit")

    def changeCamera(self, camera):

        snd.channelTwentyone.set_volume(0.0)
        snd.channelEleven.set_volume(0.1)

        if camera == "cam1a":
            spr.camButtonOneA.changeImg("ui\\button\\scam1a")
        else:
            spr.camButtonOneA.changeImg("ui\\button\\cam1a")

        if camera == "cam1b":
            spr.camButtonOneB.changeImg("ui\\button\\scam1b")
        else:
            spr.camButtonOneB.changeImg("ui\\button\\cam1b")

        if camera == "cam1c":
            spr.camButtonOneC.changeImg("ui\\button\\scam1c")
        else:
            spr.camButtonOneC.changeImg("ui\\button\\cam1c")

        if camera == "cam2a":
            spr.camButtonTwoA.changeImg("ui\\button\\scam2a")
        else:
            spr.camButtonTwoA.changeImg("ui\\button\\cam2a")

        if camera == "cam2b":
            spr.camButtonTwoB.changeImg("ui\\button\\scam2b")
        else:
            spr.camButtonTwoB.changeImg("ui\\button\\cam2b")

        if camera == "cam3":
            spr.camButtonThree.changeImg("ui\\button\\scam3")
        else:
            spr.camButtonThree.changeImg("ui\\button\\cam3")

        if camera == "cam4a":
            spr.camButtonFourA.changeImg("ui\\button\\scam4a")
        else:
            spr.camButtonFourA.changeImg("ui\\button\\cam4a")

        if camera == "cam4b":
            spr.camButtonFourB.changeImg("ui\\button\\scam4b")
        else:
            spr.camButtonFourB.changeImg("ui\\button\\cam4b")

        if camera == "cam5":
            spr.camButtonFive.changeImg("ui\\button\\scam5")
        else:
            spr.camButtonFive.changeImg("ui\\button\\cam5")

        if camera == "cam6":
            spr.camButtonSix.changeImg("ui\\button\\scam6")
        else:
            spr.camButtonSix.changeImg("ui\\button\\cam6")

        if camera == "cam7":
            spr.camButtonSeven.changeImg("ui\\button\\scam7")
        else:
            spr.camButtonSeven.changeImg("ui\\button\\cam7")

        snd.channelNine.play(snd.blip, 0)
        spr.camgroup.draw(self.screen)
        spr.camgroup.update()
        if camera == "cam2a" and self.fox.status == 3:
            self.fox.status = 4

        self.lastcam = camera

    def powerTimer(self):
        self.power -= 1

        if self.usage == 1:
            threading.Timer(9.6, self.powerTimer).start()

        elif self.usage == 2:
            threading.Timer(4.8, self.powerTimer).start()

        elif self.usage == 3:
            threading.Timer(random.choice([2.8, 2.9, 3.9]), self.powerTimer).start()

        elif self.usage >= 4:
            threading.Timer(random.choice([1.9, 2.9]), self.powerTimer).start()

    def hourTimer(self):
        self.time += 1

        if self.time == 2 or self.time == 3 or self.time == 4:

            for animatronic in Globals.animatronics:
                if animatronic.kind != "bear":
                    animatronic.ailvl += 1

        threading.Timer(self.sectohour, self.hourTimer).start()

    def leftDoor(self):
        if not self.leftdoor:
            if self.leftDoorReversed:
                spr.leftDoorAnim.reverse()
                self.leftDoorReversed = False
            spr.leftDoorAnim.play()
            snd.channelFour.play(snd.doorSound, 0)
            self.leftdoor = True
            self.usage += 1
            return None

        if self.leftdoor:
            if not self.leftDoorReversed:
                spr.leftDoorAnim.reverse()
                self.leftDoorReversed = True
            spr.leftDoorAnim.play()
            snd.channelFour.play(snd.doorSound, 0)
            self.leftdoor = False
            self.usage -= 1
            return None

    def leftLight(self):
        if self.leftlight:
            self.leftlight = False
            self.usage -= 1
            return None

        if not self.leftlight:
            for animatronic in Globals.animatronics:
                if animatronic.location == "leftdoor" and not self.leftDiscovered:
                    snd.channelNine.play(snd.windowScare, 0)
                    self.leftDiscovered = True
            self.leftlight = True
            if self.rightlight:
                self.rightlight = False
                self.usage -= 1
            self.usage += 1
            return None

    def rightDoor(self):
        if not self.rightdoor:
            if self.rightDoorReversed:
                spr.rightDoorAnim.reverse()
                self.rightDoorReversed = False
            spr.rightDoorAnim.play()
            snd.channelFour.play(snd.doorSound, 0)
            self.rightdoor = True
            self.usage += 1
            return None

        if self.rightdoor:
            if not self.rightDoorReversed:
                spr.rightDoorAnim.reverse()
                self.rightDoorReversed = True
            spr.rightDoorAnim.play()
            snd.channelFour.play(snd.doorSound, 0)
            self.rightdoor = False
            self.usage -= 1
            return None

    def rightLight(self):
        if self.rightlight:
            self.rightlight = False
            self.usage -= 1
            return None

        if not self.rightlight:
            if self.chicken.location == "rightdoor" and not self.rightDiscovered:
                snd.channelNine.play(snd.windowScare, 0)
                self.rightDiscovered = True
            self.rightlight = True

            if self.leftlight == True:
                self.leftlight = False
                self.usage -= 1

            self.usage += 1
            return None

    def changeScene(self, scene):

        if scene == "office":
            if not self.cameraAnimReversed:
                spr.cameraAnim.reverse()
                self.cameraAnimReversed = True

            spr.cameraAnim.state = pyganim.PLAYING
            spr.cameraAnim.play()

            self.fox.cooldown = random.randint(100, 300)

            for animatronic in Globals.animatronics:
                animatronic.beingWatched = False

            snd.putDown.play(0)
            self.scene = "office"

            self.runAtSceneStart = 0
            self.oldtime = 0

            for animatronic in Globals.animatronics:
                if animatronic.location == "inside":
                    self.scene = "scarejump"

        elif scene == "cam":
            if self.cameraAnimReversed:
                spr.cameraAnim.reverse()
                self.cameraAnimReversed = False

            spr.cameraAnim.state = pyganim.PLAYING
            spr.cameraAnim.play()

            if self.leftlight:
                self.usage -= 1
                self.leftlight = False
            if self.rightlight:
                self.usage -= 1
                self.rightlight = False

            snd.putDown.play(0)

        elif scene == "powerdown":
            self.scene = "powerdown"
            self.runAtSceneStart = 0
            self.oldtime = 0

        elif scene == "scarejump":
            self.scene = "scarejump"
            self.runAtSceneStart = 0
            self.oldtime = 0

        elif scene == "dead":
            self.scene = "dead"
            self.runAtSceneStart = 0
            self.oldtime = 0

        elif scene == "6am":
            self.scene = "6am"
            self.runAtSceneStart = 0
            self.oldtime = 0

        elif scene == "end":
            self.scene = "end"
            self.runAtSceneStart = 0
            self.oldtime = 0

    def current_Milliseconds(self): return int(round(time.time() * 1000))

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")

# #!/usr/bin/env python
# import sys
# import os
# import time
# import random
# import _thread
# import threading
# import pygame
# import socket
# import pyDLASYIAS.sprite as sprite
# import pyDLASYIAS.Globals as Globals
# import pyDLASYIAS.spr as spr
# import pyDLASYIAS.snd as snd
# import pyDLASYIAS.utils.functions as utils
# import pyDLASYIAS.pyganim as pyganim
# from pygame.locals import *
#
# class guardMain(object):
#     def __init__(self, power=100, time=0, sectohour=86, width=1280, height=720, fps=60, host="localhost", port=1987):
#
#         Globals.main = self
#
#         sys.setrecursionlimit(5000)
#         threading.stack_size(128*4096)
#
#         self.leftdoor = False
#         self.rightdoor = False
#         self.leftlight = False
#         self.rightlight = False
#         self.power = power
#         self.killed = False
#         self.time = time - 1
#         self.sectohour = sectohour
#         self.usage = 1
#         self.scene = "office"
#         self.lastcam = "cam1a"
#
#         self.host = host
#         self.port = port
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#         self.sock.connect((self.host, self.port))
#         self.sock.sendall(bytes("guard\n", "utf-8"))
#
#         self.received = str(self.sock.recv(1024), "utf-8")
#         threading.Thread(target=self.receiveData, args=()).start()
#
#         self.width = width
#         self.height = height
#         self.running = True
#         self.fps = fps
#
#         self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
#         pygame.display.set_caption("--pyDLASYIAS %s--" %(Globals.version))
#
#         pygame.init()
#         self.FPSCLOCK = pygame.time.Clock()
#
#         self.font = pygame.font.Font(None, 30)
#
#         self.mousex = 0
#         self.mousey = 0
#
#         self.runAtSceneStart = 0
#         self.runonce = 0
#
#         self.oldTime = 0
#
#         self.camMovement = "left"
#
#         self.powerDownStage = 0
#
#         spr.cameraAnim.state = pyganim.PAUSED
#
#         self.camButtonCooldown = False
#
#         self.leftDoorReversed = False
#         self.rightDoorReversed = False
#         self.cameraAnimReversed = False
#
#         self.lastBgPos = (0,0)
#         self.lastLBPos = (0,0)
#         self.lastRBPos = (0,0)
#
#         self.fullscreen = False
#
#         self.bearLocation = "cam1a"
#         self.rabbitLocation = "cam1a"
#         self.chickenLocation = "cam1a"
#         self.foxStatus = 0
#
#         self.animatronics = [self.rabbitLocation, self.chickenLocation, self.bearLocation, self.foxStatus]
#
#         while self.running:
#
#             Globals.mouseClick = False
#             Globals.pos = self.mousex, self.mousey
#
#             for event in pygame.event.get():
#
#                 #utils.debugprint(event, writetolog=False)
#
#                 if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
#                     pygame.quit()
#                     self.shutdown()
#
#                 if event.type == KEYUP and event.key == 292:
#                     if not self.fullscreen:
#                         self.screen = pygame.display.set_mode((self.width, self.height), FULLSCREEN, 32)
#                         pygame.display.set_caption("--pyDLASYIAS %s--" %(Globals.version))
#                         self.fullscreen = True
#
#                     if self.fullscreen:
#                         self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
#                         pygame.display.set_caption("--pyDLASYIAS %s--" %(Globals.version))
#
#
#                 elif event.type == MOUSEMOTION:
#                     self.mousex, self.mousey = event.pos
#
#                 elif event.type == MOUSEBUTTONUP:
#                     self.mousex, self.mousey = event.pos
#                     Globals.mouseClick = True
#
#             if self.scene == "office":
#
#                 if self.runonce == 0:
#                     self.send("guard")
#                     pygame.mixer.stop()
#                     snd.channelOne.play(snd.fanSound, -1)
#                     snd.channelTwo.play(snd.ambience, -1)
#                     snd.channelThree.play(snd.lightHum, -1)
#                     snd.channelEighteen.play(snd.eerieAmbience, -1)
#
#                     snd.channelTwo.set_volume(0.5)
#                     snd.channelEighteen.set_volume(0.0)
#                     snd.channelTwenty.set_volume(0.1)
#                     snd.channelTwentyone.set_volume(0.0)
#                     snd.channelTwentytwo.set_volume(0.25)
#
#                     snd.channelTwentyone.play(snd.robotVoice, -1)
#
#                     self.runonce = 1
#
#                 if self.time >= 6 :
#                     self.changeScene("6am")
#
#                 if self.power < 0:
#                     self.changeScene("powerdown")
#
#                 if self.runAtSceneStart == 0 and not self.power < 0:
#                     self.send("guard -> %s" % (self.scene))
#                     spr.bg.pos = self.lastBgPos
#                     self.runAtSceneStart = 1
#
#                 self.lastBgPos = spr.bg.pos
#
#                 spr.officegroup.add(spr.leftButton)
#                 spr.officegroup.add(spr.rightButton)
#                 spr.officegroup.add(spr.leftDoorButton)
#                 spr.officegroup.add(spr.leftLightButton)
#                 spr.officegroup.add(spr.rightDoorButton)
#                 spr.officegroup.add(spr.rightLightButton)
#                 spr.officegroup.add(spr.camButton)
#                 spr.officegroup.add(spr.leftDoor)
#                 spr.officegroup.add(spr.rightDoor)
#                 spr.officegroup.add(spr.bg)
#
#                 spr.officegroup.change_layer(spr.bg, 0)
#                 spr.officegroup.change_layer(spr.leftButton, 1)
#                 spr.officegroup.change_layer(spr.rightButton, 1)
#                 spr.officegroup.change_layer(spr.leftDoorButton, 2)
#                 spr.officegroup.change_layer(spr.leftLightButton, 2)
#                 spr.officegroup.change_layer(spr.rightDoorButton, 2)
#                 spr.officegroup.change_layer(spr.rightLightButton, 2)
#                 spr.officegroup.change_layer(spr.camButton, 4)
#                 spr.officegroup.change_layer(spr.leftDoor, 3)
#                 spr.officegroup.change_layer(spr.rightDoor, 3)
#
#                 self.movingleft = False
#                 self.movingright = False
#
#                 if self.mousex in range(0, 150) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
#                     spr.bg.pos = (spr.bg.pos[0] + 20, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] + 20, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] + 20, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] + 20, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] + 20, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] + 20, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] + 20, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] + 20, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] + 20, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingleft = True
#
#                 if self.mousex in range(150, 315) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
#                     spr.bg.pos = (spr.bg.pos[0] + 10, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] + 10, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] + 10, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] + 10, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] + 10, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] + 10, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] + 10, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] + 10, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] + 10, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingleft = True
#
#                 if self.mousex in range(315, 540) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
#                     spr.bg.pos = (spr.bg.pos[0] + 5, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] + 5, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] + 5, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] + 5, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] + 5, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] + 5, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] + 5, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] + 5, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] + 5, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingleft = True
#
#                 if self.mousex in range(1140, 1280) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
#                     spr.bg.pos = (spr.bg.pos[0] - 20, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] - 20, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] - 20, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] - 20, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] - 20, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] - 20, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] - 20, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] - 20, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] - 20, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingright = True
#
#                 if self.mousex in range(1000, 1140) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
#                     spr.bg.pos = (spr.bg.pos[0] - 10, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] - 10, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] - 10, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] - 10, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] - 10, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] - 10, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] - 10, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] - 10, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] - 10, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingright = True
#
#                 if self.mousex in range(750, 1000) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
#                     spr.bg.pos = (spr.bg.pos[0] - 5, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] - 5, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] - 5, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] - 5, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] - 5, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] - 5, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] - 5, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] - 5, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] - 5, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingright = True
#
#                 if spr.leftLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.leftLight()
#
#                 if spr.leftDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.leftDoor()
#
#                 if spr.rightLightButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.rightLight()
#
#                 if spr.rightDoorButton.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.rightDoor()
#
#                 if spr.camButton.rect.collidepoint(Globals.pos) and not self.camButtonCooldown:
#                     self.camButtonCooldown = True
#                     self.changeScene("cam")
#
#                 if not spr.camButton.rect.collidepoint(Globals.pos):
#                     self.camButtonCooldown = False
#
#                 if self.leftlight and not self.rightlight:
#                     if self.rabbitLocation == "leftdoor":
#                         spr.bg.changeImg("office\\r")
#
#                     else:
#                         spr.bg.changeImg(random.choice(["office\\1", "office\\0"]))
#
#                 elif not self.leftlight and self.rightlight:
#                     if self.chickenLocation == "rightdoor":
#                         spr.bg.changeImg("office\\c")
#
#                     else:
#                         spr.bg.changeImg(random.choice(["office\\2", "office\\0"]))
#
#                 elif not self.leftlight and not self.rightlight:
#                     spr.bg.changeImg("office\\0")
#
#                 if not self.leftlight and not self.leftdoor:
#                     spr.leftButton.changeImg("office\\button\\left\\0")
#
#                 elif self.leftlight and self.leftdoor:
#                     spr.leftButton.changeImg("office\\button\\left\\dl")
#
#                 elif self.leftlight and not self.leftdoor:
#                     spr.leftButton.changeImg("office\\button\\left\\l")
#
#                 elif not self.leftlight and self.leftdoor:
#                     spr.leftButton.changeImg("office\\button\\left\\d")
#
#                 if not self.rightlight and not self.rightdoor:
#                     spr.rightButton.changeImg("office\\button\\right\\0")
#
#                 elif self.rightlight and self.rightdoor:
#                     spr.rightButton.changeImg("office\\button\\right\\dl")
#
#                 elif self.rightlight and not self.rightdoor:
#                     spr.rightButton.changeImg("office\\button\\right\\l")
#
#                 elif not self.rightlight and self.rightdoor:
#                     spr.rightButton.changeImg("office\\button\\right\\d")
#
#                 spr.officegroup.draw(self.screen)
#                 spr.officegroup.update()
#
#                 if self.time == 0:
#                     self.timeLabel = self.font.render("12 PM", True, (255,255,255))
#                     self.screen.blit(self.timeLabel, (1040,60))
#                 else:
#                     self.timeLabel = self.font.render("%s AM" % (self.time), True, (255,255,255))
#                     self.screen.blit(self.timeLabel, (1040,60))
#
#                 self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255,255,255))
#                 self.usageLabel = self.font.render("Usage: %s" %(self.usage), True, (255,255,255))
#
#                 self.screen.blit(self.powerLabel, (50,520))
#                 self.screen.blit(self.usageLabel, (50,550))
#
#             elif self.scene == "cam":
#
#                 self.notStatic = True
#
#                 if self.time >= 6 :
#                     self.changeScene("6am")
#
#                 if self.power < 0:
#                     self.changeScene("office")
#
#                 if self.runAtSceneStart == 0 and not self.power < 0:
#                     self.send("guard -> %s" % (self.scene))
#                     spr.bg.pos = (0,0)
#                     self.changeCamera(self.lastcam)
#                     snd.channelSeven.play(snd.cameraSoundTwo, -1)
#                     self.runAtSceneStart = 1
#
#                 spr.camgroup.add(spr.camButton)
#                 spr.camgroup.add(spr.map)
#                 spr.camgroup.add(spr.camButtonOneA)
#                 spr.camgroup.add(spr.camButtonOneB)
#                 spr.camgroup.add(spr.camButtonOneC)
#                 spr.camgroup.add(spr.camButtonTwoA)
#                 spr.camgroup.add(spr.camButtonTwoB)
#                 spr.camgroup.add(spr.camButtonThree)
#                 spr.camgroup.add(spr.camButtonFourA)
#                 spr.camgroup.add(spr.camButtonFourB)
#                 spr.camgroup.add(spr.camButtonFive)
#                 spr.camgroup.add(spr.camButtonSix)
#                 spr.camgroup.add(spr.camButtonSeven)
#                 spr.camgroup.add(spr.staticTransparent)
#
#                 if self.foxStatus != 4:
#                     spr.camgroup.add(spr.bg)
#
#                 if self.foxStatus != 4 and spr.camgroup.has(spr.bg):
#                     spr.camgroup.change_layer(spr.bg, 0)
#
#                 spr.camgroup.change_layer(spr.map, 8)
#                 spr.camgroup.change_layer(spr.camButtonOneA, 10)
#                 spr.camgroup.change_layer(spr.camButtonOneB, 10)
#                 spr.camgroup.change_layer(spr.camButtonOneC, 10)
#                 spr.camgroup.change_layer(spr.camButtonTwoA, 10)
#                 spr.camgroup.change_layer(spr.camButtonTwoB, 10)
#                 spr.camgroup.change_layer(spr.camButtonThree, 10)
#                 spr.camgroup.change_layer(spr.camButtonFourA, 10)
#                 spr.camgroup.change_layer(spr.camButtonFourB, 10)
#                 spr.camgroup.change_layer(spr.camButtonFive, 10)
#                 spr.camgroup.change_layer(spr.camButtonSix, 10)
#                 spr.camgroup.change_layer(spr.camButtonSeven, 10)
#                 spr.camgroup.change_layer(spr.camButton, 10)
#                 spr.camgroup.change_layer(spr.staticTransparent, 2)
#
#                 spr.staticTransparent.changeImg(random.choice(["cameras\\misc\\static\\transparent\\0", "cameras\\misc\\static\\transparent\\1",
#                                                                "cameras\\misc\\static\\transparent\\2", "cameras\\misc\\static\\transparent\\3",
#                                                                "cameras\\misc\\static\\transparent\\4", "cameras\\misc\\static\\transparent\\5",
#                                                                "cameras\\misc\\static\\transparent\\6", "cameras\\misc\\static\\transparent\\7"]))
#
#                 if spr.camButtonOneA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam1a")
#
#                 if spr.camButtonOneB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam1b")
#
#                 if spr.camButtonOneC.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam1c")
#
#                 if spr.camButtonTwoA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam2a")
#
#                 if spr.camButtonTwoB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam2b")
#
#                 if spr.camButtonThree.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam3")
#
#                 if spr.camButtonFourA.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam4a")
#
#                 if spr.camButtonFourB.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam4b")
#
#                 if spr.camButtonFive.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam5")
#
#                 if spr.camButtonSix.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam6")
#
#                 if spr.camButtonSeven.rect.collidepoint(Globals.pos) and Globals.mouseClick:
#                     self.changeCamera("cam7")
#
#                 if self.lastcam == "cam1a":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\scam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.rabbitLocation == "cam1a" and self.chickenLocation == "cam1a" and self.bearLocation == "cam1a":
#                         spr.bg.changeImg("cameras\\cam1a\\brc")
#
#                     elif self.rabbitLocation != "cam1a" and self.chickenLocation == "cam1a" and self.bearLocation == "cam1a":
#                         spr.bg.changeImg("cameras\\cam1a\\bc")
#
#                     elif self.rabbitLocation == "cam1a" and self.chickenLocation != "cam1a" and self.bearLocation == "cam1a":
#                         spr.bg.changeImg("cameras\\cam1a\\br")
#
#                     elif self.rabbitLocation != "cam1a" and self.chickenLocation != "cam1a" and self.bearLocation == "cam1a":
#                         spr.bg.changeImg("cameras\\cam1a\\b")
#
#                     elif self.rabbitLocation != "cam1a" and self.chickenLocation != "cam1a" and self.bearLocation != "cam1a":
#                         spr.bg.changeImg("cameras\\cam1a\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#
#                 elif self.lastcam == "cam1b":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\scam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.rabbitLocation == "cam1b" and self.chickenLocation == "cam1b":
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",  "cameras\\misc\\static\\2", "cameras\\misc\\static\\3", "cameras\\misc\\static\\4", "cameras\\misc\\static\\5", "cameras\\misc\\static\\6"]))
#
#                     elif self.rabbitLocation == "cam1b" and self.chickenLocation != "cam1b":
#                         spr.bg.changeImg("cameras\\cam1b\\r")
#
#                     elif self.rabbitLocation != "cam1b" and self.chickenLocation == "cam1b":
#                         spr.bg.changeImg("cameras\\cam1b\\c")
#
#                     elif self.rabbitLocation != "cam1b" and self.chickenLocation != "cam1b" and self.bearLocation == "cam1b":
#                         spr.bg.changeImg("cameras\\cam1b\\b")
#
#                     elif self.rabbitLocation != "cam1b" and self.chickenLocation != "cam1b" and self.bearLocation != "cam1b":
#                         spr.bg.changeImg("cameras\\cam1b\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#                 elif self.lastcam == "cam1c":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\scam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.foxStatus == 0:
#                         spr.bg.changeImg("cameras\\cam1c\\0")
#
#                     elif self.foxStatus == 1:
#                         spr.bg.changeImg("cameras\\cam1c\\2")
#
#                     elif self.foxStatus == 2:
#                         spr.bg.changeImg("cameras\\cam1c\\3")
#
#                     elif self.foxStatus == 3:
#                         spr.bg.changeImg("cameras\\cam1c\\4")
#
#                     elif self.foxStatus == 4:
#                         spr.bg.changeImg("cameras\\cam1c\\4")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#                 elif self.lastcam == "cam2a":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\scam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.foxStatus != 4:
#                         if self.rabbitLocation == "cam2a":
#                             spr.bg.changeImg(random.choice(["cameras\\cam2a\\0", "cameras\\cam2a\\r"]))
#
#                         elif self.rabbitLocation != "cam2a":
#                             spr.bg.changeImg(random.choice(["cameras\\cam2a\\0", "cameras\\cam2a\\1"]))
#
#                         else:
#                             self.notStatic = False
#                             spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                             "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                             "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                             "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#                     else:
#                         spr.camgroup.remove(spr.bg)
#                         spr.camgroup.add(spr.foxSprinting)
#                         spr.camgroup.change_layer(spr.foxSprinting, 0)
#                         if spr.foxSprinting.has_Finished():
#                             self.changeScene("office")
#                             spr.camgroup.remove(spr.foxSprinting)
#
#                 elif self.lastcam == "cam2b":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\scam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.rabbitLocation == "cam2b":
#                         spr.bg.changeImg(random.choice(["cameras\\cam2b\\r", "cameras\\cam2b\\r-1"]))
#
#                     elif self.rabbitLocation != "cam2b":
#                         spr.bg.changeImg("cameras\\cam2b\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#                 elif self.lastcam == "cam3":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\scam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.rabbitLocation == "cam3":
#                         spr.bg.changeImg("cameras\\cam3\\r")
#
#                     elif self.rabbitLocation != "cam3":
#                         spr.bg.changeImg("cameras\\cam3\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#                 elif self.lastcam == "cam4a":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\scam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.chickenLocation == "cam4a":
#                         spr.bg.changeImg("cameras\\cam4a\\c")
#
#                     elif self.chickenLocation != "cam4a" and self.bearLocation == "cam4a":
#                         spr.bg.changeImg("cameras\\cam4a\\b")
#
#                     elif self.chickenLocation != "cam4a" and self.bearLocation != "cam4a":
#                         spr.bg.changeImg("cameras\\cam4a\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#                 elif self.lastcam == "cam4b":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\scam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.chickenLocation == "cam4b":
#                         spr.bg.changeImg("cameras\\cam4b\\c")
#
#                     elif self.chickenLocation != "cam4b" and self.bearLocation == "cam4b":
#                         spr.bg.changeImg("cameras\\cam4b\\b")
#
#                     elif self.chickenLocation != "cam4b" and self.bearLocation != "cam4b":
#                         spr.bg.changeImg("cameras\\cam4b\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#
#                 elif self.lastcam == "cam5":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\scam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     if self.rabbitLocation == "cam5":
#                         spr.bg.changeImg("cameras\\cam5\\r")
#
#                     elif self.rabbitLocation != "cam5":
#                         spr.bg.changeImg("cameras\\cam5\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#
#                 elif self.lastcam == "cam6":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\scam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\cam7")
#
#                     self.notStatic = False
#                     spr.bg.changeImg("cameras\\misc\\black")
#
#                 elif self.lastcam == "cam7":
#
#                     spr.camButtonOneA.changeImg("ui\\button\\cam1a")
#                     spr.camButtonOneB.changeImg("ui\\button\\cam1b")
#                     spr.camButtonOneC.changeImg("ui\\button\\cam1c")
#                     spr.camButtonTwoA.changeImg("ui\\button\\cam2a")
#                     spr.camButtonTwoB.changeImg("ui\\button\\cam2b")
#                     spr.camButtonThree.changeImg("ui\\button\\cam3")
#                     spr.camButtonFourA.changeImg("ui\\button\\cam4a")
#                     spr.camButtonFourB.changeImg("ui\\button\\cam4b")
#                     spr.camButtonFive.changeImg("ui\\button\\cam5")
#                     spr.camButtonSix.changeImg("ui\\button\\cam6")
#                     spr.camButtonSeven.changeImg("ui\\button\\scam7")
#
#                     if self.chickenLocation == "cam7" and self.bearLocation != "cam7":
#                         spr.bg.changeImg("cameras\\cam7\\c")
#
#                     elif self.chickenLocation != "cam7" and self.bearLocation == "cam7":
#                         spr.bg.changeImg("cameras\\cam7\\b")
#
#                     elif self.chickenLocation != "cam7" and self.bearLocation != "cam7":
#                         spr.bg.changeImg("cameras\\cam7\\0")
#
#                     else:
#                         self.notStatic = False
#                         spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
#                                                          "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
#                                                          "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
#                                                          "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))
#
#                 if spr.camButton.rect.collidepoint(Globals.pos) and not self.camButtonCooldown:
#                     self.camButtonCooldown = True
#                     self.changeScene("office")
#
#                 if not spr.camButton.rect.collidepoint(Globals.pos):
#                     self.camButtonCooldown = False
#
#                 if spr.bg.rect.topright[0] == 1280 and self.notStatic:
#                     self.camMovement = "right"
#
#                 if spr.bg.rect.topleft[0] == 0 and self.notStatic:
#                     self.camMovement = "left"
#
#                 if self.camMovement == "right" and self.notStatic:
#                     spr.bg.pos = (spr.bg.pos[0] + 5, spr.bg.pos[1])
#
#                 if self.camMovement == "left" and self.notStatic:
#                     spr.bg.pos = (spr.bg.pos[0] - 5, spr.bg.pos[1])
#
#                 if not self.notStatic:
#                     spr.bg.pos = (0,0)
#
#                 spr.camgroup.draw(self.screen)
#                 spr.camgroup.update()
#
#                 if self.time == 0:
#                     self.timeLabel = self.font.render("12 PM", True, (255,255,255))
#                     self.screen.blit(self.timeLabel, (1400,50))
#                 else:
#                     self.timeLabel = self.font.render("%s AM" % (self.time), True, (255,255,255))
#                     self.screen.blit(self.timeLabel, (1400,50))
#
#                 self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255,255,255))
#                 self.usageLabel = self.font.render("Usage: %s" %(self.usage), True, (255,255,255))
#
#                 self.screen.blit(self.powerLabel, (50,520))
#                 self.screen.blit(self.usageLabel, (50,550))
#                 self.screen.blit(self.font.render(Globals.camdic[self.lastcam], True, (255,255,255)), (832,292))
#
#             elif self.scene == "scarejump":
#
#                 if self.time >= 6:
#                     self.changeScene("6am")
#
#                 if self.powerDownStage == 4:
#                     if self.runAtSceneStart == 0:
#                         self.send("guard -> %s" % (self.scene))
#                         pygame.mixer.stop()
#                         spr.bearPowerdownScarejump.play()
#                         snd.channelNine.play(snd.xscream, 0)
#                         self.runAtSceneStart = 1
#
#                     spr.bearPowerdownScarejump.blit(self.screen, (0,0))
#
#                     if spr.bearPowerdownScarejump.isFinished():
#                         self.killed = True
#                         self.shutdown()
#
#                 for animatronic in self.animatronics:
#                     if animatronic.location == "inside" and self.power > 0:
#                         if self.runAtSceneStart == 0:
#                             self.send("guard -> %s" % (self.scene))
#                             snd.channelNine.play(snd.xscream, 0)
#                             spr.chickenScarejump.play()
#                             spr.rabbitScarejump.play()
#                             spr.bearNormalScarejump.play()
#                             spr.foxScarejump.play()
#                             self.runAtSceneStart = 1
#
#                         if animatronic.kind == "chicken":
#                             spr.chickenScarejump.blit(self.screen, (0,0))
#                             if spr.chickenScarejump.isFinished():
#                                 self.killed = True
#                                 self.send("guard -> dead")
#
#
#                         if animatronic.kind == "rabbit":
#                             spr.rabbitScarejump.blit(self.screen, (0,0))
#                             if spr.rabbitScarejump.isFinished():
#                                 self.killed = True
#                                 self.send("guard -> dead")
#
#
#                         if animatronic.kind == "bear":
#                             spr.bearNormalScarejump.blit(self.screen, (0,0))
#                             if spr.bearNormalScarejump.isFinished():
#                                 self.killed = True
#                                 self.send("guard -> dead")
#
#
#                         if animatronic.kind == "fox":
#                             spr.foxScarejump.blit(self.screen, (0,0))
#                             if spr.foxScarejump.isFinished():
#                                 self.killed = True
#                                 self.send("guard -> dead")
#
#             elif self.scene == "powerdown":
#
#                 spr.scaregroup.add(spr.bg)
#
#                 if self.time >= 6:
#                     self.changeScene("6am")
#
#
#                 self.movingleft = False
#                 self.movingright = False
#
#                 if self.mousex in range(0, 150) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
#                     spr.bg.pos = (spr.bg.pos[0] + 20, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] + 20, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] + 20, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] + 20, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] + 20, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] + 20, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] + 20, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] + 20, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] + 20, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingleft = True
#
#                 if self.mousex in range(150, 315) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
#                     spr.bg.pos = (spr.bg.pos[0] + 10, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] + 10, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] + 10, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] + 10, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] + 10, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] + 10, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] + 10, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] + 10, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] + 10, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingleft = True
#
#                 if self.mousex in range(315, 540) and spr.bg.rect.topleft[0] in range(-400, -10) and not self.movingright:
#                     spr.bg.pos = (spr.bg.pos[0] + 5, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] + 5, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] + 5, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] + 5, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] + 5, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] + 5, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] + 5, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] + 5, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] + 5, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingleft = True
#
#                 if self.mousex in range(1140, 1280) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
#                     spr.bg.pos = (spr.bg.pos[0] - 20, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] - 20, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] - 20, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] - 20, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] - 20, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] - 20, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] - 20, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] - 20, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] - 20, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingright = True
#
#                 if self.mousex in range(1000, 1140) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
#                     spr.bg.pos = (spr.bg.pos[0] - 10, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] - 10, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] - 10, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] - 10, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] - 10, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] - 10, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] - 10, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] - 10, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] - 10, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingright = True
#
#                 if self.mousex in range(750, 1000) and not spr.bg.rect.topright[0] < 1300 and not self.movingleft:
#                     spr.bg.pos = (spr.bg.pos[0] - 5, spr.bg.pos[1])
#
#                     spr.rightButton.pos = (spr.rightButton.pos[0] - 5, spr.rightButton.pos[1])
#                     spr.leftButton.pos = (spr.leftButton.pos[0] - 5, spr.leftButton.pos[1])
#
#                     spr.leftDoor.pos = (spr.leftDoor.pos[0] - 5, spr.leftDoor.pos[1])
#                     spr.rightDoor.pos = (spr.rightDoor.pos[0] - 5, spr.rightDoor.pos[1])
#
#                     spr.leftDoorButton.pos = (spr.leftDoorButton.pos[0] - 5, spr.leftDoorButton.pos[1])
#                     spr.leftLightButton.pos = (spr.leftLightButton.pos[0] - 5, spr.leftLightButton.pos[1])
#                     spr.rightDoorButton.pos = (spr.rightDoorButton.pos[0] - 5, spr.rightDoorButton.pos[1])
#                     spr.rightLightButton.pos = (spr.rightLightButton.pos[0] - 5, spr.rightLightButton.pos[1])
#
#                     if spr.officegroup.has(spr.leftDoor):
#                         spr.leftDoor.update()
#                     if spr.officegroup.has(spr.rightDoor):
#                         spr.rightDoor.update()
#
#                     self.movingright = True
#
#                 if self.runAtSceneStart == 0:
#                     self.send("guard -> %s" % (self.scene))
#                     pygame.mixer.stop()
#                     spr.bg.changeImg("office\\powerdown\\0")
#                     snd.channelOne.set_volume(1.0)
#                     snd.channelTwo.set_volume(0.5)
#
#                     if self.leftdoor:
#                         if not self.leftDoorReversed:
#                             spr.leftDoorAnim.reverse()
#                             self.leftDoorReversed = True
#                         spr.leftDoorAnim.play()
#                         snd.channelFour.play(snd.doorSound, 0)
#                         self.leftdoor = False
#
#                     if self.rightdoor:
#                         if not self.rightDoorReversed:
#                             spr.rightDoorAnim.reverse()
#                             self.rightDoorReversed = True
#                         spr.rightDoorAnim.play()
#                         snd.channelFour.play(snd.doorSound, 0)
#                         self.rightdoor = False
#
#                     snd.channelOne.play(snd.powerDown, loops=0)
#                     snd.channelOne.fadeout(random.randint(5000, 15000))
#
#                     snd.channelTwo.play(snd.ambienceTwo, loops=0)
#                     self.powerDownStage = 1
#                     self.runAtSceneStart = 1
#
#                 if not snd.channelOne.get_busy() and not snd.channelThirty.get_busy() and self.powerDownStage == 1:
#                     snd.channelThirty.set_volume(0.7, 0.3)
#                     snd.channelThirty.play(snd.musicBox, loops=0, maxtime=random.randint(3000, int(snd.musicBox.get_length() * 1000)))
#                     self.powerDownStage = 2
#
#                 if self.powerDownStage == 2:
#                     spr.bg.changeImg(random.choice(["office\\powerdown\\0", "office\\powerdown\\1", "office\\powerdown\\0", "office\\powerdown\\0"]))
#
#                 if not snd.channelThirty.get_busy() and self.powerDownStage == 2:
#                     self.powerDownStage = 3
#
#                 if self.powerDownStage == 3:
#                     spr.bg.changeImg("office\\powerdown\\2")
#                     self.oldTime = self.current_Milliseconds()
#                     self.powerDownStage += 1
#
#                 if self.current_Milliseconds() >= self.oldTime + 6000 and self.powerDownStage == 4:
#                     self.changeScene("scarejump")
#
#                 spr.scaregroup.update()
#                 spr.scaregroup.draw(self.screen)
#
#             elif self.scene == "6am":
#                 if self.runAtSceneStart == 1:
#                     self.send("guard -> %s" % (self.scene))
#                     pygame.mixer.stop()
#                     self.screen.fill((0,0,0))
#                     self.screen.blit(pygame.font.Font(None, 80).render("5 AM", True, (255,255,255)), (544,298))
#                     snd.channelOne.set_volume(1.0)
#                     snd.channelOne.play(snd.chimes, loops=0)
#                     self.oldTime = self.current_Milliseconds()
#                     self.runAtSceneStart = 2
#                 try:
#                     if self.current_Milliseconds() >= self.oldTime + 4500:#
#                         snd.channelTwo.play(snd.children, loops=0)
#                         self.screen.fill((0,0,0))
#                         self.screen.blit(pygame.font.Font(None, 80).render("6 AM", True, (255,255,255)), (544,298))
#                         del self.oldTime
#                 except:
#                     pass
#
#                 if not snd.channelOne.get_busy() and self.runAtSceneStart == 2:
#                     self.changeScene("end")
#
#             elif self.scene == "end":
#
#                 spr.scaregroup.add(spr.bg)
#
#                 if self.runAtSceneStart == 0:
#                     self.send("guard -> %s" % (self.scene))
#                     pygame.mixer.stop()
#                     snd.channelOne.set_volume(1.0)
#                     snd.channelOne.play(snd.musicBox, loops=-1)
#                     self.runAtSceneStart = 1
#
#                 if self.gmode == "normal":
#                     spr.bg.changeImg("ending\\normal")
#
#                 elif self.gmode == "overtime":
#                     spr.bg.changeImg("ending\\overtime")
#
#                 elif self.gmode == "custom":
#                     spr.bg.changeImg("ending\\custom")
#
#                 spr.scaregroup.update()
#                 spr.scaregroup.draw(self.screen)
#
#             if self.foxStatus == 3 and self.lastcam == "cam2a":
#                 self.foxStatus = 4
#
#             if self.foxStatus == 4 and not self.leftdoor:
#                 self.changeScene("office")
#                 self.foxStatus = 5
#
#             if self.scene == "office" and not self.leftlight and not self.rightlight and self.foxStatus != 5:
#                 snd.channelThree.set_volume(0.0)
#
#             if self.scene == "office" and self.leftlight:
#                 snd.channelThree.set_volume(0.7, 0.3)
#
#             if self.scene == "office" and self.rightlight:
#                 snd.channelThree.set_volume(0.3, 0.7)
#
#             if spr.leftDoorAnim.state == pyganim.STOPPED and self.leftdoor:
#                 spr.leftDoor.changeImg("office\\doors\\left\\15")
#
#             if spr.leftDoorAnim.state == pyganim.PLAYING:
#                 if not self.leftdoor:
#                     spr.leftDoor.changeImg("office\\doors\\left\\0")
#
#                 spr.leftDoorAnim.blit(self.screen, tuple(spr.leftDoor.pos))
#                 self.screen.blit(self.powerLabel, (50,520))
#                 self.screen.blit(self.usageLabel, (50,550))
#                 self.screen.blit(spr.camButton.image, tuple(spr.camButton.pos))
#
#             if spr.rightDoorAnim.state == pyganim.STOPPED and self.rightdoor:
#                 spr.rightDoor.changeImg("office\\doors\\right\\15")
#
#             if spr.rightDoorAnim.state == pyganim.PLAYING:
#                 if not self.rightdoor:
#                     spr.rightDoor.changeImg("office\\doors\\right\\0")
#
#                 spr.rightDoorAnim.blit(self.screen, tuple(spr.rightDoor.pos))
#                 self.screen.blit(self.powerLabel, (50,520))
#                 self.screen.blit(self.usageLabel, (50,550))
#                 self.screen.blit(self.timeLabel, (1400,50))
#
#             if spr.cameraAnim.state == pyganim.PLAYING:
#                 spr.cameraAnim.blit(self.screen, (0,0))
#
#             if spr.cameraAnim.state == pyganim.STOPPED and not self.cameraAnimReversed:
#                 self.scene = "cam"
#
#             self.screen.blit(self.font.render("%s FPS" % round(self.FPSCLOCK.get_fps()), True, (0,255,0)), (10,10))
#             self.screen.blit(self.font.render("(%s X, %s Y)" % (self.mousex, self.mousey), True, (0,255,0)), (10,40))
#
#             pygame.display.flip()
#
#             self.FPSCLOCK.tick(self.fps)
#
#     def shutdown(self):
#         utils.debugprint("Shutting down...")
#         pygame.quit()
#         del self
#         sys.exit(0)
#         os._exit(0)
#         os.system("exit")
#
#     def changeCamera(self, camera):
#         snd.channelNine.play(snd.blip, 0)
#         spr.camgroup.draw(self.screen)
#         spr.camgroup.update()
#         if camera == "cam2a" and self.foxStatus == 3:
#             self.foxStatus = 4
#
#         self.lastcam = camera
#         self.send("guard -> %s" % (self.lastcam))
#
#     def leftDoor(self):
#         if not self.leftdoor:
#             if self.leftDoorReversed:
#                 spr.leftDoorAnim.reverse()
#                 self.leftDoorReversed = False
#             spr.leftDoorAnim.play()
#             snd.channelFour.play(snd.doorSound, 0)
#             self.leftdoor = True
#             self.send("guard -> leftdoor true")
#             self.usage += 1
#             return None
#
#         if self.leftdoor:
#             if not self.leftDoorReversed:
#                 spr.leftDoorAnim.reverse()
#                 self.leftDoorReversed = True
#             spr.leftDoorAnim.play()
#             snd.channelFour.play(snd.doorSound, 0)
#             self.leftdoor = False
#             self.send("guard -> leftdoor false")
#             self.usage -= 1
#             return None
#
#     def leftLight(self):
#         if self.leftlight:
#             self.leftlight = False
#             self.send("guard -> leftlight false")
#             self.usage -= 1
#             return None
#
#         if not self.leftlight:
#
#             for animatronic in self.animatronics:
#                 if animatronic == "leftdoor":
#                     snd.channelNine.play(snd.windowScare, 0)
#
#             self.leftlight = True
#             self.send("guard -> leftlight true")
#
#             if self.rightlight:
#                 self.rightlight = False
#                 self.send("guard -> rightlight false")
#                 self.usage -= 1
#             self.usage += 1
#             return None
#
#     def rightDoor(self):
#         if not self.rightdoor:
#             if self.rightDoorReversed:
#                 spr.rightDoorAnim.reverse()
#                 self.rightDoorReversed = False
#             spr.rightDoorAnim.play()
#             snd.channelFour.play(snd.doorSound, 0)
#             self.rightdoor = True
#             self.send("guard -> rightdoor true")
#             self.usage += 1
#             return None
#
#         if self.rightdoor:
#             if not self.rightDoorReversed:
#                 spr.rightDoorAnim.reverse()
#                 self.rightDoorReversed = True
#             spr.rightDoorAnim.play()
#             snd.channelFour.play(snd.doorSound, 0)
#             self.rightdoor = False
#             self.send("guard -> rightdoor false")
#             self.usage -= 1
#             return None
#
#     def rightLight(self):
#         if self.rightlight:
#             self.rightlight = False
#             self.send("guard -> rightlight false")
#             self.usage -= 1
#             return None
#
#         if not self.rightlight:
#             if self.chickenLocation == "rightdoor":
#                 snd.channelNine.play(snd.windowScare, 0)
#
#             self.rightlight = True
#             self.send("guard -> rightlight true")
#
#             if self.leftlight == True:
#                 self.leftlight = False
#                 self.send("guard -> leftlight false")
#                 self.usage -= 1
#
#             self.usage += 1
#             return None
#
#     def changeScene(self, scene):
#         if scene == "office":
#             if not self.cameraAnimReversed:
#                 spr.cameraAnim.reverse()
#                 self.cameraAnimReversed = True
#
#             spr.cameraAnim.play()
#
#             self.usage -= 1
#             snd.putDown.play(0)
#             self.scene = "office"
#             for animatronic in self.animatronics:
#                 if animatronic == "inside":
#                     self.scene = "scarejump"
#
#         elif scene == "cam":
#             if self.cameraAnimReversed:
#                 spr.cameraAnim.reverse()
#                 self.cameraAnimReversed = False
#
#             spr.cameraAnim.play()
#             self.usage += 1
#
#             if self.leftlight:
#                 self.usage -= 1
#                 self.leftlight = False
#             if self.rightlight:
#                 self.usage -= 1
#                 self.rightlight = False
#
#             snd.putDown.play(0)
#             # Scene changes at 1170
#
#         elif scene == "powerdown":
#             self.scene = "powerdown"
#
#         elif scene == "scarejump":
#             self.scene = "scarejump"
#
#         elif scene == "dead":
#             self.scene = "dead"
#
#         elif scene == "6am":
#             self.scene = "6am"
#
#         elif scene == "end":
#             self.scene = "end"
#
#         self.runAtSceneStart = 0
#         self.oldtime = 0
#
#         utils.debugprint("Changed scene to %s" % self.scene)
#
#
#     def send(self, text):
#         self.sock.send(bytes(text, "utf-8"))
#
#     def receiveData(self):
#         self.received = str(self.sock.recv(1024), "utf-8")
#
#         if self.received == "server -> power - 1":
#             self.power -= 1
#
#         if self.received == "time -> 0":
#             self.time = 0
#
#         if self.received == "time -> 1":
#             self.time = 1
#
#         if self.received == "time -> 2":
#             self.time = 2
#
#         if self.received == "time -> 3":
#             self.time = 3
#
#         if self.received == "time -> 4":
#             self.time = 4
#
#         if self.received == "time -> 5":
#             self.time = 5
#
#         if self.received == "time -> 6":
#             self.time = 6
#
#         if self.received == "chicken -> cam1b":
#             self.chickenLocation = "cam1b"
#
#         if self.received == "chicken -> cam4a":
#             self.chickenLocation = "cam4a"
#
#         if self.received == "chicken -> cam4b":
#             self.chickenLocation = "cam4b"
#
#         if self.received == "chicken -> cam6":
#             self.chickenLocation = "cam6"
#
#         if self.received == "chicken -> cam7":
#             self.chickenLocation = "cam7"
#
#         if self.received == "chicken -> rightdoor":
#             self.chickenLocation = "rightdoor"
#
#         if self.received == "chicken -> inside":
#             self.chickenLocation = "inside"
#
#
#
#         print(self.received)
#         self.receiveData()
#
#     def current_Milliseconds(self): return int(round(time.time() * 1000))
# if __name__ == "__main__":
#     try:
#         raise Warning
#     except Warning:
#         print("You must execute game.py")
