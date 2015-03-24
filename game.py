#!/usr/bin/env python
import sys
import os
import time
import random
import socket
import threading
import pygame
from pygame.locals import *
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.animatronics as animatronics
import pyDLASYIAS.sprite as sprite
import pyDLASYIAS.main as main
import pyDLASYIAS.utils.functions as utils
import pyDLASYIAS.utils.inputbox as inputbox
import pyDLASYIAS.pyganim as pyganim
try:
    import pyDLASYIAS.multiplayer as multiplayer
except ImportError:
    print("Could not load multiplayer module!")

def launcher():
    running = True
    screen = pygame.display.set_mode((1280, 720), 0, 32)
    FPSCLOCK = pygame.time.Clock()

    scene = "intro"

    pygame.init()

    font = pygame.font.Font(None, 50)
    group = pygame.sprite.Group()
    customgroup = pygame.sprite.Group()
    multigroup = pygame.sprite.Group()

    mousex = 0
    mousey = 0

    time = 0

    title = sprite.Sprite(startpos=(0,0), image="menu\\title")
    title.groups = group

    customNightButton = sprite.Sprite(startpos=(122,560), image="menu\\custom-0")
    customNightButton.groups = group

    multiplayerButton = sprite.Sprite(startpos=(122,500), image="menu\\multiplayer-0")
    multiplayerButton.groups = group

    timeleft = sprite.Sprite(startpos=(122, 560), image="custom\\buttons\\0")
    timeleft.groups = group

    timeright = sprite.Sprite(
        startpos=(311, 560), image="custom\\buttons\\1")
    timeright.groups = group

    power = 100
    powerleft = sprite.Sprite(
        startpos=(406, 560), image="custom\\buttons\\0")
    powerleft.groups = group

    powerright = sprite.Sprite(
        startpos=(593, 560), image="custom\\buttons\\1")
    powerright.groups = group

    ready = sprite.Sprite(startpos=(1044, 603), image="custom\\buttons\\2")
    ready.groups = group

    bearspr = sprite.Sprite(
        startpos=(118, 187), image="custom\\animatronics\\b")
    bearspr.groups = group

    bearai = 0

    bearleft = sprite.Sprite(startpos=(122, 470), image="custom\\buttons\\0")
    bearleft.groups = group

    bearright = sprite.Sprite(
        startpos=(311, 470), image="custom\\buttons\\1")
    bearright.groups = group

    rabbitspr = sprite.Sprite(
        startpos=(403, 187), image="custom\\animatronics\\r")
    rabbitspr.groups = group

    rabbitai = 0

    rabbitleft = sprite.Sprite(
        startpos=(406, 470), image="custom\\buttons\\0")
    rabbitleft.groups = group

    rabbitright = sprite.Sprite(
        startpos=(593, 470), image="custom\\buttons\\1")
    rabbitright.groups = group

    chickenspr = sprite.Sprite(
        startpos=(682, 187), image="custom\\animatronics\\c")
    chickenspr.groups = group

    chickenai = 0

    chickenleft = sprite.Sprite(
        startpos=(690, 470), image="custom\\buttons\\0")
    chickenleft.groups = group

    chickenright = sprite.Sprite(
        startpos=(876, 470), image="custom\\buttons\\1")
    chickenright.groups = group

    foxspr = sprite.Sprite(
        startpos=(957, 187), image="custom\\animatronics\\f")
    foxspr.groups = group

    foxai = 0

    foxleft = sprite.Sprite(startpos=(969, 470), image="custom\\buttons\\0")
    foxleft.groups = group

    foxright = sprite.Sprite(
        startpos=(1154, 470), image="custom\\buttons\\1")
    foxright.groups = group

    intro = pyganim.PygAnimation([("images\\intro\\newspaper-0.png", 1), ("images\\intro\\static-0.png", 0.05),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\newspaper-0.png", 0.35),
                                  ("images\\intro\\static-2.png", 0.05), ("images\\intro\\static-3.png", 0.05),
                                  ("images\\intro\\b-1.png", 0.35), ("images\\intro\\static-6.png", 0.05),
                                  ("images\\intro\\itsme-0.png", 0.05), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\itsme-1.png", 0.05), ("images\\intro\\b-0.png", 0.50),
                                  ("images\\intro\\static-6.png", 0.05), ("images\\intro\\static-1.png", 0.05),
                                  ("images\\intro\\crying-0.png", 0.10), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\stage-0.png", 0.15), ("images\\intro\\static-3.png", 0.05),
                                  ("images\\intro\\static-6.png", 0.05), ("images\\intro\\stage-0.png", 0.05),
                                  ("images\\intro\\static-0.png", 0.05), ("images\\intro\\static-2.png", 0.05),
                                  ("images\\intro\\r-0.png", 0.15), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\static-6.png", 0.05), ("images\\intro\\r-0.png", 0.07),
                                  ("images\\intro\\r-1.png", 0.04), ("images\\intro\\static-2.png", 0.05),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\static-3.png", 0.05),
                                  ("images\\intro\\static-2.png", 0.05), ("images\\intro\\static-0.png", 0.05),
                                  ("images\\intro\\static-7.png", 0.05), ("images\\intro\\static-5.png", 0.05),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\static-2.png", 0.05),
                                  ("images\\intro\\static-3.png", 0.05), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\static-5.png", 0.05), ("images\\intro\\newspaper-1.png", 0.10),
                                  ("images\\intro\\static-2.png", 0.05), ("images\\intro\\newspaper-2.png", 0.10),
                                  ("images\\intro\\static-4.png", 0.05), ("images\\intro\\newspaper-3.png", 0.10),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\c-0.png", 0.15),
                                  ("images\\intro\\static-7.png", 0.05), ("images\\intro\\static-1.png", 0.05),
                                  ("images\\intro\\itsme-1.png", 0.05), ("images\\intro\\itsme-0.png", 0.05),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\static-2.png", 0.05),
                                  ("images\\intro\\static-3.png", 0.05), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\static-5.png", 0.05), ("images\\intro\\static-6.png", 0.05),
                                  ("images\\intro\\static-7.png", 0.05), ("images\\intro\\gbear-0.png", 0.05),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\static-2.png", 0.05), ("images\\intro\\static-7.png", 0.05),
                                  ("images\\intro\\itsme-2.png", 0.05), ("images\\intro\\crying-0.png", 0.05),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\static-7.png", 0.05),
                                  ("images\\intro\\static-5.png", 0.05), ("images\\intro\\stuffed.png", 0.35),
                                  ("images\\intro\\static-4.png", 0.05), ("images\\intro\\stuffed.png", 0.17),
                                  ("images\\intro\\static-1.png", 0.05), ("images\\intro\\static-2.png", 0.05),
                                  ("images\\intro\\b-2.png", 0.08), ("images\\intro\\static-6.png", 0.05),
                                  ("images\\intro\\static-4.png", 0.05), ("images\\intro\\b-5.png", 0.25),
                                  ("images\\intro\\stuffed.png", 0.14), ("images\\intro\\static-5.png", 0.06),
                                  ("images\\intro\\static-2.png", 0.06), ("images\\intro\\static-5.png", 0.05),
                                  ("images\\intro\\static-1.png", 0.06), ("images\\intro\\static-6.png", 0.05),
                                  ("images\\intro\\static-2.png", 0.06), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\static-0.png", 0.06), ("images\\intro\\static-1.png", 0.05),
                                  ("images\\intro\\static-7.png", 0.06), ("images\\intro\\static-3.png", 0.05),
                                  ("images\\intro\\pyDLASYIAS-0.png", 1), ("images\\intro\\static-4.png", 0.05),
                                  ("images\\intro\\static-2.png", 0.05), ("images\\intro\\static-1.png", 0.05)], loop=False)

    musicBox = pygame.mixer.Sound("sounds\\misc\\musicbox.wav")
    musicBox.play(0)

    chickenAvailable = True
    rabbitAvailable = True
    bearAvailable = True
    foxAvailable = True
    guardAvailable = True

    intro.play()

    while running:

        pos = (mousex, mousey)
        mouseClick = False
        pygame.display.set_caption("--pyDLASYIAS %s-- -%s FPS-" %(Globals.version, round(FPSCLOCK.get_fps())))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClick = True

        if scene == "intro":

            if intro.state == pyganim.PLAYING:
                intro.blit(screen, (0,0))

            if intro.state == pyganim.STOPPED or mouseClick:
                pygame.mixer.stop()
                scene = "main"

        if scene == "main":

            screen.fill((0,0,0))

            group.add(title)
            group.add(customNightButton)
            group.add(multiplayerButton)

            if customNightButton.rect.collidepoint(pos) and mouseClick:
                scene = "custom"

            if multiplayerButton.rect.collidepoint(pos) and mouseClick:
                scene = "address"

            if multiplayerButton.rect.collidepoint(pos):
                multiplayerButton.changeImg("menu\\multiplayer-1")

            if not multiplayerButton.rect.collidepoint(pos):
                multiplayerButton.changeImg("menu\\multiplayer-0")

            if customNightButton.rect.collidepoint(pos):
                customNightButton.changeImg("menu\\custom-1")

            if not customNightButton.rect.collidepoint(pos):
                customNightButton.changeImg("menu\\custom-0")

            group.update()
            group.draw(screen)

        if scene == "address":

            screen.fill((0,0,0))

            ip = inputbox.ask(screen, "IP (Blank for 127.0.0.1)")
            port = inputbox.ask(screen, "PORT (Blank for 1987)")

            print(ip, port)

            if ip == "":
                ip = "127.0.0.1"

            if port == "":
                port = 1987

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, int(port)))

            except OSError:
                print("Looks like something failed. Try again please!")
                pygame.time.delay(200)
                pygame.quit()
                raise

            thread = threading.Thread(group=None, target=receiveData, name="ReceiveData", args=(sock))
            thread.setDaemon(True)
            thread.start()

            scene = "multihall"


        if scene == "multihall":
            screen.fill((0,0,0))



            multigroup.update()
            multigroup.draw(screen)

            # char = input("1 Guard / 2 Rabbit / 3 Chicken / 4 Fox (Doesn't work) / 5 Bear (Doesn't work)")
            #
            # if char == "1":
            #     import pyDLASYIAS.multiplayer.guard as guard
            #     guard.guardMain(host=ip, port=int(port))
            #
            # if char == "2":
            #     import pyDLASYIAS.multiplayer.rabbit as rabbit
            #     rabbit.rabbitMain(host=ip, port=int(port))
            #
            # if char == "3":
            #     import pyDLASYIAS.multiplayer.chicken as chicken
            #     chicken.chickenMain(host=ip, port=int(port))


        if scene == "custom":

            screen.fill((0,0,0))

            customgroup.add(timeleft)
            customgroup.add(timeright)

            customgroup.add(powerleft)
            customgroup.add(powerright)

            customgroup.add(ready)

            customgroup.add(bearspr)
            customgroup.add(bearleft)
            customgroup.add(bearright)

            customgroup.add(rabbitspr)
            customgroup.add(rabbitleft)
            customgroup.add(rabbitright)

            customgroup.add(chickenspr)
            customgroup.add(chickenleft)
            customgroup.add(chickenright)

            customgroup.add(foxspr)
            customgroup.add(foxleft)
            customgroup.add(foxright)

            if bearleft.rect.collidepoint(pos) and mouseClick and bearai != 0:
                bearai -= 1

            if bearright.rect.collidepoint(pos) and mouseClick and bearai != 20:
                bearai += 1

            if rabbitleft.rect.collidepoint(pos) and mouseClick and rabbitai != 0:
                rabbitai -= 1

            if rabbitright.rect.collidepoint(pos) and mouseClick and rabbitai != 20:
                rabbitai += 1

            if chickenleft.rect.collidepoint(pos) and mouseClick and chickenai != 0:
                chickenai -= 1

            if chickenright.rect.collidepoint(pos) and mouseClick and chickenai != 20:
                chickenai += 1

            if foxleft.rect.collidepoint(pos) and mouseClick and foxai != 0:
                foxai -= 1

            if foxright.rect.collidepoint(pos) and mouseClick and foxai != 20:
                foxai += 1

            if timeleft.rect.collidepoint(pos) and mouseClick and time != 0:
                time -= 1

            if timeright.rect.collidepoint(pos) and mouseClick and time != 6:
                time += 1

            if powerleft.rect.collidepoint(pos) and mouseClick:
                if power == 0:
                    power = 100
                else:
                    power -= 1

            if powerright.rect.collidepoint(pos) and mouseClick and time != 6:
                if power == 100:
                    power = 0
                else:
                    power += 1

            if ready.rect.collidepoint(pos) and mouseClick:
                rabbit = animatronics.animatronic("Rabbit", "rabbit", rabbitai)
                chicken = animatronics.animatronic("Chicken", "chicken", chickenai)
                fox = animatronics.animatronic("Fox", "fox", foxai)
                bear = animatronics.animatronic("Bear", "bear", bearai)
                main.main(power=power, time=time)

            timeLabel = font.render(str(time), True, (255, 255, 255))
            powerLabel = font.render(str(power), True, (255, 255, 255))

            rabbitaiLabel = font.render(str(rabbitai), True, (255, 255, 255))
            chickenaiLabel = font.render(str(chickenai), True, (255, 255, 255))
            foxaiLabel = font.render(str(foxai), True, (255, 255, 255))
            bearaiLabel = font.render(str(bearai), True, (255, 255, 255))

            screen.fill((0, 0, 0))

            screen.blit(timeLabel, (257, 560))
            screen.blit(powerLabel, (533, 560))

            screen.blit(font.render("Time", True, (255, 255, 255)), (257, 620))
            screen.blit(font.render("Power", True, (255, 255, 255)), (535, 620))

            screen.blit(bearaiLabel, (257, 480))
            screen.blit(rabbitaiLabel, (540, 480))
            screen.blit(chickenaiLabel, (822, 480))
            screen.blit(foxaiLabel, (1102, 480))

            customgroup.update()
            customgroup.draw(screen)

        #screen.blit(pygame.font.Font(None, 42).render("%s FPS" % round(FPSCLOCK.get_fps()), True, (0, 255, 0)), (10, 10))

        pygame.display.flip()
        pygame.display.update()
        FPSCLOCK.tick(30)

def receiveData(socket):
    global data
    data = socket.recv(1024)
    return data

try:
    if __name__ == '__main__':
        launcher()
except:
    Globals.log.write("\n Unexpected error: %s %s \n" %
                      (sys.exc_info()[0], time.strftime("%H:%M:%S")))
    raise
