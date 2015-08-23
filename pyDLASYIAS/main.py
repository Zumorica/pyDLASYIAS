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
import pyDLASYIAS.gameObjects as gameObjects

class Main(object):
    def __init__(self, power=1, hour=0, hours_to_seconds=86, night="pyDLASYIAS"):

        self.usage = 1
        self.power = power
        self.hour = hour
        self.night = night

        self.window = director.window
        self.office = pyDLASYIAS.scenes.Office(self)
        self.camera = pyDLASYIAS.scenes.Camera(self)
        self.powerout = pyDLASYIAS.scenes.Powerout(self)
        self.scarejump = pyDLASYIAS.scenes.Scarejump(self)

        self.bear = pyDLASYIAS.animatronics.Bear("Bear", 1, self)
        self.rabbit = pyDLASYIAS.animatronics.Rabbit("Rabbit", 20, self)
        self.chicken = pyDLASYIAS.animatronics.Chicken("Chicken", 20, self)
        self.fox = pyDLASYIAS.animatronics.Fox("Fox", 1, self)

        self.animatronics = {"Bear" : self.bear,
                             "Rabbit" : self.rabbit,
                             "Chicken" : self.chicken,
                             "Fox" : self.fox}

        self.power_calculations()
        pyglet.clock.schedule_interval(self.next_hour, hours_to_seconds)

        director.run(self.office)

    def power_calculations(self, dt=0, old_usage=1):
        if self.power >= 0:
            if self.usage == 1:
                if old_usage == 1:
                    self.power -= 1

                if old_usage >= 2:
                    self.power -= 2

                pyglet.clock.schedule_once(self.power_calculations, 9.6, old_usage=1)

            if self.usage == 2:
                if old_usage == 1:
                    self.power -= 1

                if old_usage == 2:
                    self.power -= 1

                if old_usage >= 3:
                    self.power -= 2

                pyglet.clock.schedule_once(self.power_calculations, 4.8, old_usage=2)

            if self.usage == 3:
                if old_usage == 1:
                    self.power -= 1

                if old_usage == 2:
                    self.power -= 1

                if old_usage == 3:
                    self.power -= 1

                if old_usage == 4:
                    self.power -= 2

                pyglet.clock.schedule_once(self.power_calculations, random.choice([2.8, 2.9, 3.9]), old_usage=3)

            if self.usage == 4:
                self.power -= 1

                pyglet.clock.schedule_once(self.power_calculations, random.choice([1.9, 2.9]), old_usage=4)

            if self.usage == 5:
                self.usage = 4
                self.power -= 1

                pyglet.clock.schedule_once(self.power_calculations, random.choice([1.9, 2.9]), old_usage=4)

    def next_hour(self, dt=0):
        if self.hour != 6:
            self.hour += 1
