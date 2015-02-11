#!/usr/bin/env python
import sys
import os
import time
import random
import _thread
import threading
import pygame
from pygame.locals import *
import pyDLASYIAS.Globals as Globals
import pyDLASYIAS.animatronics as animatronics
import pyDLASYIAS.sprite as sprite
import pyDLASYIAS.main as main
import pyDLASYIAS.utils.functions as utils
import pyDLASYIAS.pyganim as pyganim

def launcher():
    running = True
    screen = pygame.display.set_mode((1280, 720), 0, 32)
    pygame.display.set_caption("--pyDLASYIAS %s--" %(Globals.version))
    FPSCLOCK = pygame.time.Clock()

    pygame.init()

    font = pygame.font.Font(None, 50)
    group = pygame.sprite.Group()

    mousex = 0
    mousey = 0

    time = 0
    timeleft = sprite.Sprite(startpos=(122,560), image="launcher\\buttons\\0")
    timeleft.groups = group

    timeright = sprite.Sprite(startpos=(311,560), image="launcher\\buttons\\1")
    timeright.groups = group

    power = 100
    powerleft = sprite.Sprite(startpos=(406,560), image="launcher\\buttons\\0")
    powerleft.groups = group

    powerright = sprite.Sprite(startpos=(593,560), image="launcher\\buttons\\1")
    powerright.groups = group

    ready = sprite.Sprite(startpos=(1044,603), image="launcher\\buttons\\2")
    ready.groups = group

    bearspr = sprite.Sprite(startpos=(118,187), image="launcher\\animatronics\\b")
    bearspr.groups = group

    bearai = 0

    bearleft = sprite.Sprite(startpos=(122,470), image="launcher\\buttons\\0")
    bearleft.groups = group

    bearright = sprite.Sprite(startpos=(311,470), image="launcher\\buttons\\1")
    bearright.groups = group


    rabbitspr = sprite.Sprite(startpos=(403,187), image="launcher\\animatronics\\r")
    rabbitspr.groups = group

    rabbitai = 0

    rabbitleft = sprite.Sprite(startpos=(406,470), image="launcher\\buttons\\0")
    rabbitleft.groups = group

    rabbitright = sprite.Sprite(startpos=(593,470), image="launcher\\buttons\\1")
    rabbitright.groups = group


    chickenspr = sprite.Sprite(startpos=(682,187), image="launcher\\animatronics\\c")
    chickenspr.groups = group

    chickenai = 0

    chickenleft = sprite.Sprite(startpos=(690,470), image="launcher\\buttons\\0")
    chickenleft.groups = group

    chickenright = sprite.Sprite(startpos=(876,470), image="launcher\\buttons\\1")
    chickenright.groups = group

    foxspr = sprite.Sprite(startpos=(957,187), image="launcher\\animatronics\\f")
    foxspr.groups = group

    foxai = 0

    foxleft = sprite.Sprite(startpos=(969,470), image="launcher\\buttons\\0")
    foxleft.groups = group

    foxright = sprite.Sprite(startpos=(1154,470), image="launcher\\buttons\\1")
    foxright.groups = group

    while running:

        pos = (mousex, mousey)
        mouseClick = False

        group.add(timeleft)
        group.add(timeright)

        group.add(powerleft)
        group.add(powerright)

        group.add(ready)

        group.add(bearspr)
        group.add(bearleft)
        group.add(bearright)

        group.add(rabbitspr)
        group.add(rabbitleft)
        group.add(rabbitright)

        group.add(chickenspr)
        group.add(chickenleft)
        group.add(chickenright)

        group.add(foxspr)
        group.add(foxleft)
        group.add(foxright)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClick = True

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


        timeLabel = font.render(str(time), True, (255,255,255))
        powerLabel = font.render(str(power), True, (255,255,255))

        rabbitaiLabel = font.render(str(rabbitai), True, (255,255,255))
        chickenaiLabel = font.render(str(chickenai), True, (255,255,255))
        foxaiLabel = font.render(str(foxai), True, (255,255,255))
        bearaiLabel = font.render(str(bearai), True, (255,255,255))

        screen.fill((0,0,0))

        screen.blit(timeLabel, (257,560))
        screen.blit(powerLabel, (533,560))

        screen.blit(font.render("Time", True, (255,255,255)), (257,620))
        screen.blit(font.render("Power", True, (255,255,255)), (535,620))

        screen.blit(bearaiLabel, (257,480))
        screen.blit(rabbitaiLabel, (540,480))
        screen.blit(chickenaiLabel, (822,480))
        screen.blit(foxaiLabel, (1102,480))

        screen.blit(pygame.font.Font(None, 42).render("%s FPS" % round(FPSCLOCK.get_fps()), True, (0,255,0)), (10,10))

        group.update()
        group.draw(screen)
        pygame.display.flip()
        FPSCLOCK.tick(30)

try:
    if __name__ == '__main__':
        launcher()
except:
    Globals.log.write("\n Unexpected error: %s %s \n" % (sys.exc_info()[0], time.strftime("%H:%M:%S")))
    raise
