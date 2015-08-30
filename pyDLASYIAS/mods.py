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
import pyDLASYIAS.gameObjects as gameObjects

class Base(object):
    def __init__(self, main_game):
        self.Game = main_game

        director.window.push_handlers(self)

        self.setup()

    def on_hour_advance(self, dt=0):
        pass

    def on_power_calculation(self, dt=0):
        pass

    def on_office_setup(self, scene):
        pass

    def on_office_update_begin(self, dt=0):
        pass

    def on_office_update_end(self, dt=0):
        pass

    def on_office_enter(self):
        pass

    def on_office_exit(self):
        pass


    def on_camera_setup(self, scene):
        pass

    def on_camera_update_begin(self, dt=0):
        pass

    def on_camera_update_end(self, dt=0):
        pass

    def on_camera_enter(self):
        pass

    def on_camera_exit(self):
        pass


    def on_powerout_setup(self, scene):
        pass

    def on_powerout_update_begin(self, dt=0):
        pass

    def on_powerout_update_end(self, dt=0):
        pass

    def on_powerout_enter(self):
        pass

    def on_powerout_exit(self):
        pass

    def on_powerout_stage_2(self, dt=0):
        pass

    def on_powerout_stage_3(self, dt=0):
        pass

    def on_powerout_stage_4(self, dt=0):
        pass


    def on_scarejump_setup(self, scene):
        pass

    def on_scarejump_update_begin(self, dt=0):
        pass

    def on_scarejump_update_end(self, dt=0):
        pass

    def on_scarejump_enter(self):
        pass

    def on_scarejump_exit(self):
        pass

    def on_scarejump_static(self, dt=0):
        pass


    def on_stuffed_setup(self, scene):
        pass

    def on_stuffed_update_begin(self, dt=0):
        pass

    def on_stuffed_update_end(self, dt=0):
        pass

    def on_stuffed_enter(self):
        pass

    def on_stuffed_exit(self):
        pass


    def on_night_end_setup(self, scene):
        pass

    def on_night_end_update_begin(self, dt=0):
        pass

    def on_night_end_update_end(self, dt=0):
        pass

    def on_night_end_enter(self):
        pass

    def on_night_end_exit(self):
        pass

    def on_night_end_stage_2(self, dt=0):
        pass

    def on_night_end_stage_3(self, dt=0):
        pass


    def on_ending_setup(self, scene):
        pass

    def on_ending_update_begin(self, dt=0):
        pass

    def on_ending_update_end(self, dt=0):
        pass

    def on_ending_enter(self):
        pass

    def on_ending_exit(self):
        pass

    def setup(self):
        pass
