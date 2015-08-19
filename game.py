'''To-Do launcher.'''
import pyDLASYIAS
import cocos
import pyglet
import random
import cocos
import time
import sys
import os
from pyglet.gl import *
from pyglet.gl.glu import *
from cocos.director import director
import pyDLASYIAS.gameObjects as gameObjects

sys.setrecursionlimit(10000)

director.init(autoscale=True, audio_backend="sdl", \
              audio=None, fullscreen=False, \
              resizable=True, vsync=True, width=1280,
              height=720, caption="pyDLASYIAS", \
              visible=True)
director.set_depth_test(True)

pyDLASYIAS.main.Main()
