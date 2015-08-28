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

import pyDLASYIAS

pyglet.resource.path = ["images"]
pyglet.resource.reindex()

class Base(cocos.sprite.Sprite):

    EventDispatcher = pyglet.event.EventDispatcher()

    def __init__(self, img, img_pos=(0, 0)):
        if isinstance(img, str):
            img_loaded = pyDLASYIAS.assets.load(img)
            super().__init__(img_loaded, img_pos)
        else:
            super().__init__(img, img_pos)

        self.isMovable = True
        self._set_anchor((0, 0))
        self.rect = self.get_rect()

        self.dx = 0
        self.dy = 0

    def update(self, dt=0):
        if self.isMovable and dt != None:
            self.position = (self.position[0] + (self.dx * dt), self.position[1] + (self.dy * dt))
            self.dx = 0
            self.dy = 0
            self.rect = self.get_rect()

    def change_image(self, img):
        try:
            image = pyDLASYIAS.assets.load(img)
        except TypeError:
            image = img
        else:
            self.image = image

        self.rect = self.get_rect()
        self.update()

    def on_enter(self):
        super().on_enter()
        pyglet.clock.schedule(self.update)
        director.window.push_handlers(self)

    def on_exit(self):
        super().on_enter()
        pyglet.clock.unschedule(self.update)
        director.window.remove_handlers(self)

Base.EventDispatcher.register_event_type("on_button_press")
Base.EventDispatcher.register_event_type("on_button_collide")
Base.EventDispatcher.register_event_type("on_camera_press")
Base.EventDispatcher.register_event_type("on_animation_end")

Base.register_event_type("on_button_press")
Base.register_event_type("on_button_collide")
Base.register_event_type("on_camera_press")
Base.register_event_type("on_animation_end")

class Tablet(Base):
    def __init__(self, img_pos=(0, 0)):
        self.isClosed = True
        self.isMovable = False
        self.Frames = []
        self.isAnimPlaying = False

        for i in range(0, 11):
            if i != 10:
                self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\cameras\\misc\\animation\\%s.png" %(i)), 0.020))
            else:
                self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\cameras\\misc\\animation\\%s.png" %(i)), None))

        self.animation_normal = pyglet.image.Animation(self.Frames)
        self.Frames = []

        for i in reversed(range(0, 11)):
            if i != 0:
                self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\cameras\\misc\\animation\\%s.png" %(i)), 0.020))
            else:
                self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\cameras\\misc\\animation\\%s.png" %(i)), None))

        self.animation_reversed = pyglet.image.Animation(self.Frames)
        self.Frames = []

        super().__init__("images\\cameras\\misc\\animation\\0.png", img_pos)
        self.opacity = 0

    def update(self, dt=0):
        super().update(dt)

        self.position = (0, 0)

        @self.event
        def on_animation_end():
            self.opacity = 0
            self.isAnimPlaying = False
            self.EventDispatcher.dispatch_event("on_animation_end")

    def open(self):
        self.isClosed = False
        self.isAnimPlaying = True
        self.image = self.animation_normal
        self.opacity = 255

    def close(self):
        self.isClosed = True
        self.isAnimPlaying = True
        self.image = self.animation_reversed
        self.opacity = 255

class Static(Base):
    def __init__(self, opacity_min=255, opacity_max=255, random=False):
        super().__init__("images\\cameras\\misc\\static\\0.png", (0, 0))
        self.opacity_min = opacity_min
        self.opacity_max = opacity_max
        self.random = random
        self.get_random_opacity()
        self.index = 0
        self.Sprites = [pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\0.png"),
                        pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\1.png"),
                        pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\2.png"),
                        pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\3.png"),
                        pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\4.png"),
                        pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\5.png"),
                        pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\6.png"),
                        pyDLASYIAS.assets.load("images\\cameras\\misc\\static\\7.png")]

    def get_random_opacity(self, dt=0):
        self.opacity = random.randint(self.opacity_min, self.opacity_max)

    def set_opacity(self, opacity, dt=0):
        self.opacity = opacity

    def update(self, dt=0):
        super().update(dt)
        if self.random:
            image = random.choice(self.Sprites)
            if image == self.image:
                self.update()
            else:
                self.image = image
        else:
            self.index += 1
            if self.index > 7:
                self.index = 0
            self.image = self.Sprites[self.index]

class Camera(Base):
    def __init__(self, name, img, img_pos):
        super().__init__("images\\ui\\button\\camera\\0.png", img_pos)
        self.isMovable = False
        if name != "cam1a":
            self.pressed = False
        else:
            self.pressed = True
        self.name = name
        self.text = cocos.sprite.Sprite(pyDLASYIAS.assets.load(img), (img_pos[0] + 7.5, img_pos[1] + 7.5))
        self.text._set_anchor((0, 0))
        self.Sprites = [pyDLASYIAS.assets.load("images\\ui\\button\\camera\\0.png"),
                        pyDLASYIAS.assets.load("images\\ui\\button\\camera\\1.png")]

    def draw(self):
        super().draw()
        self.text.draw()

    def cameraPress(self):
        self.dispatch_event("on_camera_press", self)
        self.EventDispatcher.dispatch_event("on_camera_press", self)

    def on_camera_press(self, camera):
        self.pressed = True
        self.update()

    def on_mouse_press(self, x, y, button, mod):
        real_pos = director.get_virtual_coordinates(x, y)
        if self.contains(real_pos[0], real_pos[1]):
            self.cameraPress()

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self.on_mouse_press)

    def on_exit(self):
        super().on_exit()
        director.window.remove_handlers(self.on_mouse_press)

    def update(self, dt=0):
        if self.pressed:
            self.image = self.Sprites[1]
        else:
            self.image = self.Sprites[0]

class Door(Base):
    def __init__(self, isRightDoor, img_pos):
        self.isRightDoor = isRightDoor
        self.isClosed = False
        self.isMovable = True
        self.Frames = []

        if not self.isRightDoor:
            for i in range(0, 16):
                if i != 15:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\left\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\left\\%s.png" %(i)), None))

            self.animation_normal = pyglet.image.Animation(self.Frames)
            self.Frames = []

            for i in reversed(range(0, 16)):
                if i != 0:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\left\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\left\\%s.png" %(i)), None))

            self.animation_reversed = pyglet.image.Animation(self.Frames)

            super().__init__(pyDLASYIAS.assets.load("images\\office\\doors\\left\\0.png"), img_pos)

        else:
            for i in range(0, 16):
                if i != 15:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\right\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\right\\%s.png" %(i)), None))

            self.animation_normal = pyglet.image.Animation(self.Frames)
            self.Frames = []

            for i in reversed(range(0, 16)):
                if i != 0:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\right\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\doors\\right\\%s.png" %(i)), None))

            self.animation_reversed = pyglet.image.Animation(self.Frames)

            super().__init__(pyDLASYIAS.assets.load("images\\office\\doors\\right\\0.png"), img_pos)

    def update(self, dt=0):
        super().update(dt)

    def open(self, dt=0):
        self.isClosed = False
        self.image = self.animation_reversed

    def close(self, dt=0):
        self.isClosed = True
        self.image = self.animation_normal

    def __cmp__(self, other):
        return self.isClosed == other

    def __eq__(self, other):
        return self.isClosed == other

    def __bool__(self):
        return self.isClosed

class SceneButton(Base):
    def __init__(self, img_pos):
        super().__init__("images\\ui\\button\\camera.png", img_pos)
        self.isMovable = False
        self.cooldown = False

    def collideButton(self):
        self.dispatch_event("on_button_collide")

    def on_button_collide(self):
        pass

    def showImage(self, dt=0):
        self.opacity = 255
        self.cooldown = False

    def on_mouse_motion(self, x, y, dx, dy):
        real_pos = director.get_virtual_coordinates(x, y)
        if self.contains(real_pos[0], real_pos[1]) and not self.cooldown:
            self.opacity = 0
            self.cooldown = True
            self.collideButton()

        if self.contains(real_pos[0], real_pos[1]) and self.cooldown:
            self.opacity = 0
            self.cooldown = True

        else:
            self.showImage()

    def on_enter(self):
        super().on_enter()
        director.window.push_handlers(self.on_mouse_motion)

    def on_exit(self):
        super().on_exit()
        director.window.remove_handlers(self.on_mouse_motion)

class Button(Base):
    def __init__(self, isRightButton, door, img_pos):
        if not isinstance(door, object):
            raise ValueError("'door' is not an object.")

        self.door = door
        self.light = False
        self.isRightButton = isRightButton
        self.isMovable = True
        self.cooldown = False

        if not self.isRightButton:
            self.Sprite = {"0" : pyDLASYIAS.assets.load("images\\office\\button\\left\\0.png"),
                           "d" : pyDLASYIAS.assets.load("images\\office\\button\\left\\d.png"),
                           "l" : pyDLASYIAS.assets.load("images\\office\\button\\left\\l.png"),
                           "dl" : pyDLASYIAS.assets.load("images\\office\\button\\left\\dl.png")}
            super().__init__(self.Sprite["0"], img_pos)

        else:
            self.Sprite = {"0" : pyDLASYIAS.assets.load("images\\office\\button\\right\\0.png"),
                           "d" : pyDLASYIAS.assets.load("images\\office\\button\\right\\d.png"),
                           "l" : pyDLASYIAS.assets.load("images\\office\\button\\right\\l.png"),
                           "dl" : pyDLASYIAS.assets.load("images\\office\\button\\right\\dl.png")}
            super().__init__(self.Sprite["0"], img_pos)

    def buttonPress(self, button, state):
        self.EventDispatcher.dispatch_event("on_button_press", self.isRightButton, button, state)

    def on_button_press(self, isRightButton, button, state):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        real_pos = director.get_virtual_coordinates(x, y)
        position = director.get_virtual_coordinates(self.position[0], self.position[1])
        rect_light = cocos.rect.Rect((position[0] + 30), (position[1] + 62), ((position[0] + 68)-(position[0] + 30)), ((position[1] + 118)-(position[1] + 62)))
        rect_door = cocos.rect.Rect((position[0] + 30), (position[1] + 144), ((position[0] + 68)-(position[0] + 30)), ((position[1] + 193)-(position[1] + 155)))
        #if real_pos[0] in range((int(position[0]) + 30), (int(position[0]) + 68)) and real_pos[1] in range((int(position[1]) + 62), (int(position[1]) + 118)) and button == 1:
        if rect_light.contains(real_pos[0], real_pos[1]) and button == 1:
            if self.light:
                self.light = False
                self.buttonPress("light", self.light)
            else:
                self.light = True
                self.buttonPress("light", self.light)

        #if real_pos[0] in range((int(self.position[0]) + 30), (int(self.position[0]) + 68)) and real_pos[1] in range((int(self.position[1]) + 144), (int(self.position[1]) + 193)) and button == 1 and not self.cooldown:
        if rect_door.contains(real_pos[0], real_pos[1]) and button == 1 and not self.cooldown:
            if self.door:
                self.door.open()
                self.buttonPress("door", self.door)
                self.cooldown = True

            else:
                self.door.close()
                self.buttonPress("door", self.door)
                self.cooldown = True


    def update(self, dt=0):
        super().update(dt)
        if not self.door and not self.light:
            self.image = self.Sprite["0"]

        if self.door and not self.light:
            self.image = self.Sprite["d"]

        if not self.door and self.light:
            self.image = self.Sprite["l"]

        if self.door and self.light:
            self.image = self.Sprite["dl"]

        @self.door.event
        def on_animation_end():
            self.cooldown = False

class Blinking(Base):
    def __init__(self, img, seconds, img_pos, isMovable=False):
        super().__init__(img, img_pos)
        pyglet.clock.schedule_interval(self.schedule_this, seconds)
        self.isMovable = isMovable

    def schedule_this(self, dt=0):
        if self.opacity == 255:
            self.opacity = 0

        elif self.opacity == 0:
            self.opacity = 255

        else:
            self.opacity = 255

class Fan(Base):
    def __init__(self, img_pos):
        self.Frames = []
        self.isMovable = True

        for i in range(0, 3):
                self.Frames.append(pyglet.image.AnimationFrame(pyDLASYIAS.assets.load("images\\office\\fan\\%s.png" %(i)), 0.025))

        self.animation = pyglet.image.Animation(self.Frames)


        super().__init__(self.animation, img_pos)

class Animation(Base):
    def __init__(self, image_path, max_number, frame_time, img_pos, looping=False, isMovable=True, autostart=True):
        self.isMovable = isMovable
        self.Frames = []
        for i in range(0, max_number + 1):
            self.Frames.append(pyDLASYIAS.assets.load("%s\\%s.png" %(image_path, str(i))))

        self.animation = pyglet.image.Animation.from_image_sequence(self.Frames, frame_time, looping)
        self.Frames = []

        for i in reversed(range(0, max_number + 1)):
            self.Frames.append(pyDLASYIAS.assets.load("%s\\%s.png" %(image_path, str(i))))

        self.animation_reversed = pyglet.image.Animation.from_image_sequence(self.Frames, frame_time, looping)
        self.Frames = []

        if autostart:
            super().__init__(self.animation, img_pos)
        else:
            super().__init__("%s\\0.png"%(image_path), img_pos)

    def play(self, dt=0):
        self.image = self.animation

    def play_reversed(self, dt=0):
        self.image = self.animation_reversed
