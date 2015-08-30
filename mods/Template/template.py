import pyDLASYIAS
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
from pyDLASYIAS.mods import Base
import pyDLASYIAS.gameObjects as gameObjects

IMAGE=pyDLASYIAS.assets.load("mods\\Template\\image.png")
TITLE = "Template mod"
DESCRIPTION = "Template mod that makes a label appear with the animatronics' location."
AUTHOR = "ZDDM"
ENABLED = True

class Mod(Base):
    '''Template mod that adds a label to the office with the location of the animatronics.'''
    def __init__(self, main_game):
        super().__init__(main_game)

    def setup(self):
        super().setup()
        self.label = cocos.text.Label(". . .", position=(40, 180), font_size=16, font_name="Fnaf UI")

        pyglet.clock.schedule(self.update)

    def on_office_setup(self, scene):
        scene.add(self.label, z=5)

    def on_camera_setup(self, scene):
        scene.add(self.label, z=5)

    def update(self, dt=0):
        self.label.element.text = "B: %s, R: %s, C: %s, F: %s" %(self.Game.bear.location, self.Game.rabbit.location, self.Game.chicken.location, self.Game.fox.status)
