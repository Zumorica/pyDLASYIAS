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

class Intro(pyDLASYIAS.scenes.Base):
    def __init__(self):
        super().__init__(None)

        self.setup()

    def setup(self):

        self.Frames = [pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\newspaper-0.png"), 1),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\newspaper-0.png"), 0.35),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\b-1.png"), 0.35),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\itsme-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\itsme-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\b-0.png"), 0.50),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\crying-0.png"), 0.10),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\stage-0.png"), 0.15),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\stage-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\r-0.png"), 0.15),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\r-0.png"), 0.07),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\r-1.png"), 0.04),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\newspaper-1.png"), 0.10),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\newspaper-2.png"), 0.10),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\newspaper-3.png"), 0.10),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\c-0.png"), 0.15),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\itsme-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\itsme-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\gbear-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\itsme-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\crying-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-0.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\stuffed.png"), 0.35),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\stuffed.png"), 0.17),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\b-2.png"), 0.08),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\b-5.png"), 0.25),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\stuffed.png"), 0.14),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-0.png"), 0.06),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.06),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.06),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.05),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.06),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-6.png"), 0.06),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-7.png"), 0.07),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-0.png"), 0.08),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-1.png"), 0.09),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-2.png"), 0.10),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-3.png"), 0.11),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-4.png"), 0.12),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\intro\\static-5.png"), 0.13),
                       pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\cameras\\misc\\black.png"), None)]

        self.animation = pyglet.image.Animation(self.Frames)

    def on_enter(self):
        super().on_enter()
        pyDLASYIAS.assets.Channel[30].play(pyDLASYIAS.assets.Sounds["misc"]["musicbox"], 0)
        pyDLASYIAS.assets.Channel[30].fadeout(10000)

        self.sprite = cocos.sprite.Sprite(self.animation, anchor=(0,0))

        self.add(self.sprite, z=0)

        director.window.push_handlers(self)

    def on_exit(self):
        super().on_exit()

        pygame.mixer.stop()
        director.window.remove_handlers(self)

    def on_mouse_press(self, x, y, button, mod):
        pyglet.clock.unschedule(self.update)
        director.run(Main_Menu())

    def on_key_press(self, symbol, mod):
        pyglet.clock.unschedule(self.update)
        director.run(Main_Menu())

    def update(self, dt=0):
        super().update(dt)

        if not pyDLASYIAS.assets.Channel[30].get_busy():
            pyglet.clock.unschedule(self.update)
            director.run(main_menu)

class Main_Menu(pyDLASYIAS.scenes.Base):
    def __init__(self):
        super().__init__(None)

        self.setup()

    def setup(self):
        self.static = gameObjects.Static(87, 120)
        self.background = gameObjects.Base("images\\intro\\b-0.png", (0,0))
        self.custom_night = Menu_Item("Custom Night", position=(40, 128), callback=self.enter_custom_night, font_size=16, font_name="Fnaf UI")
        self.mod_list = Menu_Item("Mods", position=(40, 172), callback=self.enter_mods_list, font_size = 16, font_name="Fnaf UI")
        self.online_menu = Menu_Item("Online multiplayer", position=(40, 84), callback=self.enter_online_menu, font_size=16, font_name="Fnaf UI")

        self.add(self.static, z=1)
        self.add(self.background, z=0)
        self.add(self.custom_night, z=2)
        self.add(self.online_menu, z=2)
        self.add(self.mod_list, z=2)
        self.add(Menu_Title(position=(32, director.window.height - 64), font_size=32, font_name="Fnaf UI"))

    def enter_online_menu(self):
        director_run(Connect_Client())

    def enter_custom_night(self):
        director.run(custom_night)

    def enter_mods_list(self):
        director.run(mod_list)

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self)

    def update(self, dt=0):
        super().update(dt)
        director.window.remove_handlers(self)

class Menu_Item(cocos.text.Label):
    def __init__(self, text='', position=(0, 0), callback=None, rect=None, **kwargs):
        super().__init__(text, position, **kwargs)
        if rect == None:
            self.rect = cocos.rect.Rect(position[0], position[1], self.element.content_width, self.element.content_height)
        else:
            self.rect = rect

        self.callback = callback

        self.isSelected = False

    def no_callback(self):
        pass

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self)

    def on_exit(self):
        super().on_exit()
        director.window.remove_handlers(self)

    def on_mouse_press(self, x, y, button, mod):
        if self.rect.contains(x, y) and button == 1 and self.visible:
            if self.callback == None:
                self.no_callback()
            else:
                self.callback()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.rect.contains(x, y) and not self.isSelected and not self.element.text.startswith(">"):
            self.isSelected = True
            self.element.text = ">%s" %(self.element.text)
            if self.visible:
                pyDLASYIAS.assets.Sounds["camera"]["blip"].play(0)
        elif self.element.text.startswith(">") and not self.rect.contains(x, y):
            self.element.text = self.element.text[1:]
            self.isSelected = False

class Menu_Title(cocos.text.Label):
    def __init__(self, position=(0, 0), **kwargs):
        super().__init__(">pyDLASYIAS", position, **kwargs)
        self.rect = cocos.rect.Rect(self.position[0], self.position[1], self.element.content_width, self.element.content_height)
        self.isSelected = False

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self)

    def on_exit(self):
        super().on_exit()
        director.window.remove_handlers(self)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.rect.contains(x, y) and not self.isSelected and not self.element.text == ">pyDontLetAnimatronicsStuffYouIntoASuit":
            self.isSelected = True
            self.element.text = ">pyDontLetAnimatronicsStuffYouIntoASuit"
            self.rect = cocos.rect.Rect(self.position[0], self.position[1], self.element.content_width, self.element.content_height)
        elif self.element.text == ">pyDontLetAnimatronicsStuffYouIntoASuit" and not self.rect.contains(x, y):
            self.element.text = ">pyDLASYIAS"
            self.rect = cocos.rect.Rect(self.position[0], self.position[1], self.element.content_width, self.element.content_height)
            self.isSelected = False

class Custom_Night(pyDLASYIAS.scenes.Base):
    def __init__(self):
        super().__init__(None)

        self.setup()

    def go_back(self):
        director.run(main_menu)

    def setup(self):
        self.add(cocos.layer.util_layers.ColorLayer(0, 0, 0, 255), z=0)

        self.power = 100
        self.hour = 0
        self.bear_level = 0
        self.rabbit_level = 0
        self.chicken_level = 0
        self.fox_level = 0
        self.mods = False

        self.label_custom = cocos.text.Label("Custom Night", (64, 624), font_size=32, font_name="Fnaf UI", bold=True)

        self.label_bear_level = cocos.text.Label(str(self.bear_level), (227, 255), font_size=24, font_name="Fnaf UI")
        self.label_rabbit_level = cocos.text.Label(str(self.rabbit_level), (510, 255), font_size=24, font_name="Fnaf UI")
        self.label_chicken_level = cocos.text.Label(str(self.chicken_level), (792, 255), font_size=24, font_name="Fnaf UI")
        self.label_fox_level = cocos.text.Label(str(self.fox_level), (1072, 255), font_size=24, font_name="Fnaf UI")

        self.bear_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\b.png"), (128, 346), anchor=(0,0))
        self.rabbit_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\r.png"), (413, 346), anchor=(0,0))
        self.chicken_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\c.png"), (692, 346), anchor=(0,0))
        self.fox_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\f.png"), (967, 346), anchor=(0,0))

        self.button_left_bear = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\0.png"), (122,250), anchor=(0,0))
        self.button_right_bear = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\1.png"), (311,250), anchor=(0,0))

        self.button_left_rabbit = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\0.png"), (406,250), anchor=(0,0))
        self.button_right_rabbit = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\1.png"), (593,250), anchor=(0,0))

        self.button_left_chicken = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\0.png"), (690,250), anchor=(0,0))
        self.button_right_chicken = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\1.png"), (876,250), anchor=(0,0))

        self.button_left_fox = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\0.png"), (969,250), anchor=(0,0))
        self.button_right_fox = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\1.png"), (1154,250), anchor=(0,0))

        self.button_left_time = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\0.png"), (122, 110), anchor=(0,0))
        self.button_right_time = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\1.png"), (311, 110), anchor=(0,0))
        self.label_time = cocos.text.Label(str(self.hour), (227, 125), font_size=24, font_name="Fnaf UI")
        self.label_time_title = cocos.text.Label("Hour", (122, 175), font_size=28, font_name="Fnaf UI", bold=True)

        self.button_left_power = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\0.png"), (406, 110), anchor=(0,0))
        self.button_right_power = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\1.png"), (593, 110), anchor=(0,0))
        self.label_power = cocos.text.Label(str(self.power), (510, 125), font_size=24, font_name="Fnaf UI")
        self.label_power_title = cocos.text.Label("Power", (406, 175), font_size=28, font_name="Fnaf UI", bold=True)

        self.button_left_mod = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\0.png"), (690, 110), anchor=(0,0))
        self.button_right_mod = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\1.png"), (876, 110), anchor=(0,0))
        self.label_mod_title = cocos.text.Label("Enable Mods", (690, 175), font_size=28, font_name="Fnaf UI", bold=True)
        self.label_mods = cocos.text.Label(str(self.mods), (792, 125), font_size=18, font_name="Fnaf UI")

        self.button_ready = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\buttons\\2.png"), (1044, 117), anchor=(0,0))
        self.back = Menu_Item("Back", (16, 16), self.go_back, font_size=16, font_name="Fnaf UI")

        self.add(self.label_custom, z=1)
        self.add(self.label_power_title, z=1)
        self.add(self.label_time_title, z=1)
        self.add(self.label_bear_level, z=1)
        self.add(self.label_rabbit_level, z=1)
        self.add(self.label_chicken_level, z=1)
        self.add(self.label_fox_level, z=1)
        self.add(self.bear_sprite, z=1)
        self.add(self.rabbit_sprite, z=1)
        self.add(self.chicken_sprite, z=1)
        self.add(self.fox_sprite, z=1)
        self.add(self.button_left_bear, z=1)
        self.add(self.button_right_bear, z=1)
        self.add(self.button_left_rabbit, z=1)
        self.add(self.button_right_rabbit, z=1)
        self.add(self.button_left_chicken, z=1)
        self.add(self.button_right_chicken, z=1)
        self.add(self.button_left_fox, z=1)
        self.add(self.label_time, z=1)
        self.add(self.button_left_power, z=1)
        self.add(self.button_right_power, z=1)
        self.add(self.button_left_mod, z=1)
        self.add(self.button_right_mod, z=1)
        self.add(self.label_mod_title, z=1)
        self.add(self.label_mods, z=1)
        self.add(self.label_power, z=1)
        self.add(self.button_ready, z=1)
        self.add(self.back, z=1)

    def on_enter(self):
        super().on_enter()

        self.power = 100
        self.hour = 0
        self.bear_level = 0
        self.rabbit_level = 0
        self.chicken_level = 0
        self.fox_level = 0

    def on_exit(self):
        super().on_exit()

    def on_mouse_press(self, x, y, button, mod):
        if self.button_left_time.contains(x, y):
            if self.hour != 0:
                self.hour -= 1

        if self.button_right_time.contains(x, y):
            if self.hour != 6:
                self.hour += 1

        if self.button_left_power.contains(x, y):
            if self.power != 0:
                self.power -= 1

        if self.button_right_power.contains(x, y):
            if self.power != 999:
                self.power += 1

        if self.button_left_bear.contains(x, y):
            if self.bear_level != 0:
                self.bear_level -= 1

        if self.button_right_bear.contains(x, y):
            if self.bear_level != 20:
                self.bear_level += 1

        if self.button_left_rabbit.contains(x, y):
            if self.rabbit_level != 0:
                self.rabbit_level -= 1

        if self.button_right_rabbit.contains(x, y):
            if self.rabbit_level != 20:
                self.rabbit_level += 1

        if self.button_left_chicken.contains(x, y):
            if self.chicken_level != 0:
                self.chicken_level -= 1

        if self.button_right_chicken.contains(x, y):
            if self.chicken_level != 20:
                self.chicken_level += 1

        if self.button_left_fox.contains(x, y):
            if self.fox_level != 0:
                self.fox_level -= 1

        if self.button_right_fox.contains(x, y):
            if self.fox_level != 20:
                self.fox_level += 1

        if self.button_left_mod.contains(x, y):
            if self.mods:
                self.mods = False

        if self.button_right_mod.contains(x, y):
            if not self.mods:
                self.mods = True

        if self.button_ready.contains(x, y):
            global mods
            if not self.mods:
                mods = []
            else:
                mods = mods

            self.Game = pyDLASYIAS.main.Main(power=self.power, hour=self.hour, \
                                                                        night="Custom Night", ending="custom", \
                                                                        bear_level = self.bear_level, \
                                                                        rabbit_level = self.rabbit_level, \
                                                                        chicken_level = self.chicken_level, \
                                                                        fox_level = self.fox_level, menu=main_menu, mods=mods)

    def update(self, dt=0):
        super().update(dt)
        self.label_power.element.text = str(self.power)
        self.label_time.element.text = str(self.hour)
        self.label_bear_level.element.text = str(self.bear_level)
        self.label_rabbit_level.element.text = str(self.rabbit_level)
        self.label_chicken_level.element.text = str(self.chicken_level)
        self.label_fox_level.element.text = str(self.fox_level)
        self.label_mods.element.text = str(self.mods)

class Mod_List(pyDLASYIAS.scenes.Base):
    def __init__(self):
        super().__init__(None)

        self.setup()

    def go_back(self):
        director.run(main_menu)

    def setup(self):
        self.page = 0
        self.mods = mods
        self.mod_list = []
        self.active_list = cocos.cocosnode.CocosNode()
        self.back = Menu_Item("Back", (16, 16), self.go_back, font_size=16, font_name="Fnaf UI")
        self.next = Menu_Item("Next", (272, 16), self.on_next_page, font_size=16, font_name="Fnaf UI")
        self.previous = Menu_Item("Previous", (128, 16), self.on_previous_page, font_size=16, font_name="Fnaf UI")
        self.page_label = cocos.text.Label("Page %s / %s" %(self.page, len(self.mods) // 2), (512, 16), font_size=16, font_name="Fnaf UI")


        for num, mod in enumerate(self.mods):
            if num % 2 == 0:
                self.mod_list.append(Mod_Listed(mod, (64, director.window.height - 264)))
            else:
                self.mod_list.append(Mod_Listed(mod, (64, 128)))

        self.add(self.active_list, z=2)
        self.add(cocos.layer.util_layers.ColorLayer(0, 0, 0, 255), z=0)
        self.add(gameObjects.Static(), z=1)
        self.add(self.back, z=2)
        self.add(self.next, z=2)
        self.add(self.previous, z=2)
        self.add(self.page_label, z=2)

        self.active_list.add(self.mod_list[self.page * 2])
        try:
            self.active_list.add(self.mod_list[(self.page * 2) + 1])
        except IndexError:
            pass

    def on_next_page(self, dt=0):
        if (len(self.mods)//2) % 2 == 0:
            if not self.page == len(self.mods) // 2:
                self.page += 1
                self.page_label.element.text = "Page %s / %s" %(self.page, len(self.mods) // 2)
                for children in self.active_list.get_children():
                    children.kill()

                self.active_list.add(self.mod_list[self.page * 2])
                try:
                    self.active_list.add(self.mod_list[(self.page * 2) + 1])
                except IndexError:
                    pass
        else:
            if not (self.page == len(self.mods) // 2):
                self.page += 1
                self.page_label.element.text = "Page %s / %s" %(self.page, len(self.mods) // 2)
                for children in self.active_list.get_children():
                    children.kill()

                self.active_list.add(self.mod_list[self.page * 2])
                try:
                    self.active_list.add(self.mod_list[(self.page * 2) + 1])
                except IndexError:
                    pass

    def on_previous_page(self, dt=0):
        if not self.page == 0:
            self.page -= 1
            self.page_label.element.text = "Page %s / %s" %(self.page, len(self.mods) // 2)
            for children in self.active_list.get_children():
                children.kill()

            self.active_list.add(self.mod_list[self.page * 2])
            try:
                self.active_list.add(self.mod_list[(self.page * 2) + 1])
            except IndexError:
                pass

class Mod_Listed(gameObjects.Base):
    def __init__(self, mod, img_pos):
        self.mod = mod
        try:
            super().__init__(self.mod.IMAGE, img_pos)

        except:
            super().__init__(pyDLASYIAS.assets.load("images\\modding\\no_image.png"), img_pos)

        self.setup()

    def on_enter(self):
        super().on_enter()
        pyglet.clock.schedule(self.update)

    def on_exit(self):
        super().on_exit()
        pyglet.clock.unschedule(self.update)

    def on_press(self):
        if self.mod.ENABLED:
            self.mod.ENABLED = False
        else:
            self.mod.ENABLED = True

    def update(self, dt=0):
        if self.enabled.isSelected:
            self.enabled_bool.element.text = " " + str(self.mod.ENABLED)
        else:
            self.enabled_bool.element.text = str(self.mod.ENABLED)

    def setup(self):
        self.title = cocos.text.Label(self.mod.TITLE, position=(self.width + 20, self.height - 16), font_size=24, font_name="Fnaf UI")
        self.description = cocos.text.Label(self.mod.DESCRIPTION, position=(self.width + 20,  + self.height - 64), font_size=12, font_name="Fnaf UI", multiline=True, width=director.window.width - self.width - 20)
        self.author = cocos.text.Label("By " + self.mod.AUTHOR, position=(self.width + self.title.element.content_width + 40, self.height - 18), font_size=18, font_name="Fnaf UI")
        self.enabled = Menu_Item("Enabled: ", callback=self.on_press, position = (self.width + 20, 16), font_size=16, font_name="Fnaf UI")
        self.enabled_bool = cocos.text.Label(str(self.mod.ENABLED), position = (self.width + 20 + self.enabled.element.content_width, 16), font_size=12, font_name="Fnaf UI")

        self.enabled.rect = cocos.rect.Rect(self.position[0] + self.width + 20, self.position[1] +  16, self.enabled.element.content_width, self.enabled.element.content_height)

        if self.title.element.content_width > self.description.element.content_width:
            self.layer = cocos.layer.util_layers.ColorLayer(0, 0, 0, 255, width=self.width + self.title.element.content_width + self.author.element.content_width + 60 + 64, height = 264)
        else:
            self.layer = cocos.layer.util_layers.ColorLayer(0, 0, 0, 255, width=self.width + self.description.element.content_width + 64, height = 264)

        self.layer.position = (-32, -32)

        self.add(self.layer, z=-1)
        self.add(self.title, z=4)
        self.add(self.description, z=4)
        self.add(self.author, z=4)
        self.add(self.enabled, z=4)
        self.add(self.enabled_bool, z=4)



class Connect_Client(pyDLASYIAS.scenes.Base):
    def __init__(self):
        super().__init__(None)

        self.setup()

    def go_back(self):
        director.run(main_menu)

    def setup(self):
        self.input_host = Input_Text((256, 256))
        self.input_port = Input_Text((256, 128))

        self.label_host = cocos.text.Label("IP Address", position=(32, 256), font_size=22, font_name="Fnaf UI")
        self.label_port = cocos.text.Label("Port", position=(32, 128), font_size=22, font_name="Fnaf UI")
        self.back = Menu_Item("Back", (32, 16), self.go_back, font_size=16, font_name="Fnaf UI")

        self.add(self.back, z=1)
        self.add(self.input_host, z=1)
        self.add(self.input_port, z=1)
        self.add(self.label_host, z=1)
        self.add(self.label_port, z=1)
        self.add(Menu_Item("Connect", (32, 64), self.connect, font_size=18, font_name="Fnaf UI"))

    def connect(self):
        try:
            address = (self.input_host.text.element.text, int(self.input_port.text.element.text))
        except ValueError:
            print("Error! Is the port a number?")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"testing_connection", address)
            sock.settimeout(10)
            sock.recv(1024)
        except socket.error as e:
            print("Error: %s" %(e))
            director.run(main_menu)
        else:
            sock.close()
            director.run(Online_Hall(address))

class Input_Text(cocos.cocosnode.CocosNode):
    def __init__(self, position):
        super().__init__()

        self.position = position
        self.anchor = (0, 0)

        self.setup()

    def setup(self):
        self.selected = False

        self.layer = cocos.layer.util_layers.ColorLayer(25, 25, 25, 255, width=276, height=32)
        self.layer_2 = cocos.layer.util_layers.ColorLayer(255, 255, 255, 255, width=292, height=48)
        self.layer_2.position = (-8, -8)
        self.layer_2.visible = False
        self.text = cocos.text.Label("", position=(8, 8), font_size=16, font_name="Fnaf UI")

        self.add(self.layer, z=1)
        self.add(self.layer_2, z=0)
        self.add(self.text, z=2)

    def on_key_press(self, k, mod):
        if k == key.BACKSPACE and self.text.element.text != "" and self.selected:
            self.text.element.text = self.text.element.text[:-1]
            if len(self.text.element.text) > 18:
                self.layer.kill()
                self.layer_2.kill()
                self.layer = cocos.layer.util_layers.ColorLayer(25, 25, 25, 255, width=self.layer.width - 16, height=32)
                self.layer_2 = cocos.layer.util_layers.ColorLayer(255, 255, 255, 255, width=self.layer_2.width - 16, height=48)
                self.layer_2.position = (-8, -8)
                self.add(self.layer, z=1)
                self.add(self.layer_2, z=0)

    def on_mouse_press(self, x, y, button, mod):
        rect = cocos.rect.Rect(self.position[0], self.position[1],  self.layer.width, self.layer.height)
        if rect.contains(x, y):
            self.selected = True
            self.layer_2.visible = True
        else:
            self.selected = False
            self.layer_2.visible = False

    def on_text(self, text):
        if self.selected:
            self.text.element.text = self.text.element.text + text
            if len(self.text.element.text) > 18:
                self.layer.kill()
                self.layer_2.kill()
                self.layer = cocos.layer.util_layers.ColorLayer(25, 25, 25, 255, width=self.layer.width + 16, height=32)
                self.layer_2 = cocos.layer.util_layers.ColorLayer(255, 255, 255, 255, width=self.layer_2.width + 16, height=48)
                self.layer_2.position = (-8, -8)
                self.add(self.layer, z=1)
                self.add(self.layer_2, z=0)

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self)

    def on_exit(self):
        super().on_enter()
        director.window.remove_handlers(self)

class Online_Hall(pyDLASYIAS.scenes.Base):
    def __init__(self, address=()):
        super().__init__(None)

        self.address = address

        self.setup()

    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.hasGameStarted = False
        self.thread = threading.Thread(target=self.update_networking)

        self.isGuardLocked = False
        self.isBearLocked = False
        self.isRabbitLocked = False
        self.isChickenLocked = False
        self.isFoxLocked = False

        self.isGuardSelected = False
        self.isBearSelected = False
        self.isRabbitSelected = False
        self.isChickenSelected = False
        self.isFoxSelected = False

        self.character = None

        self.guard_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\multiplayer\\g.png"), (50, 500), anchor=(0, 0))
        self.bear_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\b.png"), (300, 500), anchor=(0,0))
        self.rabbit_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\r.png"), (550, 500), anchor=(0,0))
        self.chicken_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\c.png"), (800, 500), anchor=(0,0))
        self.fox_sprite = cocos.sprite.Sprite(pyDLASYIAS.assets.load("images\\custom\\animatronics\\f.png"), (1050, 500), anchor=(0,0))

        self.guard_label = cocos.text.Label("Guard", position=(100, 465), font_size=16, font_name="Fnaf UI")
        self.bear_label = cocos.text.Label("Bear", position=(350, 465), font_size=16, font_name="Fnaf UI")
        self.rabbit_label = cocos.text.Label("Rabbit", position=(600, 465), font_size=16, font_name="Fnaf UI")
        self.chicken_label = cocos.text.Label("Chicken", position=(850, 465), font_size=16, font_name="Fnaf UI")
        self.fox_label = cocos.text.Label("Fox", position=(1100, 465), font_size=16, font_name="Fnaf UI")
        self.waiting_label = cocos.text.Label("Waiting for players...", position=(32, 32), font_size=16, font_name="Fnaf UI")

        self.guard_layer = cocos.layer.util_layers.ColorLayer(0, 255, 0, 255, width=208, height=208)
        self.guard_layer.position = (-4, -4)
        self.bear_layer = cocos.layer.util_layers.ColorLayer(0, 255, 0, 255, width=208, height=208)
        self.bear_layer.position = (-4, -4)
        self.rabbit_layer = cocos.layer.util_layers.ColorLayer(0, 255, 0, 255, width=208, height=208)
        self.rabbit_layer.position = (-4, -4)
        self.chicken_layer = cocos.layer.util_layers.ColorLayer(0, 255, 0, 255, width=208, height=208)
        self.chicken_layer.position = (-4, -4)
        self.fox_layer = cocos.layer.util_layers.ColorLayer(0, 255, 0, 255, width=208, height=208)
        self.fox_layer.position = (-4, -4)

        self.guard_sprite.add(self.guard_layer, z=-1)
        self.bear_sprite.add(self.bear_layer, z=-1)
        self.rabbit_sprite.add(self.rabbit_layer, z=-1)
        self.chicken_sprite.add(self.chicken_layer, z=-1)
        self.fox_sprite.add(self.fox_layer, z=-1)

        self.lock = Menu_Item("Lock character", position=(32, 80))
        self.lock.visible = False

        self.add(self.bear_sprite, z=1)
        self.add(self.rabbit_sprite, z=1)
        self.add(self.chicken_sprite, z=1)
        self.add(self.fox_sprite, z=1)
        self.add(self.guard_sprite, z=1)
        self.add(self.guard_label, z=1)
        self.add(self.bear_label, z=1)
        self.add(self.rabbit_label, z=1)
        self.add(self.chicken_label, z=1)
        self.add(self.fox_label, z=1)
        self.add(self.lock, z=1)
        self.add(self.waiting_label, z=1)
        self.add(gameObjects.Static(80, 125))

    def lock_character(self):
        self.lock.visible = False
        if self.isGuardSelected:
            self.character = "guard"
            for i in range(0, 10):
                self.socket.sendto(b'guard_locked', self.address)
            self.isGuardLocked = True
            self.guard_layer.color = (0, 0, 255)

        if self.isBearSelected:
            self.character = "bear"
            for i in range(0, 10):
                self.socket.sendto(b'bear_locked', self.address)
            self.isBearLocked = True
            self.bear_layer.color = (0, 0, 255)

        if self.isRabbitSelected:
            self.character = "rabbit"
            for i in range(0, 10):
                self.socket.sendto(b'rabbit_locked', self.address)
            self.isRabbitLocked = True
            self.rabbit_layer.color = (0, 0, 255)

        if self.isChickenSelected:
            self.character = "chicken"
            for i in range(0, 10):
                self.socket.sendto(b'chicken_locked', self.address)
            self.isChickenLocked = True
            self.chicken_layer.color = (0, 0, 255)

        if self.isFoxSelected:
            self.character = "fox"
            for i in range(0, 10):
                self.socket.sendto(b'fox_locked', self.address)
            self.isFoxLocked = True
            self.fox_layer.color == (0, 0, 255)

    def on_mouse_press(self, x, y, button, mod):
        if self.character == None:
            if self.lock.rect.contains(x, y) and self.lock.visible and button == 1:
                self.lock_character()

            self.lock.visible = False
            if self.guard_sprite.get_rect().contains(x, y) and not self.isGuardLocked and button == 1:
                self.guard_layer.color = (255, 255, 0)
                self.isGuardSelected = True
                self.lock.visible = True

            else:
                if not self.isGuardLocked:
                    self.guard_layer.color = (0, 255 ,0)
                    self.isGuardSelected = False

            if self.bear_sprite.get_rect().contains(x, y) and not self.isBearLocked and button == 1:
                self.bear_layer.color = (255, 255, 0)
                self.isBearSelected = True
                self.lock.visible = True

            else:
                if not self.isBearLocked:
                    self.bear_layer.color = (0, 255, 0)
                    self.isBearSelected = False

            if self.rabbit_sprite.get_rect().contains(x, y) and not self.isRabbitLocked and button == 1:
                self.rabbit_layer.color = (255, 255, 0)
                self.isRabbitSelected = True
                self.lock.visible = True

            else:
                if not self.isRabbitLocked:
                    self.rabbit_layer.color = (0, 255, 0)
                    self.isGuardSelected = False

            if self.chicken_sprite.get_rect().contains(x, y) and not self.isChickenLocked and button == 1:
                self.chicken_layer.color = (255, 255, 0)
                self.isChickenSelected = True
                self.lock.visible = True

            else:
                if not self.isChickenLocked:
                    self.chicken_layer.color = (0, 255, 0)
                    self.isChickenSelected = False

            if self.fox_sprite.get_rect().contains(x, y) and not self.isFoxLocked and button == 1:
                self.fox_layer.color = (255, 255, 0)
                self.isFoxSelected = True
                self.lock.visible = True

            else:
                if not self.isFoxLocked:
                    self.fox_layer.color = (0, 255, 0)
                    self.isFoxSelected = False

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self)
        self.thread.start()

    def on_exit(self):
        super().on_exit()
        director.window.remove_handlers(self)
        self.hasGameStarted = True

    def receive_data(self):
        data = self.socket.recv(1024)

        if str(data) == "guard_locked":
            self.isGuardLocked = True

        if str(data) == "bear_locked":
            self.isBearLocked = True

        if str(data) == "rabbit_locked":
            self.isRabbitLocked = True

        if str(data) == "chicken_locked":
            self.isChickenLocked = True

        if str(data) == "fox_locked":
            self.isFoxLocked = True

        if str(data) == "game_start" and not self.hasGameStarted:
            pyglet.clock.unschedule(self.receive_data)
            self.on_exit()
            pyDLASYIAS.networking.Main(self, self.address)

    def update(self, dt=0):
        pass

    def update_networking(self):
        if not self.hasGameStarted:
            self.receive_data()

            self.update_networking()

if __name__ == "__main__":
    global intro, main_menu, custom_night, mods
    director.init(autoscale=True, audio_backend="sdl", \
                  audio=None, fullscreen=False, \
                  resizable=False, vsync=True, width=1280,
                  height=720, caption="pyDLASYIAS", \
                  visible=True)
    director.set_depth_test(True)
    intro = Intro()
    main_menu = Main_Menu()
    custom_night = Custom_Night()
    mods = []
    if platform.system() == "Windows":
        for mod in glob.iglob(".\\mods\\*\\*.py"):
            split = mod.split("\\")
            loaded = __import__(split[1] + "." + split[2] + "." + split[3].replace(".py", ""))
            if split[3] != "__init__.py":
                exec("mods.append(loaded.%s.%s)" %(split[2], split[3].replace(".py", "")))
    else:
        for mod in glob.iglob("./mods//*//*.py"):
            split = mod.split("/")
            loaded = __import__(split[1] + "." + split[2] + "." + split[3].replace(".py", ""))
            if split[3] != "__init__.py":
                exec("mods.append(loaded.%s.%s)" %(split[2], split[3].replace(".py", "")))

    mod_list = Mod_List()

    director.run(intro)
