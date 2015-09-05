import cocos
import pyglet
import pygame.mixer
import platform
import random
import cocos
import time
import sys
import os
from pyglet.gl import *
from pyglet.gl.glu import *
from cocos.director import director
from cocos.scenes import *

__all__ = ['Backgrounds', 'Sounds', 'Cameras', 'Channel', 'load']

def load(filename):
    if filename.endswith(".png"):
        if platform.system() == "Windows":
            return pyglet.image.load(filename)

        else:
            filename = filename.replace("\\", "/")
            return pyglet.image.load(filename)

    elif filename.endswith(".wav"):
        if platform.system() == "Windows":
            return pygame.mixer.Sound(filename)

        else:
            filename = filename.replace("\\", "/")
            return pygame.mixer.Sound(filename)

    else:
        raise ValueError("filename is neither a png or a wav")

Backgrounds = {"office" : {"0" : load("images\\office\\0.png"),
                                       "1" : load("images\\office\\1.png"),
                                       "2" : load("images\\office\\2.png"),
                                       "r" : load("images\\office\\r.png"),
                                       "c" : load("images\\office\\c.png")},
               "camera" : {"cam1a" : {"0" : load("images\\cameras\\cam1a\\0.png"),
                                                  "b" : load("images\\cameras\\cam1a\\b.png"),
                                                  "b-1" : load("images\\cameras\\cam1a\\b-1.png"),
                                                  "bc" : load("images\\cameras\\cam1a\\bc.png"),
                                                  "br" : load("images\\cameras\\cam1a\\br.png"),
                                                  "brc" : load("images\\cameras\\cam1a\\brc.png"),
                                                  "brc-1" : load("images\\cameras\\cam1a\\brc-1.png")},
                           "cam1b" : {"0" : load("images\\cameras\\cam1b\\0.png"),
                                            "b" : load("images\\cameras\\cam1b\\b.png"),
                                            "c" : load("images\\cameras\\cam1b\\c.png"),
                                            "c-1" : load("images\\cameras\\cam1b\\c-1.png"),
                                            "r" : load("images\\cameras\\cam1b\\r.png"),
                                            "r-1" : load("images\\cameras\\cam1b\\r-1.png")},
                           "cam1c" : {"0" : load("images\\cameras\\cam1c\\0.png"),
                                           "1" : load("images\\cameras\\cam1c\\1.png"),
                                           "2" : load("images\\cameras\\cam1c\\2.png"),
                                           "3" : load("images\\cameras\\cam1c\\3.png"),
                                           "4" : load("images\\cameras\\cam1c\\4.png"),
                                           "5" : load("images\\cameras\\cam1c\\5.png")},
                           "cam2a" : {"0" : load("images\\cameras\\cam2a\\0.png"),
                                            "1" : load("images\\cameras\\cam2a\\1.png"),
                                            "r" : load("images\\cameras\\cam2a\\r.png")},
                           "cam2b" : {"0" : load("images\\cameras\\cam2b\\0.png"),
                                            "1" : load("images\\cameras\\cam2b\\1.png"),
                                            "2" : load("images\\cameras\\cam2b\\2.png"),
                                            "r" : load("images\\cameras\\cam2b\\r.png"),
                                            "r-1" : load("images\\cameras\\cam2b\\r-1.png")},
                           "cam3" : {"0" : load("images\\cameras\\cam3\\0.png"),
                                          "r" : load("images\\cameras\\cam3\\r.png")},
                           "cam4a" : {"0" : load("images\\cameras\\cam4a\\0.png"),
                                            "1" : load("images\\cameras\\cam4a\\1.png"),
                                            "2" : load("images\\cameras\\cam4a\\2.png"),
                                            "b" : load("images\\cameras\\cam4a\\b.png"),
                                            "c" : load("images\\cameras\\cam4a\\c.png"),
                                            "c-1" : load("images\\cameras\\cam4a\\c-1.png")},
                           "cam4b" : {"0" : load("images\\cameras\\cam4b\\0.png"),
                                            "1" : load("images\\cameras\\cam4b\\1.png"),
                                            "2" : load("images\\cameras\\cam4b\\2.png"),
                                            "3" : load("images\\cameras\\cam4b\\3.png"),
                                            "4" : load("images\\cameras\\cam4b\\4.png"),
                                            "b" : load("images\\cameras\\cam4b\\b.png"),
                                            "c" : load("images\\cameras\\cam4b\\c.png"),
                                            "c-1" : load("images\\cameras\\cam4b\\c-1.png"),
                                            "c-2" : load("images\\cameras\\cam4b\\c-2.png")},
                           "cam5" : {"0" : load("images\\cameras\\cam5\\0.png"),
                                          "1" : load("images\\cameras\\cam5\\1.png"),
                                          "r" : load("images\\cameras\\cam5\\r.png"),
                                          "r-1" : load("images\\cameras\\cam5\\r-1.png")},
                           "cam6" : {"0" : load("images\\cameras\\misc\\black.png")},
                           "cam7" : {"0" : load("images\\cameras\\cam7\\0.png"),
                                          "c" : load("images\\cameras\\cam7\\c.png"),
                                          "b" : load("images\\cameras\\cam7\\b.png"),
                                          "c-1" : load("images\\cameras\\cam7\\c-1.png")}},
               "powerout" : {"0" : load("images\\office\\powerout\\0.png"),
                                   "1" : load("images\\office\\powerout\\1.png"),
                                   "2" : load("images\\office\\powerout\\2.png")}}

pygame.mixer.init()

Sounds = {"ambience" : {"ambience" : load("sounds\\ambience\\ambience.wav"),
                                     "ambience2" : load("sounds\\ambience\\ambience2.wav"),
                                     "eerieambience" : load("sounds\\ambience\\eerieambience.wav"),
                                     "fan" : load("sounds\\ambience\\fan.wav")},

                  "camera" : {"blip" : load("sounds\\camera\\blip.wav"),
                                    "camerasound" : load("sounds\\camera\\camerasound.wav"),
                                    "camerasound2" : load("sounds\\camera\\camerasound2.wav"),
                                    "computernoise" : load("sounds\\camera\\computernoise.wav"),
                                    "deepsteps" : load("sounds\\camera\\deepsteps.wav"),
                                    "garble" : load("sounds\\camera\\garble.wav"),
                                    "garble2" : load("sounds\\camera\\garble2.wav"),
                                    "garble3" : load("sounds\\camera\\garble3.wav"),
                                    "piratesong" : load("sounds\\camera\\piratesong.wav"),
                                    "pots" : load("sounds\\camera\\pots.wav"),
                                    "pots2" : load("sounds\\camera\\pots2.wav"),
                                    "pots3" : load("sounds\\camera\\pots3.wav"),
                                    "pots4" : load("sounds\\camera\\pots4.wav"),
                                    "putdown" : load("sounds\\camera\\putdown.wav"),
                                    "run" : load("sounds\\camera\\run.wav"),
                                    "runningfast" : load("sounds\\camera\\runningfast.wav"),
                                    "static" : load("sounds\\camera\\static.wav"),
                                    "static2" : load("sounds\\camera\\static2.wav"),
                                    "static3" : load("sounds\\camera\\static3.wav")},

                 "misc" : {"6AM" : load("sounds\\misc\\6AM.wav"),
                               "children" : load("sounds\\misc\\children.wav"),
                               "circus" : load("sounds\\misc\\circus.wav"),
                               "door" : load("sounds\\misc\\door.wav"),
                               "doorknocking" : load("sounds\\misc\\doorknocking.wav"),
                               "doorpounding" : load("sounds\\misc\\doorpounding.wav"),
                               "error" : load("sounds\\misc\\error.wav"),
                               "honk" : load("sounds\\misc\\honk.wav"),
                               "lighthum" : load("sounds\\misc\\lighthum.wav"),
                               "musicbox" : load("sounds\\misc\\musicbox.wav"),
                               "powerout" : load("sounds\\misc\\powerout.wav"),
                               "robotvoice" : load("sounds\\misc\\robotvoice.wav")},

                 "scary" : {"breathing" : load("sounds\\scary\\breathing.wav"),
                                "breathing2" : load("sounds\\scary\\breathing2.wav"),
                                "breathing3" :    load("sounds\\scary\\breathing3.wav"),
                                "breathing4" : load("sounds\\scary\\breathing4.wav"),
                                "freddygiggle" : load("sounds\\scary\\freddygiggle.wav"),
                                "freddygiggle2" : load("sounds\\scary\\freddygiggle2.wav"),
                                "freddygiggle3" : load("sounds\\scary\\freddygiggle3.wav"),
                                "giggle" : load("sounds\\scary\\giggle.wav"),
                                "robotvoice" : load("sounds\\scary\\robotvoice.wav"),
                                "windowscare" : load("sounds\\scary\\windowscare.wav"),
                                "XSCREAM" : load("sounds\\scary\\XSCREAM.wav"),
                                "XSCREAM2" : load("sounds\\scary\\XSCREAM2.wav")}}

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
                   "cam7" : "Restrooms",
                   "left_door" : "West Hall Blind Spot",
                   "right_door" : "East Hall Blind Spot",
                   "inside" : "security_office"}

pygame.mixer.set_num_channels(31)

Channel = [pygame.mixer.Channel(i) for i in range(0, 31)]
