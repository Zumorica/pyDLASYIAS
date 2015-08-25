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

class Base(object):
    def __init__(self, name, level, main_game):
        self.name = name
        self.level_base = level
        self.level_extra = 0
        self.level = self.level_base + self.level_extra
        self.kind = "generic"
        self.location = "cam1a"
        self.isOnCamera = False
        self.isActive = True
        self.Game = main_game

        pyglet.clock.schedule(self.update)

    def move(self, location, direct_move=False):
        if self.isActive:
            if isinstance(location, str):
                if direct_move:
                    self.change_static_opacity()
                    self.location = location
                    self.change_static_opacity()

                else:
                    if random.randint(1, 20) <= self.level:
                        self.change_static_opacity()
                        self.location = location
                        self.change_static_opacity()

            elif isinstance(location, list):
                if direct_move:
                    self.change_static_opacity()
                    self.location = random.choice(location)
                    self.change_static_opacity()

                else:
                    if random.randint(1, 20) <= self.level:
                        self.change_static_opacity()
                        self.location = random.choice(location)
                        self.change_static_opacity()

    def change_static_opacity(self, local=True):
        if local:
            if self.location == self.Game.camera.active_camera:
                self.Game.camera.static.opacity = 255
                pyglet.clock.schedule_once(self.Game.camera.static.get_random_opacity, random.randint(2, 5))
        else:
            self.Game.camera.static.opacity = 255
            pyglet.clock.schedule_once(self.Game.camera.static.get_random_opacity, random.randint(2, 5))

    def think(self, dt=0):
        if self.Game.hour >= 2:
            self.level_extra = 1

        self.level = self.level_base + self.level_extra

    def update(self, dt=0):
        if self.location == self.Game.camera.active_camera:
            self.isOnCamera = True

        else:
            self.isOnCamera = False

class Chicken(Base):
    def __init__(self, name, level, main_game):
        super().__init__(name, level, main_game)
        self.kind = "chicken"
        self.location = "cam1a"

        pyglet.clock.schedule_interval(self.think, 4)

    def think(self, dt=0):
        super().think(dt)
        if self.isActive and self.level > 0:
            if self.location == "cam1a":
                self.move("cam1b")

            elif self.location == "cam1b":
                self.move(["cam7", "cam6"])

            elif self.location == "cam4a":
                self.move(["cam1b", "cam4b"])

            elif self.location == "cam4b" and not self.isOnCamera:
                self.move(["cam4a", "right_door"])

            elif self.location == "cam6":
                self.move(["cam7", "cam4a"])
                if self.location != "cam6":
                    pyDLASYIAS.assets.Channel[11].set_volume(0.0)
                    pyDLASYIAS.assets.Channel[11].stop()

            elif self.location == "cam7":
                self.move(["cam6", "cam4a"])

            elif self.location == "right_door":
                if self.Game.office.right_button.door:
                    self.move(["cam1b", "right_door"])
                    if self.location != "right_door":
                        self.Game.right_discovered = False

                else:
                    self.move(["security_office", "right_door"])

            else:
                self.location == "cam1a"

class Rabbit(Base):
    def __init__(self, name, level, main_game):
        super().__init__(name, level, main_game)
        self.kind = "rabbit"
        self.location = "cam1a"

        pyglet.clock.schedule_interval(self.think, 4)

    def think(self, dt=0):
        super().think(dt)
        if self.isActive and self.level > 0:
            if self.location == "cam1a":
                self.move(["cam5", "cam1b"])

            elif self.location == "cam1b":
                self.move(["cam5", "cam2a"])

            elif self.location == "cam2a":
                if self.Game.fox.status == 4:
                    self.move("cam3", True)
                else:
                    self.move(["cam3", "cam2b"])

            elif self.location == "cam2b":
                if self.Game.fox.status == 4:
                    self.move("cam3", True)
                else:
                    self.move(["cam3", "left_door"])

            elif self.location == "cam3":
                if not self.Game.fox.status == 4:
                    self.move(["left_door", "cam2a"])

            elif self.location == "cam5":
                self.move(["cam1b", "cam2a"])

            elif self.location == "left_door":
                if self.Game.office.left_button.door:
                    self.move(["cam1b", "left_door"])
                    if self.location != "left_door":
                        self.Game.left_discovered = False

                else:
                    self.move(["security_office", "left_door"])

class Fox(Base):
    def __init__(self, name, level, main_game):
        super().__init__(name, level, main_game)
        self.kind = "fox"
        self.location = "cam1c"
        self.status = 0
        self.cooldown = False

        pyglet.clock.schedule_interval(self.think, 5)

    def think(self, dt=0):
        super().think(dt)
        if self.isActive and self.level > 0:
            if self.status < 3 and not self.isOnCamera and self.level != 0 and not self.cooldown:
                if random.randint(0, 20) <= self.level:
                    self.status += 1

            elif self.status == 3 and (self.Game.camera.active_camera == "cam2a" or random.randint(0, 20) <= self.level):
                self.status = 4

            elif self.status == 4 and self.Game.camera.active_camera != "cam2a" \
                                  and random.randint(0, 20) <= self.level \
                                  and self.Game.animatronics["Rabbit"].location not in ["cam2a", "cam2b", "left_door"]:
                self.status == 5

class Bear(Base):
    def __init__(self, name, level, main_game):
        super().__init__(name, level, main_game)
        self.kind = "bear"
        self.location = "cam1a"

        pyglet.clock.schedule_interval(self.think, 3)

    def move(self, location, direct_move=False):
        if self.location == "cam1a":
            pyDLASYIAS.assets.Channel[30].set_volume(0.2, 0.2)
        if self.location == "cam1b":
            pyDLASYIAS.assets.Channel[30].set_volume(0.3, 0.3)
        if self.location == "cam7":
            pyDLASYIAS.assets.Channel[30].set_volume(0.3, 0.5)
        if self.location == "cam6":
            pyDLASYIAS.assets.Channel[30].set_volume(0.4, 0.6)
        if self.location == "cam4a":
            pyDLASYIAS.assets.Channel[30].set_volume(0.45, 0.65)
        if self.location == "cam4b":
            pyDLASYIAS.assets.Channel[30].set_volume(0.3, 0.7)

        pyDLASYIAS.assets.Channel[30].play(random.choice([pyDLASYIAS.assets.Sounds["scary"]["freddygiggle"], pyDLASYIAS.assets.Sounds["scary"]["freddygiggle2"], pyDLASYIAS.assets.Sounds["scary"]["freddygiggle3"]]))

        if self.isActive:
            if isinstance(location, str):
                if direct_move:
                    self.change_static_opacity()
                    self.location = location
                    self.change_static_opacity()

                else:
                    if random.randint(1, 20) <= self.level:
                        self.change_static_opacity()
                        self.location = location
                        self.change_static_opacity()

            elif isinstance(location, list):
                if direct_move:
                    self.change_static_opacity()
                    self.location = random.choice(location)
                    self.change_static_opacity()

                else:
                    if random.randint(1, 20) <= self.level:
                        self.change_static_opacity()
                        self.location = random.choice(location)
                        self.change_static_opacity()

    def think(self, dt=0):
        super().think(dt)
        if self.isActive and self.level > 0:
            if self.Game.hour >= 2:
                self.level_extra = 1

            self.level = self.level_base + self.level_extra

            if self.level > 4:
                if self.location == "cam1a" and self.Game.animatronics["Rabbit"].location != "cam1a" \
                                            and self.Game.animatronics["Chicken"].location != "cam1a" and (not self.isOnCamera and random.randint(0, 1)):
                    self.move("cam1b")

                elif self.location == "cam1b" and self.Game.animatronics["Rabbit"].location != "cam1b" \
                                              and self.Game.animatronics["Chicken"].location != "cam1b" and not self.isOnCamera:
                    self.move("cam7")

                elif self.location == "cam7" and self.Game.animatronics["Rabbit"].location != "cam7" \
                                             and self.Game.animatronics["Chicken"].location != "cam7" and not self.isOnCamera:
                    self.move("cam6")

                elif self.location == "cam6" and self.Game.animatronics["Rabbit"].location != "cam6" \
                                             and self.Game.animatronics["Chicken"].location != "cam6" and not self.isOnCamera:
                    self.move("cam4a")

                elif self.location == "cam4a" and self.Game.animatronics["Rabbit"].location != "cam4a" \
                                              and self.Game.animatronics["Chicken"].location != "cam4a" and not self.isOnCamera:
                    self.move("cam4b")

                elif self.location == "cam4b" and self.Game.animatronics["Rabbit"].location != "cam1a" \
                                              and self.Game.animatronics["Chicken"].location != "cam1a"  \
                                              and not self.isOnCamera and not self.Game.office.right_button.door:
                    self.move(["security_office", "cam4a"])
