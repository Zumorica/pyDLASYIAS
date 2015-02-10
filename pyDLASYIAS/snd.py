import pygame
from pygame.locals import *

pygame.init()

def init():
    global channelZero, channelOne, channelTwo, channelThree, channelFour, channelFive, channelSix, channelSeven, \
                    channelEight, channelNine, channelTen, channelEleven, channelTwelve, channelThirteen, channelFourteen, \
                    channelFifteen, channelSixteen, channelSeventeen, channelEighteen, channelNineteen, channelTwenty, \
                    channelTwentytwo, channelTwentyone, channelTwentythree, channelTwentyfour, channelTwentyfive, \
                    channelTwentysix, channelTwentyseven, channelTwentyeight, channelTwentynine, channelThirty

    pygame.mixer.set_num_channels(31)

    channelZero = pygame.mixer.Channel(0)
    channelOne = pygame.mixer.Channel(1)
    channelTwo = pygame.mixer.Channel(2)
    channelThree = pygame.mixer.Channel(3)
    channelFour = pygame.mixer.Channel(4)
    channelFive = pygame.mixer.Channel(5)
    channelSix = pygame.mixer.Channel(6)
    channelSeven = pygame.mixer.Channel(7)
    channelEight = pygame.mixer.Channel(8)
    channelNine = pygame.mixer.Channel(9)
    channelTen = pygame.mixer.Channel(10)
    channelEleven = pygame.mixer.Channel(11)
    channelTwelve = pygame.mixer.Channel(12)
    channelThirteen = pygame.mixer.Channel(13)
    channelFourteen = pygame.mixer.Channel(14)
    channelFifteen = pygame.mixer.Channel(15)
    channelSixteen = pygame.mixer.Channel(16)
    channelSeventeen = pygame.mixer.Channel(17)
    channelEighteen = pygame.mixer.Channel(18)
    channelNineteen = pygame.mixer.Channel(19)
    channelTwenty = pygame.mixer.Channel(20)
    channelTwentyone = pygame.mixer.Channel(21)
    channelTwentytwo = pygame.mixer.Channel(22)
    channelTwentythree = pygame.mixer.Channel(23)
    channelTwentyfour = pygame.mixer.Channel(24)
    channelTwentyfive = pygame.mixer.Channel(25)
    channelTwentysix = pygame.mixer.Channel(26)
    channelTwentyseven = pygame.mixer.Channel(27)
    channelTwentyeight = pygame.mixer.Channel(28)
    channelTwentynine = pygame.mixer.Channel(29)
    channelThirty = pygame.mixer.Channel(30)

    global xscream, xscreamTwo, giggle, freddyGiggle, freddyGiggleTwo, freddyGiggleThree, windowScare, robotVoice, \
                  breathing, breathingTwo, breathingThree, breathingFour, chimes, children, doorSound, doorKnocking, \
                  doorPoundering, freddyNose, musicBox, powerDown, lightHum, buttonError, blip, cameraSound, cameraSoundTwo, \
                  computerNoise, garble, garbleTwo, garbleThree, putDown, pots, potsTwo, potsThree, potsFour, static, ambience, \
                  ambienceTwo, eerieAmbience, fanSound

    xscream = pygame.mixer.Sound("sounds\\scary\\XSCREAM.wav")
    xscreamTwo = pygame.mixer.Sound("sounds\\scary\\XSCREAM2.wav")

    giggle = pygame.mixer.Sound("sounds\\scary\\giggle.wav")
    freddyGiggle = pygame.mixer.Sound("sounds\\scary\\freddygiggle.wav")
    freddyGiggleTwo = pygame.mixer.Sound("sounds\\scary\\freddygiggle2.wav")
    freddyGiggleThree = pygame.mixer.Sound("sounds\\scary\\freddygiggle3.wav")

    windowScare = pygame.mixer.Sound("sounds\\scary\\windowscare.wav")

    robotVoice = pygame.mixer.Sound("sounds\\scary\\robotvoice.wav")

    breathing = pygame.mixer.Sound("sounds\\scary\\breathing.wav")
    breathingTwo = pygame.mixer.Sound("sounds\\scary\\breathing2.wav")
    breathingThree = pygame.mixer.Sound("sounds\\scary\\breathing3.wav")
    breathingFour = pygame.mixer.Sound("sounds\\scary\\breathing4.wav")

    chimes = pygame.mixer.Sound("sounds\\misc\\6AM.wav")
    children = pygame.mixer.Sound("sounds\\misc\\children.wav")

    doorSound = pygame.mixer.Sound("sounds\\misc\\door.wav")
    doorknocking = pygame.mixer.Sound("sounds\\misc\\doorknocking.wav")
    doorPoundering = pygame.mixer.Sound("sounds\\misc\\doorpounding.wav")

    freddyNose = pygame.mixer.Sound("sounds\\misc\\honk.wav")
    musicBox = pygame.mixer.Sound("sounds\\misc\\musicbox.wav")
    powerDown = pygame.mixer.Sound("sounds\\misc\\powerdown.wav")

    lightHum = pygame.mixer.Sound("sounds\\misc\\lighthum.wav")
    buttonError = pygame.mixer.Sound("sounds\\misc\\error.wav")

    blip = pygame.mixer.Sound("sounds\\camera\\blip.wav")
    cameraSound = pygame.mixer.Sound("sounds\\camera\\camerasound.wav")
    cameraSoundTwo = pygame.mixer.Sound("sounds\\camera\\camerasound2.wav")

    computerNoise = pygame.mixer.Sound("sounds\\camera\\computernoise.wav")
    garble = pygame.mixer.Sound("sounds\\camera\\garble.wav")
    garbleTwo = pygame.mixer.Sound("sounds\\camera\\garble2.wav")
    garbleThree = pygame.mixer.Sound("sounds\\camera\\garble3.wav")

    putDown = pygame.mixer.Sound("sounds\\camera\\putdown.wav")

    pots = pygame.mixer.Sound("sounds\\camera\\pots.wav")
    potsTwo = pygame.mixer.Sound("sounds\\camera\\pots2.wav")
    potsThree = pygame.mixer.Sound("sounds\\camera\\pots3.wav")
    potsFour = pygame.mixer.Sound("sounds\\camera\\pots4.wav")

    static = pygame.mixer.Sound("sounds\\camera\\static2.wav")

    ambience = pygame.mixer.Sound("sounds\\ambience\\ambience.wav")
    ambienceTwo = pygame.mixer.Sound("sounds\\ambience\\ambience2.wav")
    eerieAmbience = pygame.mixer.Sound("sounds\\ambience\\eerieambience.wav")

    fanSound = pygame.mixer.Sound("sounds\\ambience\\fan.wav")
