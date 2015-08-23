import cocos
import pyglet
import pygame.mixer
import random
import cocos
import time
import sys
import os
from pyglet.gl import *
from pyglet.gl.glu import *
from cocos.director import director
from cocos.scenes import *

__all__ = ['Backgrounds', 'Sounds', 'Cameras', 'Channel']

Backgrounds = {"office" : {"0" : pyglet.image.load("images\\office\\0.png"),
                           "1" : pyglet.image.load("images\\office\\1.png"),
                           "2" : pyglet.image.load("images\\office\\2.png"),
                           "r" : pyglet.image.load("images\\office\\r.png"),
                           "c" : pyglet.image.load("images\\office\\c.png")},
               "camera" : {"cam1a" : {"0" : pyglet.image.load("images\\cameras\\cam1a\\0.png"),
                                      "b" : pyglet.image.load("images\\cameras\\cam1a\\b.png"),
                                      "b-1" : pyglet.image.load("images\\cameras\\cam1a\\b-1.png"),
                                      "bc" : pyglet.image.load("images\\cameras\\cam1a\\bc.png"),
                                      "br" : pyglet.image.load("images\\cameras\\cam1a\\br.png"),
                                      "brc" : pyglet.image.load("images\\cameras\\cam1a\\brc.png"),
                                      "brc-1" : pyglet.image.load("images\\cameras\\cam1a\\brc-1.png")},
                           "cam1b" : {"0" : pyglet.image.load("images\\cameras\\cam1b\\0.png"),
                                      "b" : pyglet.image.load("images\\cameras\\cam1b\\b.png"),
                                      "c" : pyglet.image.load("images\\cameras\\cam1b\\c.png"),
                                      "c-1" : pyglet.image.load("images\\cameras\\cam1b\\c-1.png"),
                                      "r" : pyglet.image.load("images\\cameras\\cam1b\\r.png"),
                                      "r-1" : pyglet.image.load("images\\cameras\\cam1b\\r-1.png")},
                           "cam1c" : {"0" : pyglet.image.load("images\\cameras\\cam1c\\0.png"),
                                      "1" : pyglet.image.load("images\\cameras\\cam1c\\1.png"),
                                      "2" : pyglet.image.load("images\\cameras\\cam1c\\2.png"),
                                      "3" : pyglet.image.load("images\\cameras\\cam1c\\3.png"),
                                      "4" : pyglet.image.load("images\\cameras\\cam1c\\4.png"),
                                      "5" : pyglet.image.load("images\\cameras\\cam1c\\5.png")},
                           "cam2a" : {"0" : pyglet.image.load("images\\cameras\\cam2a\\0.png"),
                                      "1" : pyglet.image.load("images\\cameras\\cam2a\\1.png"),
                                      "r" : pyglet.image.load("images\\cameras\\cam2a\\r.png")},
                           "cam2b" : {"0" : pyglet.image.load("images\\cameras\\cam2b\\0.png"),
                                      "1" : pyglet.image.load("images\\cameras\\cam2b\\1.png"),
                                      "2" : pyglet.image.load("images\\cameras\\cam2b\\2.png"),
                                      "r" : pyglet.image.load("images\\cameras\\cam2b\\r.png"),
                                      "r-1" : pyglet.image.load("images\\cameras\\cam2b\\r-1.png")},
                           "cam3" : {"0" : pyglet.image.load("images\\cameras\\cam3\\0.png"),
                                     "r" : pyglet.image.load("images\\cameras\\cam3\\r.png")},
                           "cam4a" : {"0" : pyglet.image.load("images\\cameras\\cam4a\\0.png"),
                                      "1" : pyglet.image.load("images\\cameras\\cam4a\\1.png"),
                                      "2" : pyglet.image.load("images\\cameras\\cam4a\\2.png"),
                                      "b" : pyglet.image.load("images\\cameras\\cam4a\\b.png"),
                                      "c" : pyglet.image.load("images\\cameras\\cam4a\\c.png"),
                                      "c-1" : pyglet.image.load("images\\cameras\\cam4a\\c-1.png")},
                           "cam4b" : {"0" : pyglet.image.load("images\\cameras\\cam4b\\0.png"),
                                      "1" : pyglet.image.load("images\\cameras\\cam4b\\1.png"),
                                      "2" : pyglet.image.load("images\\cameras\\cam4b\\2.png"),
                                      "3" : pyglet.image.load("images\\cameras\\cam4b\\3.png"),
                                      "4" : pyglet.image.load("images\\cameras\\cam4b\\4.png"),
                                      "b" : pyglet.image.load("images\\cameras\\cam4b\\b.png"),
                                      "c" : pyglet.image.load("images\\cameras\\cam4b\\c.png"),
                                      "c-1" : pyglet.image.load("images\\cameras\\cam4b\\c-1.png"),
                                      "c-2" : pyglet.image.load("images\\cameras\\cam4b\\c-2.png")},
                           "cam5" : {"0" : pyglet.image.load("images\\cameras\\cam5\\0.png"),
                                     "1" : pyglet.image.load("images\\cameras\\cam5\\1.png"),
                                     "r" : pyglet.image.load("images\\cameras\\cam5\\r.png"),
                                     "r-1" : pyglet.image.load("images\\cameras\\cam5\\r-1.png")},
                           "cam6" : {"0" : pyglet.image.load("images\\cameras\\misc\\black.png")},
                           "cam7" : {"0" : pyglet.image.load("images\\cameras\\cam7\\0.png"),
                                     "b" : pyglet.image.load("images\\cameras\\cam7\\b.png"),
                                     "c" : pyglet.image.load("images\\cameras\\cam7\\c.png"),
                                     "c-1" : pyglet.image.load("images\\cameras\\cam7\\c-1.png")}},
               "powerout" : {"0" : pyglet.image.load("images\\office\\powerout\\0.png"),
                             "1" : pyglet.image.load("images\\office\\powerout\\1.png"),
                             "2" : pyglet.image.load("images\\office\\powerout\\2.png")}}

pygame.mixer.init()

Sounds = {"ambience" : {"ambience" : pygame.mixer.Sound("sounds\\ambience\\ambience.wav"),
                        "ambience2" : pygame.mixer.Sound("sounds\\ambience\\ambience2.wav"),
                        "eerieambience" : pygame.mixer.Sound("sounds\\ambience\\eerieambience.wav"),
                        "fan" : pygame.mixer.Sound("sounds\\ambience\\fan.wav")},

          "camera" : {"blip" : pygame.mixer.Sound("sounds\\camera\\blip.wav"),
                      "camerasound" : pygame.mixer.Sound("sounds\\camera\\camerasound.wav"),
                      "camerasound2" : pygame.mixer.Sound("sounds\\camera\\camerasound2.wav"),
                      "computernoise" : pygame.mixer.Sound("sounds\\camera\\computernoise.wav"),
                      "deepsteps" : pygame.mixer.Sound("sounds\\camera\\deepsteps.wav"),
                      "garble" : pygame.mixer.Sound("sounds\\camera\\garble.wav"),
                      "garble2" : pygame.mixer.Sound("sounds\\camera\\garble2.wav"),
                      "garble3" : pygame.mixer.Sound("sounds\\camera\\garble3.wav"),
                      "piratesong" : pygame.mixer.Sound("sounds\\camera\\piratesong.wav"),
                      "pots" : pygame.mixer.Sound("sounds\\camera\\pots.wav"),
                      "pots2" : pygame.mixer.Sound("sounds\\camera\\pots2.wav"),
                      "pots3" : pygame.mixer.Sound("sounds\\camera\\pots3.wav"),
                      "pots4" : pygame.mixer.Sound("sounds\\camera\\pots4.wav"),
                      "putdown" : pygame.mixer.Sound("sounds\\camera\\putdown.wav"),
                      "run" : pygame.mixer.Sound("sounds\\camera\\run.wav"),
                      "runningfast" : pygame.mixer.Sound("sounds\\camera\\runningfast.wav"),
                      "static" : pygame.mixer.Sound("sounds\\camera\\static.wav"),
                      "static2" : pygame.mixer.Sound("sounds\\camera\\static2.wav"),
                      "static3" : pygame.mixer.Sound("sounds\\camera\\static3.wav")},

         "misc" : {"6AM" : pygame.mixer.Sound("sounds\\misc\\6AM.wav"),
                   "children" : pygame.mixer.Sound("sounds\\misc\\children.wav"),
                   "circus" : pygame.mixer.Sound("sounds\\misc\\circus.wav"),
                   "door" : pygame.mixer.Sound("sounds\\misc\\door.wav"),
                   "doorknocking" : pygame.mixer.Sound("sounds\\misc\\doorknocking.wav"),
                   "doorpounding" : pygame.mixer.Sound("sounds\\misc\\doorpounding.wav"),
                   "error" : pygame.mixer.Sound("sounds\\misc\\error.wav"),
                   "honk" : pygame.mixer.Sound("sounds\\misc\\honk.wav"),
                   "lighthum" : pygame.mixer.Sound("sounds\\misc\\lighthum.wav"),
                   "musicbox" : pygame.mixer.Sound("sounds\\misc\\musicbox.wav"),
                   "powerout" : pygame.mixer.Sound("sounds\\misc\\powerout.wav"),
                   "robotvoice" : pygame.mixer.Sound("sounds\\misc\\robotvoice.wav")},

         "scary" : {"breathing" : pygame.mixer.Sound("sounds\\scary\\breathing.wav"),
                    "breathing2" : pygame.mixer.Sound("sounds\\scary\\breathing2.wav"),
                    "breathing3" :    pygame.mixer.Sound("sounds\\scary\\breathing3.wav"),
                    "breathing4" : pygame.mixer.Sound("sounds\\scary\\breathing4.wav"),
                    "freddygiggle" : pygame.mixer.Sound("sounds\\scary\\freddygiggle.wav"),
                    "freddygiggle2" : pygame.mixer.Sound("sounds\\scary\\freddygiggle2.wav"),
                    "freddygiggle3" : pygame.mixer.Sound("sounds\\scary\\freddygiggle3.wav"),
                    "giggle" : pygame.mixer.Sound("sounds\\scary\\giggle.wav"),
                    "robotvoice" : pygame.mixer.Sound("sounds\\scary\\robotvoice.wav"),
                    "windowscare" : pygame.mixer.Sound("sounds\\scary\\windowscare.wav"),
                    "XSCREAM" : pygame.mixer.Sound("sounds\\scary\\XSCREAM.wav"),
                    "XSCREAM2" : pygame.mixer.Sound("sounds\\scary\\XSCREAM2.wav")}}

Cameras = {"cam1a" : "Stage Show",
           "cam1b" : "Dinning Area",
           "cam1c" : "Pirate Cove",
           "cam2a" : "West Hall",
           "cam2b" : "West Hall Corner",
           "cam3" : "Supply Room",
           "cam4a" : "East Hall",
           "cam4b" : "East Hall Corner",
           "cam5" : "Backstage",
           "cam6" : "Kitchen",
           "cam7" : "Restrooms"}

pygame.mixer.set_num_channels(31)

Channel = [pygame.mixer.Channel(i) for i in range(0, 31)]
