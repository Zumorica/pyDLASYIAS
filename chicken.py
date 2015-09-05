#!/usr/bin/env python3
import glob
import importlib
import threading
import socket
import cocos
import pyglet
import socket
import pygame.mixer
import platform
import random
import cocos
import time
import sys
import os
from pyglet.gl import *
from pyglet.gl.glu import *
from pyglet.window import key
from cocos.director import director
from cocos.scenes import *

sys.setrecursionlimit(25000)

import pyDLASYIAS
import pyDLASYIAS.gameObjects as gameObjects

pyglet.font.add_file('FNAF.ttf')

director.init(autoscale=True, audio_backend="sdl", \
              audio=None, fullscreen=False, \
              resizable=False, vsync=True, width=1280,
              height=720, caption="pyDLASYIAS", \
              visible=True)

pyDLASYIAS.networking.Chicken_Main(None, ("localhost", 9999))
