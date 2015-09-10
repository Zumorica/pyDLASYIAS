import pyDLASYIAS
import cocos
import pyglet
import pygame.mixer
import pickle
import random
import cocos
import time
import sys
import os
from pyglet.gl import *
from pyglet.gl.glu import *
from cocos.director import director
from cocos.scenes import *
import pyDLASYIAS.gameObjects as gameObjects

class Base(object):
    def __init__(self):
        self.kind = "generic"
        self.event = None

    def get_pickled(self):
        return pickle.dumps(self)

class Guard(Base):
    def __init__(self, name="Victim", left_door=False, left_light=False, right_door=False, right_light=False, last_cam="cam1a", scene="office", usage=1):
        self.name = name
        self.kind = "guard"
        self.event = "character_update"
        self.left_door = left_door
        self.left_light = left_light
        self.right_door = right_door
        self.right_light = right_light
        self.last_cam = last_cam
        self.scene = scene
        self.usage = usage

class Animatronic(Base):
    def __init__(self, name="Endoskeleton"):
        self.name = name
        self.kind = "generic"
        self.event = "character_update"
        self.location = "cam1a"
        self.isOnCamera = False
        self.status = 0

    def change_static_opacity(self, local=True):
        if local:
            if self.location == self.Game.camera.active_camera:
                self.Game.camera.static.opacity = 255
                pyglet.clock.schedule_once(self.Game.camera.static.get_random_opacity, random.randint(2, 5))
        else:
            self.Game.camera.static.opacity = 255
            pyglet.clock.schedule_once(self.Game.camera.static.get_random_opacity, random.randint(2, 5))

class Chicken(Animatronic):
    def __init__(self, name="Chicken"):
        super().__init__(name)
        self.kind = "chicken"

class Rabbit(Animatronic):
    def __init__(self, name="Rabbit"):
        super().__init__(name)
        self.kind = "rabbit"

class Bear(Animatronic):
    def __init__(self, name="Bear"):
        super().__init__(name)
        self.kind = "bear"

class Fox(Animatronic):
    def __init__(self, name="Fox"):
        super().__init__(name)
        self.kind = "fox"

class Night_State(Base):
    def __init__(self, power, hour):
        self.name = "no_name"
        self.kind = "night_state"
        self.power = power
        self.hour = hour

class Event(Base):
    def __init__(self, event, event_2=None):
        self.name = "no_name"
        self.kind = "event"
        self.event = event
        self.event_2 = event_2
