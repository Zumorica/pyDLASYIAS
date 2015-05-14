#!/usr/bin/env python
import sys
import os
import time
import random
import _thread
import threading
import pygame
import socket
import lightning
import pyDLASYIAS.sprite as sprite
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.spr as spr
import pyDLASYIAS.snd as snd
import pyDLASYIAS.utils.functions as utils
import pyDLASYIAS.utils.inputbox as inputbox
import pyDLASYIAS.pyganim as pyganim
import pyDLASYIAS.multiplayer.common as common
from pygame.locals import *

class chickenMain():
    def __init__(self, socket, width=1280, height=720, fps=59):

        Globals.main = self
        self.power = 100
        self.time = 0
        self.usage = 1
        self.scene = "cam"
        self.location = "cam1a"
        self.width = width
        self.height = height
        self.running = True
        self.fps = fps
        self.FPSCLOCK = pygame.time.Clock()
        self.mousex = 0
        self.mousey = 0
        self.runAtSceneStart = 0
        self.runonce = 0
        self.oldTime = 0
        self.staticTime = 0
        self.camMovement = "left"
        self.powerDownStage = 0
        self.alphaStatic = True
        self.static = False
        self.fullscreen = False
        self.rabbit = common.Animatronic("Rabbit", "rabbit")
        self.chicken = common.Animatronic("Chicken", "chicken")
        self.fox = common.Animatronic("Fox", "fox")
        self.bear = common.Animatronic("Bear", "bear")
        self.guard = common.Guard("Guard")
        self.cooldown = 1500
        self.cooldownSpeed = 4
        self.socket = socket
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        thread = threading.Thread(target=self.update)
        thread.setDaemon(True)
        self.main_loop()

    def handle_events(self):
        for event in pygame.event.get():

            # utils.debugprint(event, writetolog=False)

            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                self.shutdown()
                return False

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

        return True

    def main_loop(self):
        '''Main game loop.'''

        spr.cameraAnim.state = pyganim.PAUSED
        pygame.init()

        while self.running:

            Globals.mouseClick = False
            Globals.pos = self.mousex, self.mousey
            pygame.display.set_caption("--pyDLASYIAS %s-- -%s FPS-" %(Globals.version, round(self.FPSCLOCK.get_fps())))

            self.cooldownSpeed = 4

            if self.guard.scene == "cam":
                self.cooldownSpeed = 2

            if self.guard.lastcam == self.location:
                self.cooldownSpeed = 1

            if self.cooldown:
                self.cooldown -= self.cooldownSpeed

            if self.handle_events():

                if self.scene == "cam":

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
                        pass

                    if self.runAtSceneStart == 0 and not self.power < 0:
                        spr.bg.pos = [0, 0]
                        snd.channelSeven.play(snd.cameraSoundTwo, -1)
                        snd.channelTen.play(random.choice([snd.garble, snd.garbleTwo, snd.garbleThree]), -1)
                        snd.channelSeven.set_volume(1.0)
                        snd.channelOne.set_volume(0.03, 0.07)
                        self.changeCamera(self.location)
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


                    if spr.camButtonOneA.rect.collidepoint(Globals.pos) and Globals.mouseClick and not self.cooldown:
                        self.changeCamera("cam1a")

                    if spr.camButtonOneB.rect.collidepoint(Globals.pos) and Globals.mouseClick and not self.cooldown:
                        self.changeCamera("cam1b")

                    if spr.camButtonFourA.rect.collidepoint(Globals.pos) and Globals.mouseClick and not self.cooldown:
                        self.changeCamera("cam4a")

                    if spr.camButtonFourB.rect.collidepoint(Globals.pos) and Globals.mouseClick and not self.cooldown:
                        self.changeCamera("cam4b")

                    if spr.camButtonSix.rect.collidepoint(Globals.pos) and Globals.mouseClick and not self.cooldown:
                        self.changeCamera("cam6")

                    if spr.camButtonSeven.rect.collidepoint(Globals.pos) and Globals.mouseClick and not self.cooldown:
                        self.changeCamera("cam7")

                    if self.location == "cam1a":

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

                    elif self.location == "cam1b":

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

                    elif self.location == "cam4a":

                        if self.chicken.location == "cam4a":
                            spr.bg.changeImg("cameras\\cam4a\\c")

                        elif self.chicken.location != "cam4a" and self.bear.location == "cam4a":
                            spr.bg.changeImg("cameras\\cam4a\\b")

                        elif self.chicken.location != "cam4a" and self.bear.location != "cam4a":
                            spr.bg.changeImg("cameras\\cam4a\\0")

                        else:
                            self.alphaStatic = False
                            self.static = True

                    elif self.location == "cam4b":

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

                    elif self.location == "cam6":

                        spr.bg.pos = [0,0]
                        self.alphaStatic = False
                        self.static = False

                        if self.chicken.location == "cam6":
                            snd.channelEleven.queue(random.choice([snd.pots, snd.potsTwo, snd.potsThree, snd.potsFour]))

                        if self.bear.location == "cam6":
                            snd.channelEleven.queue(snd.musicBox)

                        snd.channelEleven.set_volume(random.uniform(0.6, 0.8))

                        spr.bg.changeImg("cameras\\misc\\black")

                    elif self.location == "cam7":

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
                        if animatronic.location == self.location:
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
                        self.timeLabel = lightning.text.Text("12 PM", (255,255,255), 1040, 60, 32)
                    else:
                        self.timeLabel = lightning.text.Text("%s AM" %(self.time), (255,255,255), 1040, 60, 32)

                    self.coolLabel = lightning.text.Text("Your cooldown: %s" %(self.cooldown), (255,255,255), 50, 490, 32)
                    self.powerLabel = lightning.text.Text("Guard's Power: %s" %(self.power), (255,255,255), 50, 520, 32)
                    self.usageLabel = lightning.text.Text("Guard's Usage: %s" %(self.usage), (255,255,255), 50, 550, 32)

                    self.coolLabel.draw(self.screen)
                    self.powerLabel.draw(self.screen)
                    self.usageLabel.draw(self.screen)
                    self.timeLabel.draw(self.screen)
                    lightning.text.Text(Globals.camdic[self.location], (255,255,255), 832, 292, 32).draw(self.screen)

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

                    pass

                self.chicken.location = self.location

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

        if camera == "cam4b":
            spr.camButtonFourB.changeImg("ui\\button\\scam4b")
        else:
            spr.camButtonFourB.changeImg("ui\\button\\cam4b")

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

        self.location = camera
        self.sendData()

    def changeScene(self, scene):

        if scene == "cam":
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

        self.sendData()

    def current_Milliseconds(self): return int(round(time.time() * 1000))

    def sendData(self):
        try:
            self.socket.sendall(self.chicken.get_pickled())
        except OSError:
            print("Send failed!")
            raise

    def update(self):
        data = self.socket.recv(1024)
        obj = pickle.loads(data)

        if obj.type == "Animatronic":

            if obj.kind == "rabbit":
                self.rabbit = obj

            if obj.kind == "bear":
                self.bear = obj

            if obj.kind == "fox":
                self.fox = obj

        if obj.type == "Guard":
            self.guard = obj

        if obj.type == "Event":
            self.time = obj.time
            self.power = obj.power

        self.update()

if __name__ == "__main__":
    try:
        raise Warning
    except Warning:
        print("You must execute game.py")
