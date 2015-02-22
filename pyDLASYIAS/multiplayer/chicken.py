#!/usr/bin/env python
import sys
import os
import time
import random
import _thread
import threading
import pygame
import socket
import pyDLASYIAS.sprite as sprite
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.spr as spr
import pyDLASYIAS.snd as snd
import pyDLASYIAS.utils.functions as utils
import pyDLASYIAS.pyganim as pyganim
from pygame.locals import *

class chickenMain():
    def __init__(self, host="localhost", port=1987, fps=40, width=1280, height=720):

        sys.setrecursionlimit(5000)
        threading.stack_size(128*4096)

        self.location = "cam1a"
        self.scene = "cam"

        self.rabbitLocation = "cam1a"
        self.bearLocation = "cam1a"
        self.foxStatus = 0

        self.time = 0
        self.power = 100

        # Server IP adress and port.
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((self.host, self.port))
        self.sock.sendall(bytes("chicken\n", "utf-8"))

        self.received = str(self.sock.recv(1024), "utf-8")

        self.width = width
        self.height = height
        self.running = True
        self.fps = fps

        self.beingWatched = False

        self.cooldown = random.randint(500, 900)

        threading.Thread(target=self.receiveData, args=()).start()

        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption("--pyDLASYIAS %s--" %(Globals.version))

        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()

        self.font = pygame.font.Font(None, 30)

        self.mousex = 0
        self.mousey = 0

        self.runAtSceneStart = 0
        self.runonce = 0

        self.oldTime = 0

        self.camMovement = "left"

        self.bearLocation = "cam1a"
        self.rabbitLocation = "cam1a"
        self.foxStatus = 0
        self.guardLocation = "office"

        self.leftdoor = False
        self.rightdoor = False
        self.leftlight = False
        self.rightlight = False

        self.animatronics = [self.bearLocation, self.rabbitLocation]

        while self.running:

            if self.cooldown != 0:
                self.cooldown -= 1

            Globals.mouseClick = False
            Globals.pos = self.mousex, self.mousey

            for event in pygame.event.get():

                #utils.debugprint(event, writetolog=False)

                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()

                elif event.type == KEYUP and event.key == K_SPACE:
                    self.cooldown = 0

                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos

                elif event.type == MOUSEBUTTONUP:
                    self.mousex, self.mousey = event.pos
                    Globals.mouseClick = True

            if self.scene == "cam":
                self.notStatic = True

                if self.runAtSceneStart == 0 and not self.power < 0:
                    spr.bg.pos = (0,0)
                    self.changeCamera(self.location)
                    snd.channelSeven.play(snd.cameraSoundTwo, -1)
                    self.runAtSceneStart = 1

                    spr.camgroup.add(spr.mapAnim)
                    spr.camgroup.add(spr.camButtonOneA)
                    spr.camgroup.add(spr.camButtonOneB)
                    spr.camgroup.add(spr.camButtonFourA)
                    spr.camgroup.add(spr.camButtonFourB)
                    spr.camgroup.add(spr.camButtonSix)
                    spr.camgroup.add(spr.camButtonSeven)
                    spr.camgroup.add(spr.staticTransparent)
                    spr.camgroup.add(spr.bg)

                    if self.location == "cam4b":
                        spr.camgroup.add(spr.camButtonRight)

                    spr.camgroup.change_layer(spr.bg, 0)
                    spr.camgroup.change_layer(spr.mapAnim, 8)
                    spr.camgroup.change_layer(spr.camButtonOneA, 10)
                    spr.camgroup.change_layer(spr.camButtonOneB, 10)
                    spr.camgroup.change_layer(spr.camButtonFourA, 10)
                    spr.camgroup.change_layer(spr.camButtonFourB, 10)
                    spr.camgroup.change_layer(spr.camButtonSix, 10)
                    spr.camgroup.change_layer(spr.camButtonSeven, 10)
                    spr.camgroup.change_layer(spr.staticTransparent, 2)
                    if spr.camgroup.has(spr.camButtonRight):
                        spr.camgroup.change_layer(spr.camButtonRight, 10)



                spr.staticTransparent.changeImg(random.choice(["cameras\\misc\\static\\transparent\\0", "cameras\\misc\\static\\transparent\\1",
                                                               "cameras\\misc\\static\\transparent\\2", "cameras\\misc\\static\\transparent\\3",
                                                               "cameras\\misc\\static\\transparent\\4", "cameras\\misc\\static\\transparent\\5",
                                                               "cameras\\misc\\static\\transparent\\6", "cameras\\misc\\static\\transparent\\7"]))

                if spr.camButtonOneB.rect.collidepoint(Globals.pos) and Globals.mouseClick and self.cooldown == 0 and self.location != "cam1b" and not self.beingWatched and self.location in ["cam1a", "cam7", "cam6"]:
                    self.changeCamera("cam1b")
                    self.cooldown = random.randint(300, 550)

                if spr.camButtonFourA.rect.collidepoint(Globals.pos) and Globals.mouseClick and self.cooldown == 0 and self.location != "cam4a" and not self.beingWatched and self.location in ["cam6", "cam7"]:
                    self.changeCamera("cam4a")
                    self.cooldown = random.randint(400, 700)

                if spr.camButtonFourB.rect.collidepoint(Globals.pos) and Globals.mouseClick and self.cooldown == 0 and self.location != "cam4b" and not self.beingWatched and self.location in ["cam4a"]:
                    self.changeCamera("cam4b")
                    self.cooldown = random.randint(450, 600)

                if spr.camButtonSix.rect.collidepoint(Globals.pos) and Globals.mouseClick and self.cooldown == 0 and self.location != "cam6" and not self.beingWatched and self.location in ["cam1b", "cam7"]:
                    self.changeCamera("cam6")
                    self.cooldown = random.randint(200, 400)

                if spr.camButtonSeven.rect.collidepoint(Globals.pos) and Globals.mouseClick and self.cooldown == 0 and self.location != "cam7" and not self.beingWatched and self.location in ["cam1b", "cam6"]:
                    self.changeCamera("cam7")
                    self.cooldown = random.randint(400, 500)

                if self.location == "cam1a":

                    spr.camButtonOneA.changeImg("ui\\button\\scam1a")
                    spr.camButtonOneB.changeImg("ui\\button\\cam1b")
                    spr.camButtonFourA.changeImg("ui\\button\\cam4a")
                    spr.camButtonFourB.changeImg("ui\\button\\cam4b")
                    spr.camButtonSix.changeImg("ui\\button\\cam6")
                    spr.camButtonSeven.changeImg("ui\\button\\cam7")

                    if self.rabbitLocation == "cam1a" and self.location == "cam1a" and self.bearLocation == "cam1a":
                        spr.bg.changeImg("cameras\\cam1a\\brc")

                    elif self.rabbitLocation != "cam1a" and self.location == "cam1a" and self.bearLocation == "cam1a":
                        spr.bg.changeImg("cameras\\cam1a\\bc")

                    else:
                        self.notStatic = False
                        spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))


                elif self.location == "cam1b":

                    spr.camButtonOneA.changeImg("ui\\button\\cam1a")
                    spr.camButtonOneB.changeImg("ui\\button\\scam1b")
                    spr.camButtonFourA.changeImg("ui\\button\\cam4a")
                    spr.camButtonFourB.changeImg("ui\\button\\cam4b")
                    spr.camButtonSix.changeImg("ui\\button\\cam6")
                    spr.camButtonSeven.changeImg("ui\\button\\cam7")

                    if self.rabbitLocation == "cam1b" and self.location == "cam1b":
                        spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",  "cameras\\misc\\static\\2", "cameras\\misc\\static\\3", "cameras\\misc\\static\\4", "cameras\\misc\\static\\5", "cameras\\misc\\static\\6"]))

                    elif self.rabbitLocation != "cam1b" and self.location == "cam1b":
                        spr.bg.changeImg("cameras\\cam1b\\c")

                    else:
                        self.notStatic = False
                        spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

                elif self.location == "cam4a":

                    spr.camButtonOneA.changeImg("ui\\button\\cam1a")
                    spr.camButtonOneB.changeImg("ui\\button\\cam1b")
                    spr.camButtonFourA.changeImg("ui\\button\\scam4a")
                    spr.camButtonFourB.changeImg("ui\\button\\cam4b")
                    spr.camButtonSix.changeImg("ui\\button\\cam6")
                    spr.camButtonSeven.changeImg("ui\\button\\cam7")

                    if self.location == "cam4a":
                        spr.bg.changeImg("cameras\\cam4a\\c")

                    else:
                        self.notStatic = False
                        spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

                elif self.location == "cam4b":

                    spr.camButtonOneA.changeImg("ui\\button\\cam1a")
                    spr.camButtonOneB.changeImg("ui\\button\\cam1b")
                    spr.camButtonFourA.changeImg("ui\\button\\cam4a")
                    spr.camButtonFourB.changeImg("ui\\button\\scam4b")
                    spr.camButtonSix.changeImg("ui\\button\\cam6")
                    spr.camButtonSeven.changeImg("ui\\button\\cam7")

                    if self.location == "cam4b":
                        spr.bg.changeImg("cameras\\cam4b\\c")

                    else:
                        self.notStatic = False
                        spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

                elif self.location == "cam6":

                    spr.camButtonOneA.changeImg("ui\\button\\cam1a")
                    spr.camButtonOneB.changeImg("ui\\button\\cam1b")
                    spr.camButtonFourA.changeImg("ui\\button\\cam4a")
                    spr.camButtonFourB.changeImg("ui\\button\\cam4b")
                    spr.camButtonSix.changeImg("ui\\button\\scam6")
                    spr.camButtonSeven.changeImg("ui\\button\\cam7")

                    self.notStatic = False
                    spr.bg.changeImg("cameras\\misc\\black")

                elif self.location == "cam7":

                    spr.camButtonOneA.changeImg("ui\\button\\cam1a")
                    spr.camButtonOneB.changeImg("ui\\button\\cam1b")
                    spr.camButtonFourA.changeImg("ui\\button\\cam4a")
                    spr.camButtonFourB.changeImg("ui\\button\\cam4b")
                    spr.camButtonSix.changeImg("ui\\button\\cam6")
                    spr.camButtonSeven.changeImg("ui\\button\\scam7")

                    if self.location == "cam7" and self.bearLocation != "cam7":
                        spr.bg.changeImg("cameras\\cam7\\c")

                    else:
                        self.notStatic = False
                        spr.bg.changeImg(random.choice(["cameras\\misc\\static\\0", "cameras\\misc\\static\\1",
                                                         "cameras\\misc\\static\\2", "cameras\\misc\\static\\3",
                                                         "cameras\\misc\\static\\4", "cameras\\misc\\static\\5",
                                                         "cameras\\misc\\static\\6", "cameras\\misc\\static\\7"]))

                if spr.bg.rect.topright[0] == 1280 and self.notStatic:
                    self.camMovement = "right"

                if spr.bg.rect.topleft[0] == 0 and self.notStatic:
                    self.camMovement = "left"

                if self.camMovement == "right" and self.notStatic:
                    spr.bg.pos = (spr.bg.pos[0] + 5, spr.bg.pos[1])

                if self.camMovement == "left" and self.notStatic:
                    spr.bg.pos = (spr.bg.pos[0] - 5, spr.bg.pos[1])

                if not self.notStatic:
                    spr.bg.pos = (0,0)

                for animatronic in Globals.animatronics:
                    if animatronic.location == self.location:
                        animatronic.beingWatched = True

                    else:
                        animatronic.beingWatched = False


                spr.camgroup.draw(self.screen)
                spr.camgroup.update()

            if self.time == 0:
                self.timeLabel = self.font.render("12 PM", True, (255,255,255))
                self.screen.blit(self.timeLabel, (1400,50))
            else:
                self.timeLabel = self.font.render("%s AM" % (self.time), True, (255,255,255))
                self.screen.blit(self.timeLabel, (1400,50))

            self.powerLabel = self.font.render("Power left: %s" %(self.power), True, (255,255,255))
            self.cooldownLabel = self.font.render("Cooldown: %s" %(self.cooldown), True, (255,255,255))

            self.screen.blit(self.powerLabel, (50,520))
            self.screen.blit(self.cooldownLabel, (50,550))
            self.screen.blit(self.font.render(Globals.camdic[self.location], True, (255,255,255)), (832,292))

            self.screen.blit(self.font.render("%s FPS" % round(self.FPSCLOCK.get_fps()), True, (0,255,0)), (10,10))
            self.screen.blit(self.font.render("(%s X, %s Y)" % (self.mousex, self.mousey), True, (0,255,0)), (10,40))

            pygame.display.flip()
            pygame.display.update()


    def changeCamera(self, camera):
        snd.channelNine.play(snd.blip, 0)
        spr.camgroup.draw(self.screen)
        spr.camgroup.update()
        self.location = camera
        self.send("chicken -> %s" % (self.location))

    def current_Milliseconds(self): return int(round(time.time() * 1000))

    def send(self, text):
        self.sock.send(bytes(text, "utf-8"))

    def receiveData(self):
        self.received = str(self.sock.recv(1024), "utf-8")
        print(self.received)


        if self.received == "server -> power - 1":
            self.power -= 1

        if self.received == "time -> 0":
            self.time = 0

        if self.received == "time -> 1":
            self.time = 1

        if self.received == "time -> 2":
            self.time = 2

        if self.received == "time -> 3":
            self.time = 3

        if self.received == "time -> 4":
            self.time = 4

        if self.received == "time -> 5":
            self.time = 5

        if self.received == "time -> 6":
            self.time = 6


        if self.received == "guard -> cam1a":
            self.guardLocation = "cam1a"

        if self.received == "guard -> cam1b":
            self.guardLocation = "cam1b"

        if self.received == "guard -> cam1c":
            self.guardLocation = "cam1c"

        if self.received == "guard -> cam2a":
            self.guardLocation = "cam2a"

        if self.received == "guard -> cam2b":
            self.guardLocation = "cam2b"

        if self.received == "guard -> cam3":
            self.guardLocation = "cam3"

        if self.received == "guard -> cam4a":
            self.guardLocation = "cam4a"

        if self.received == "guard -> cam4b":
            self.guardLocation = "cam4b"

        if self.received == "guard -> cam5":
            self.guardLocation = "cam5"

        if self.received == "guard -> cam6":
            self.guardLocation = "cam6"

        if self.received == "guard -> cam7":
            self.guardLocation = "cam7"

        if self.received == "guard -> office":
            self.guardLocation = "office"

        if self.received == "guard -> cam":
            self.guardLocation = "cam"

        if self.received == "guard -> leftdoor true":
            self.leftdoor = True

        if self.received == "guard -> leftdoor false":
            self.leftdoor = False

        if self.received == "guard -> rightdoor true":
            self.rightdoor = True

        if self.received == "guard -> rightdoor false":
            self.rightdoor = False

        if self.received == "guard -> leftlight false":
            self.leftlight = False

        if self.received == "guard -> leftlight true":
            self.leftlight = True
            if self.rightlight:
                self.rightlight = False

        if self.received == "guard -> rightlight false":
            self.rightlight = False

        if self.received == "guard -> rightlight true":
            self.rightlight = True
            if self.leftlight:
                self.leftlight = False

        self.receiveData()
