#!/usr/bin/env python3
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
        self.custom_night = Menu_Item("Custom Night", position=(40, 120), callback=self.enter_custom_night, font_size=16, font_name="Fnaf UI")

        self.add(self.static, z=1)
        self.add(self.background, z=0)
        self.add(self.custom_night, z=2)
        self.add(Menu_Title(position=(32, director.window.height - 64), font_size=32, font_name="Fnaf UI"))

    def enter_custom_night(self):
        director.run(custom_night)

    def on_enter(self):
        super().on_enter()

    def update(self, dt=0):
        super().update(dt)

class Menu_Item(cocos.text.Label):
    def __init__(self, text='', position=(0, 0), callback=None, **kwargs):
        super().__init__(text, position, **kwargs)
        self.rect = cocos.rect.Rect(position[0], position[1], self.element.content_width, self.element.content_height)
        self.callback = callback
        self.isSelected = False

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self)

    def on_exit(self):
        super().on_exit()
        director.window.remove_handlers(self)

    def on_mouse_press(self, x, y, button, mod):
        if self.rect.contains(x, y) and button == 1:
            self.callback()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.rect.contains(x, y) and not self.isSelected and not self.element.text.startswith(">"):
            self.isSelected = True
            self.element.text = ">%s" %(self.element.text)
            pyDLASYIAS.assets.Sounds["camera"]["blip"].play(0)
        elif self.element.text.startswith(">") and not self.rect.contains(x, y):
            self.element.text = self.element.text[1:]
            self.isSelected = False

class Menu_Title(cocos.text.Label):
    def __init__(self, position=(0, 0), **kwargs):
        super().__init__(">pyDLASYIAS", position, **kwargs)
        self.rect = cocos.rect.Rect(position[0], position[1], self.element.content_width, self.element.content_height)
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
        self.add(self.button_right_fox, z=1)
        self.add(self.button_left_time, z=1)
        self.add(self.button_right_time, z=1)
        self.add(self.label_time, z=1)
        self.add(self.button_left_power, z=1)
        self.add(self.button_right_power, z=1)
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

        if self.button_ready.contains(x, y):
            pyDLASYIAS.main.Main(power=self.power, hour=self.hour, \
                                 night="Custom Night", ending="custom", \
                                 bear_level = self.bear_level, \
                                 rabbit_level = self.rabbit_level, \
                                 chicken_level = self.chicken_level, \
                                 fox_level = self.fox_level, menu=main_menu)

    def update(self, dt=0):
        super().update(dt)
        self.label_power.element.text = str(self.power)
        self.label_time.element.text = str(self.hour)
        self.label_bear_level.element.text = str(self.bear_level)
        self.label_rabbit_level.element.text = str(self.rabbit_level)
        self.label_chicken_level.element.text = str(self.chicken_level)
        self.label_fox_level.element.text = str(self.fox_level)

if __name__ == "__main__":
    global intro, main_menu, custom_night
    director.init(autoscale=True, audio_backend="sdl", \
                  audio=None, fullscreen=False, \
                  resizable=False, vsync=True, width=1280,
                  height=720, caption="pyDLASYIAS", \
                  visible=True)
    director.set_depth_test(True)
    intro = Intro()
    main_menu = Main_Menu()
    custom_night = Custom_Night()
    director.run(intro)
