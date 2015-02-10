import pyDLASYIAS.sprite as sprite
import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_mode((1280,720), 0, 0)

def init():
    global allgroup, officegroup, camgroup, scaregroup

    allgroup = pygame.sprite.Group()
    officegroup = pygame.sprite.LayeredUpdates()
    camgroup = pygame.sprite.LayeredUpdates()
    scaregroup = pygame.sprite.LayeredUpdates()

    global leftButton, rightButton, leftDoorButton, leftLightButton, rightDoorButton, rightLightButton, camButton, \
           map, camButtonOneA, camButtonOneB, camButtonOneC, camButtonTwoA, camButtonTwoB, camButtonThree, camButtonFourA, \
           camButtonFourB, camButtonFive, camButtonSix, camButtonSeven, leftDoor, rightDoor, foxSprinting, leftDoorClose, \
           leftDoorOpen, rightDoorClose, rightDoorOpen, chickenScarejump, rabbitScarejump, bearNormalScarejump, foxScarejump, \
           bearPowerdownScarejump, staticTransparent, bg, cameraOpen, cameraClose

    leftButton = sprite.Sprite(startpos=(0, 180), image="office\\button\\left\\0")
    leftButton.groups = allgroup, officegroup

    rightButton = sprite.Sprite(startpos=(1500, 180), image="office\\button\\right\\0")
    rightButton.groups = allgroup, officegroup

    leftDoorButton = sprite.Sprite(startpos=(34, 232), image="office\\button\\collision")
    leftDoorButton.groups = allgroup, officegroup

    leftLightButton = sprite.Sprite(startpos=(34, 314), image="office\\button\\collision")
    leftLightButton.groups = allgroup, officegroup

    rightDoorButton = sprite.Sprite(startpos=(1525,232), image="office\\button\\collision")
    rightDoorButton.groups = allgroup, officegroup

    rightLightButton = sprite.Sprite(startpos=(1525,314), image="office\\button\\collision")
    rightLightButton.groups = allgroup, officegroup

    camButton = sprite.Sprite(startpos=(245, 635), image="ui\\button\\camera")
    camButton.groups = allgroup, officegroup, camgroup

    map = sprite.Sprite(startpos=(848, 313), image="ui\\map")
    map.groups = allgroup, camgroup

    camButtonOneA = sprite.Sprite(startpos=(983,353), image="ui\\button\\cam1a")
    camButtonOneA.groups = allgroup, camgroup

    camButtonOneB = sprite.Sprite(startpos=(963,409), image="ui\\button\\cam1b")
    camButtonOneB.groups = allgroup, camgroup

    camButtonOneC = sprite.Sprite(startpos=(931,487), image="ui\\button\\cam1c")
    camButtonOneC.groups = allgroup, camgroup

    camButtonTwoA = sprite.Sprite(startpos=(954,574), image="ui\\button\\cam2a")
    camButtonTwoA.groups = allgroup, camgroup

    camButtonTwoB = sprite.Sprite(startpos=(954,626), image="ui\\button\\cam2b")
    camButtonTwoB.groups = allgroup, camgroup

    camButtonThree = sprite.Sprite(startpos=(877,574), image="ui\\button\\cam3")
    camButtonThree.groups = allgroup, camgroup

    camButtonFourA = sprite.Sprite(startpos=(1060,574), image="ui\\button\\cam4a")
    camButtonFourA.groups = allgroup, camgroup

    camButtonFourB = sprite.Sprite(startpos=(1060,626), image="ui\\button\\cam4b")
    camButtonFourB.groups = allgroup, camgroup

    camButtonFive = sprite.Sprite(startpos=(857,436), image="ui\\button\\cam5")
    camButtonFive.groups = allgroup, camgroup

    camButtonSix = sprite.Sprite(startpos=(1163,556), image="ui\\button\\cam6")
    camButtonSix.groups = allgroup, camgroup

    camButtonSeven = sprite.Sprite(startpos=(1172,424), image="ui\\button\\cam7")
    camButtonSeven.groups = allgroup, camgroup

    leftDoor = sprite.Sprite(startpos=(72,0), image="office\\doors\\left\\0")
    leftDoor.groups = allgroup, officegroup

    rightDoor = sprite.Sprite(startpos=(1270,0), image="office\\doors\\right\\0")
    rightDoor.groups = allgroup, officegroup

    foxSprinting = sprite.Animated(startpos=(0,0), images=["cameras\\cam2a\\animation\\0.png","cameras\\cam2a\\animation\\1.png",
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
    foxSprinting.groups = camgroup, allgroup

    leftDoorClose = sprite.Animated(startpos=(72,0), images=["office\\doors\\left\\0.png", "office\\doors\\left\\1.png",
                                                             "office\\doors\\left\\2.png", "office\\doors\\left\\3.png",
                                                             "office\\doors\\left\\4.png", "office\\doors\\left\\5.png",
                                                             "office\\doors\\left\\6.png", "office\\doors\\left\\7.png",
                                                             "office\\doors\\left\\8.png", "office\\doors\\left\\9.png",
                                                             "office\\doors\\left\\10.png", "office\\doors\\left\\11.png",
                                                             "office\\doors\\left\\12.png", "office\\doors\\left\\13.png",
                                                             "office\\doors\\left\\14.png", "office\\doors\\left\\15.png"])
    leftDoorClose.groups = allgroup, officegroup

    leftDoorOpen = sprite.Animated(startpos=(72,0), images=["office\\doors\\left\\15.png", "office\\doors\\left\\14.png",
                                                            "office\\doors\\left\\13.png", "office\\doors\\left\\12.png",
                                                            "office\\doors\\left\\11.png", "office\\doors\\left\\10.png",
                                                            "office\\doors\\left\\9.png", "office\\doors\\left\\8.png",
                                                            "office\\doors\\left\\7.png", "office\\doors\\left\\6.png",
                                                            "office\\doors\\left\\5.png", "office\\doors\\left\\4.png",
                                                            "office\\doors\\left\\3.png", "office\\doors\\left\\2.png",
                                                            "office\\doors\\left\\1.png", "office\\doors\\left\\0.png"])
    leftDoorOpen.groups = allgroup, officegroup

    rightDoorClose = sprite.Animated(startpos=(1270,0), images=["office\\doors\\right\\0.png", "office\\doors\\right\\1.png",
                                                                   "office\\doors\\right\\2.png", "office\\doors\\right\\3.png",
                                                                   "office\\doors\\right\\4.png", "office\\doors\\right\\5.png",
                                                                   "office\\doors\\right\\6.png", "office\\doors\\right\\7.png",
                                                                   "office\\doors\\right\\8.png", "office\\doors\\right\\9.png",
                                                                   "office\\doors\\right\\10.png", "office\\doors\\right\\11.png",
                                                                   "office\\doors\\right\\12.png", "office\\doors\\right\\13.png",
                                                                   "office\\doors\\right\\14.png", "office\\doors\\right\\15.png"])
    rightDoorClose.groups = allgroup, officegroup

    rightDoorOpen = sprite.Animated(startpos=(1270,0), images=["office\\doors\\right\\15.png", "office\\doors\\right\\14.png",
                                                                   "office\\doors\\right\\13.png", "office\\doors\\right\\12.png",
                                                                   "office\\doors\\right\\11.png", "office\\doors\\right\\10.png",
                                                                   "office\\doors\\right\\9.png", "office\\doors\\right\\8.png",
                                                                   "office\\doors\\right\\7.png", "office\\doors\\right\\6.png",
                                                                   "office\\doors\\right\\5.png", "office\\doors\\right\\4.png",
                                                                   "office\\doors\\right\\3.png", "office\\doors\\right\\2.png",
                                                                   "office\\doors\\right\\1.png", "office\\doors\\right\\0.png"])
    rightDoorOpen.groups = allgroup, officegroup

    chickenScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\chicken\\0.png", "office\\scarejump\\chicken\\1.png",
                                                                    "office\\scarejump\\chicken\\2.png", "office\\scarejump\\chicken\\3.png",
                                                                    "office\\scarejump\\chicken\\4.png", "office\\scarejump\\chicken\\5.png",
                                                                    "office\\scarejump\\chicken\\6.png", "office\\scarejump\\chicken\\7.png",
                                                                    "office\\scarejump\\chicken\\8.png", "office\\scarejump\\chicken\\9.png",
                                                                    "office\\scarejump\\chicken\\10.png", "office\\scarejump\\chicken\\11.png",
                                                                    "office\\scarejump\\chicken\\12.png"])
    chickenScarejump.groups = allgroup, scaregroup

    rabbitScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\rabbit\\0.png", "office\\scarejump\\rabbit\\1.png",
                                                                   "office\\scarejump\\rabbit\\2.png", "office\\scarejump\\rabbit\\3.png",
                                                                   "office\\scarejump\\rabbit\\4.png", "office\\scarejump\\rabbit\\5.png",
                                                                   "office\\scarejump\\rabbit\\6.png", "office\\scarejump\\rabbit\\7.png",
                                                                   "office\\scarejump\\rabbit\\8.png", "office\\scarejump\\rabbit\\9.png",
                                                                   "office\\scarejump\\rabbit\\10.png"])
    rabbitScarejump.groups = allgroup, scaregroup

    foxScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\fox\\0.png", "office\\scarejump\\fox\\1.png",
                                                                "office\\scarejump\\fox\\2.png", "office\\scarejump\\fox\\3.png",
                                                                "office\\scarejump\\fox\\4.png", "office\\scarejump\\fox\\5.png",
                                                                "office\\scarejump\\fox\\6.png", "office\\scarejump\\fox\\7.png",
                                                                "office\\scarejump\\fox\\8.png", "office\\scarejump\\fox\\9.png",
                                                                "office\\scarejump\\fox\\10.png", "office\\scarejump\\fox\\11.png",
                                                                "office\\scarejump\\fox\\12.png", "office\\scarejump\\fox\\13.png",
                                                                "office\\scarejump\\fox\\14.png", "office\\scarejump\\fox\\15.png",
                                                                "office\\scarejump\\fox\\16.png", "office\\scarejump\\fox\\17.png",
                                                                "office\\scarejump\\fox\\18.png"])
    foxScarejump.groups = allgroup, scaregroup

    bearNormalScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\bear\\normal\\0.png", "office\\scarejump\\bear\\normal\\1.png",
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
    bearNormalScarejump.groups = allgroup, scaregroup

    bearPowerdownScarejump = sprite.Animated(startpos=(0,0), images=["office\\scarejump\\bear\\powerdown\\0.png", "office\\scarejump\\bear\\powerdown\\1.png",
                                                                          "office\\scarejump\\bear\\powerdown\\2.png", "office\\scarejump\\bear\\powerdown\\3.png",
                                                                          "office\\scarejump\\bear\\powerdown\\4.png", "office\\scarejump\\bear\\powerdown\\5.png",
                                                                          "office\\scarejump\\bear\\powerdown\\6.png", "office\\scarejump\\bear\\powerdown\\7.png",
                                                                          "office\\scarejump\\bear\\powerdown\\8.png", "office\\scarejump\\bear\\powerdown\\9.png",
                                                                          "office\\scarejump\\bear\\powerdown\\10.png", "office\\scarejump\\bear\\powerdown\\11.png",
                                                                          "office\\scarejump\\bear\\powerdown\\12.png", "office\\scarejump\\bear\\powerdown\\13.png",
                                                                          "office\\scarejump\\bear\\powerdown\\14.png", "office\\scarejump\\bear\\powerdown\\15.png",
                                                                          "office\\scarejump\\bear\\powerdown\\16.png", "office\\scarejump\\bear\\powerdown\\17.png",
                                                                          "office\\scarejump\\bear\\powerdown\\18.png", "office\\scarejump\\bear\\powerdown\\19.png"])
    bearPowerdownScarejump.groups = allgroup, scaregroup

    cameraOpen = sprite.Animated(startpos=(0,0), images=["cameras\\misc\\animation\\0.png", "cameras\\misc\\animation\\1.png", "cameras\\misc\\animation\\2.png",
                                                         "cameras\\misc\\animation\\3.png", "cameras\\misc\\animation\\4.png", "cameras\\misc\\animation\\5.png",
                                                         "cameras\\misc\\animation\\6.png", "cameras\\misc\\animation\\7.png", "cameras\\misc\\animation\\8.png",
                                                         "cameras\\misc\\animation\\9.png", "cameras\\misc\\animation\\10.png"])
    cameraOpen.groups = allgroup, officegroup

    cameraClose = sprite.Animated(startpos=(0,0), images=["cameras\\misc\\animation\\10.png", "cameras\\misc\\animation\\9.png", "cameras\\misc\\animation\\8.png",
                                                          "cameras\\misc\\animation\\7.png", "cameras\\misc\\animation\\6.png", "cameras\\misc\\animation\\5.png",
                                                          "cameras\\misc\\animation\\4.png", "cameras\\misc\\animation\\3.png", "cameras\\misc\\animation\\2.png",
                                                          "cameras\\misc\\animation\\1.png", "cameras\\misc\\animation\\0.png"])
    cameraClose.groups = allgroup, officegroup


    staticTransparent = sprite.Sprite(startpos=(0,0), image="cameras\\misc\\static\\transparent\\0")
    staticTransparent.groups = allgroup, officegroup, camgroup, scaregroup

    bg = sprite.Sprite("office\\0", (0,0))
    bg.groups = allgroup, officegroup, camgroup, scaregroup

    allgroup.add(leftButton)
    allgroup.add(rightButton)
    allgroup.add(leftDoorButton)
    allgroup.add(leftLightButton)
    allgroup.add(rightDoorButton)
    allgroup.add(rightLightButton)
    allgroup.add(camButton)
    allgroup.add(map)
    allgroup.add(bg)
    allgroup.add(camButtonOneA)
    allgroup.add(bearNormalScarejump)
    allgroup.add(bearPowerdownScarejump)
    allgroup.add(foxScarejump)
    allgroup.add(rabbitScarejump)
    allgroup.add(chickenScarejump)
    allgroup.add(leftDoorClose)
    allgroup.add(rightDoorOpen)
    allgroup.add(leftDoorOpen)
    allgroup.add(rightDoorClose)
    allgroup.add(camButtonOneA)
    allgroup.add(camButtonOneB)
    allgroup.add(camButtonOneC)
    allgroup.add(camButtonTwoA)
    allgroup.add(camButtonTwoB)
    allgroup.add(camButtonThree)
    allgroup.add(camButtonFourA)
    allgroup.add(camButtonFourB)
    allgroup.add(camButtonFive)
    allgroup.add(camButtonSix)
    allgroup.add(camButtonSeven)
    allgroup.add(staticTransparent)
    allgroup.add(leftDoor)
    allgroup.add(rightDoor)
