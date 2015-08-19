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
from cocos.euclid import *
from cocos.actions.basegrid_actions import *
from cocos.actions import *
from cocos.director import director
import pyDLASYIAS.gameObjects as gameObjects

class Base(cocos.scene.Scene):
    def __init__(self, main_game):
        super().__init__()
        self.Game = main_game

        self.isActive = False

    def update(self, dt=0):
        pass

    def on_enter(self):
        super().on_enter()
        self.isActive = True
        self.enable_handlers(True)
        director.window.push_handlers(self)
        pyglet.clock.schedule(self.update)

    def on_exit(self):
        super().on_exit()
        self.isActive = False
        self.enable_handlers(False)
        director.window.remove_handlers(self)
        pyglet.clock.unschedule(self.update)

class Office(Base):
    def __init__(self, main_game):
        super().__init__(main_game)

        self.setup()

    def setup(self):
        self.moving = "left"
        self.game_start = True
        self.mouse_x = 0
        self.mouse_y = 0

        # -GameObjects here- #
        self.left_door = gameObjects.Door(False, (72, 0))
        self.right_door = gameObjects.Door(True, (1270, 0))

        self.left_button = gameObjects.Button(False, self.left_door, (0, 180))
        self.right_button = gameObjects.Button(True, self.right_door, (1500, 180))

        self.background = gameObjects.Base("images\\office\\0.png", (0, 0))
        self.scene_button = gameObjects.SceneButton((director.window.width//4, 36))

        self.power_label = cocos.text.Label("Power left:  "+str(self.Game.power)+"%", position=(40, 150), font_size=16)
        self.usage_label = cocos.text.Label("Usage:  "+str(self.Game.usage), position=(40, 120), font_size=16)
        self.hour_label = cocos.text.Label(str(self.Game.hour)+"  AM", position=(1020, 650), font_size=16)
        self.night_label = cocos.text.Label(self.Game.night, position=(1020, 670), font_size=16)
        self.add(self.power_label, z=10)
        self.add(self.usage_label, z=10)
        self.add(self.hour_label, z=10)
        self.add(self.night_label, z=10)

        self.tablet = gameObjects.Tablet()

        self.add(self.background, z=0)
        self.add(self.left_door, z=1)
        self.add(self.right_door, z=1)
        self.add(self.left_button, z=1)
        self.add(self.right_button, z=1)
        self.add(self.scene_button, z=5)
        self.add(self.tablet, z=7)

        @pyDLASYIAS.gameObjects.Button.EventDispatcher.event
        def on_button_press(isRightButton, button, state):
            if not isRightButton:
                if button == "light":
                    if state == True and self.right_button.light:
                        self.right_button.light = False
                        self.left_button.light = True

                    elif state == True and not self.right_button.light:
                        self.Game.usage += 1

                    elif state == False and not self.right_button.light:
                        self.Game.usage -= 1

                if button == "door":
                    if state == True:
                        self.Game.usage += 1

                    elif state == False:
                        self.Game.usage -= 1

            if isRightButton:
                if button == "light":
                    if state == True and self.left_button.light:
                        self.left_button.light = False
                        self.right_button.light = True

                    elif state == True and not self.left_button.light:
                        self.Game.usage += 1

                    elif state == False and not self.left_button.light:
                        self.Game.usage -=1

                if button == "door":
                    if state == True:
                        self.Game.usage += 1

                    if state == False:
                        self.Game.usage -= 1

        @self.scene_button.event
        def on_button_collide():
            if self.isActive and not self.tablet.isAnimPlaying:
                self.tablet.open()
                self.Game.usage += 1
                if self.left_button.light:
                    self.left_button.light = False
                    self.Game.usage -= 1

                if self.right_button.light:
                    self.right_button.light = False
                    self.Game.usage -= 1

        @self.tablet.EventDispatcher.event
        def on_animation_end():
            if not self.tablet.isClosed and self.isActive:
                director.run(self.Game.camera)


    def on_mouse_motion(self, x, y, dx, dy):
        real_pos = director.get_virtual_coordinates(x, y)
        self.mouse_x = real_pos[0]
        self.mouse_y = real_pos[1]

    def on_enter(self):
        super().on_enter()
        if not self.game_start:
            self.tablet.close()
            self.Game.usage -= 1
        else:
            self.game_start = False


    def on_exit(self):
        super().on_exit()

    def update(self, dt=0):
        super().update(dt)

        self.power_label.element.text = "Power left:  "+str(self.Game.power)+"%"
        self.usage_label.element.text = "Usage:  "+str(self.Game.usage)
        if self.Game.hour == 0: self.hour_label.element.text = "12  AM"
        else: self.hour_label.element.text = str(self.Game.hour)+"  PM"

        if self.Game.power > 25:
            self.background.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.left_button.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.right_button.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.left_door.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.right_door.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)

        # The code below makes the office move with the mouse's position.

        if self.mouse_x in range(0, 150) and not self.background.position[0] >= 0.0:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = 600
                except:
                    pass
            self.moving = "left"

        if self.mouse_x in range(151, 315) and not self.background.position[0] >= 0.0:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = 400
                except:
                    pass
            self.moving = "left"

        if self.mouse_x in range(316, 540) and not self.background.position[0] >= 0.0:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = 200
                except:
                    pass
            self.moving = "left"

        if self.mouse_x in range(1140, 1280) and not self.background.position[0] <= -315:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = -600
                except:
                    pass
            self.moving = "right"

        if self.mouse_x in range(1000, 1139) and not self.background.position[0] <= -315:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = -400
                except:
                    pass
            self.moving = "right"

        if self.mouse_x in range(750, 999) and not self.background.position[0] <= -315:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = -200
                except:
                    pass
            self.moving = "right"

        # The code below changes the image of the office.

        if not self.left_button.light and not self.right_button.light:
            self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["0"]

        if self.left_button.light and not self.right_button.light:
            self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["1"]

        if not self.left_button.light and self.right_button.light:
            self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["2"]

class Camera(Base):
    def __init__(self, main_game):
        super().__init__(main_game)

        self.setup()

    def setup(self):
        self.active_camera = "cam1a"
        self.camera_movement = "left"
        self.random_number = 0
        self.mouse_x = 0
        self.mouse_y = 0

        #-GameObjects here-#
        self.cam1a = gameObjects.Camera("cam1a", "images\\ui\\button\\camera\\1a.png", (963, 387))
        self.cam1b = gameObjects.Camera("cam1b", "images\\ui\\button\\camera\\1b.png", (934, 331))
        self.cam1c = gameObjects.Camera("cam1c", "images\\ui\\button\\camera\\1c.png", (901, 253))
        self.cam2a = gameObjects.Camera("cam2a", "images\\ui\\button\\camera\\2a.png", (954, 146))
        self.cam2b = gameObjects.Camera("cam2b", "images\\ui\\button\\camera\\2b.png", (954, 104))
        self.cam3 = gameObjects.Camera("cam3", "images\\ui\\button\\camera\\3.png", (877, 146))
        self.cam4a = gameObjects.Camera("cam4a", "images\\ui\\button\\camera\\4a.png", (1060, 146))
        self.cam4b = gameObjects.Camera("cam4b", "images\\ui\\button\\camera\\4b.png", (1060, 104))
        self.cam5 = gameObjects.Camera("cam5", "images\\ui\\button\\camera\\5.png", (817, 304))
        self.cam6 = gameObjects.Camera("cam6", "images\\ui\\button\\camera\\6.png", (1163, 164))
        self.cam7 = gameObjects.Camera("cam7", "images\\ui\\button\\camera\\7.png", (1172, 296))
        self.map = gameObjects.Base("images\\ui\\map-0.png", (848, 47))
        self.reddot = gameObjects.Blinking("images\\ui\\red-0.png", 0.75, (50, 625))
        self.whiteline = gameObjects.Base("images\\ui\\white-0.png", (0, 0))
        self.static = gameObjects.Static(70, 160)
        self.background = gameObjects.Base("images\\cameras\\cam1a\\brc.png", (0, 0))
        self.scene_button = gameObjects.SceneButton((director.window.width//4, 36))

        self.power_label = cocos.text.Label("Power left:  "+str(self.Game.power)+"%", position=(40, 150), font_size=16)
        self.usage_label = cocos.text.Label("Usage:  "+str(self.Game.usage), position=(40, 120), font_size=16)
        self.hour_label = cocos.text.Label(str(self.Game.hour)+"  AM", position=(1020, 650), font_size=16)
        self.night_label = cocos.text.Label(self.Game.night, position=(1020, 670), font_size=16)
        self.add(self.power_label, z=10)
        self.add(self.usage_label, z=10)
        self.add(self.hour_label, z=10)
        self.add(self.night_label, z=10)

        self.map.isMovable = False
        self.reddot.isMovable = False
        self.static.isMovable = False
        self.whiteline.isMovable = False

        self.CamButtons = {"cam1a" : self.cam1a,
                           "cam1b" : self.cam1b,
                           "cam1c" : self.cam1c,
                           "cam2a" : self.cam2a,
                           "cam2b" : self.cam2b,
                           "cam3" : self.cam3,
                           "cam4a" : self.cam4a,
                           "cam4b" : self.cam4b,
                           "cam5" : self.cam5,
                           "cam6" : self.cam6,
                           "cam7" : self.cam7}

        self.add(self.cam1a, z=5)
        self.add(self.cam1b, z=5)
        self.add(self.cam1c, z=5)
        self.add(self.cam2a, z=5)
        self.add(self.cam2b, z=5)
        self.add(self.cam3, z=5)
        self.add(self.cam4a, z=5)
        self.add(self.cam4b, z=5)
        self.add(self.cam5, z=5)
        self.add(self.cam6, z=5)
        self.add(self.cam7, z=5)
        self.add(self.map, z=4)
        self.add(self.reddot, z=5)
        self.add(self.whiteline, z=4)
        self.add(self.static, z=2)
        self.add(self.scene_button, z=10)
        self.add(self.background, z=0)

        @self.cam1a.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam1a.pressed = True
            self.active_camera = "cam1a"

        @self.cam1b.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam1b.pressed = True
            self.active_camera = "cam1b"

        @self.cam1c.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam1c.pressed = True
            self.active_camera = "cam1c"

        @self.cam2a.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam2a.pressed = True
            self.active_camera = "cam2a"

        @self.cam2b.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam2b.pressed = True
            self.active_camera = "cam2b"

        @self.cam3.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam3.pressed = True
            self.active_camera = "cam3"

        @self.cam4a.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam4a.pressed = True
            self.active_camera = "cam4a"

        @self.cam4b.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam4b.pressed = True
            self.active_camera = "cam4b"

        @self.cam5.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam5.pressed = True
            self.active_camera = "cam5"

        @self.cam6.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam6.pressed = True
            self.active_camera = "cam6"

        @self.cam7.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam7.pressed = True
            self.active_camera = "cam7"

        @self.scene_button.event
        def on_button_collide():
            if self.isActive:
                director.run(self.Game.office)

        return True

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_enter(self):
        super().on_enter()
        self.static.get_random_opacity()
        self.random_number = random.randint(0, 100)

    def update(self, dt=0):
        super().update(dt)

        self.power_label.element.text = "Power left:  "+str(self.Game.power)+"%"
        self.usage_label.element.text = "Usage:  "+str(self.Game.usage)
        if self.Game.hour == 0: self.hour_label.element.text = "12  AM"
        else: self.hour_label.element.text = str(self.Game.hour)+"  PM"

        # # The code below makes the camera move with the mouse.
        # if self.mouse_x in range(0, 150) and not self.background.position[0] >= 0.0:
        #     for children in self.get_children():
        #         if children.isMovable:
        #             children.dx = 600
        #     self.camera_movement = "left"
        #
        # if self.mouse_x in range(151, 315) and not self.background.position[0] >= 0.0:
        #     for children in self.get_children():
        #         if children.isMovable:
        #             children.dx = 400
        #     self.camera_movement = "left"
        #
        # if self.mouse_x in range(316, 540) and not self.background.position[0] >= 0.0:
        #     for children in self.get_children():
        #         if children.isMovable:
        #             children.dx = 200
        #     self.camera_movement = "left"
        #
        # if self.mouse_x in range(1140, 1280) and not self.background.position[0] <= -315:
        #     for children in self.get_children():
        #         if children.isMovable:
        #             children.dx = -600
        #     self.camera_movement = "right"
        #
        # if self.mouse_x in range(1000, 1139) and not self.background.position[0] <= -315:
        #     for children in self.get_children():
        #         if children.isMovable:
        #             children.dx = -400
        #     self.camera_movement = "right"
        #
        # if self.mouse_x in range(750, 999) and not self.background.position[0] <= -315:
        #     for children in self.get_children():
        #         if children.isMovable:
        #             children.dx = -200
        #     self.camera_movement = "right"

        if self.camera_movement == "left" and not self.background.position[0] <= 0:
            self.background.dx = -500

        if self.camera_movement == "right" and not self.background.position[0] <= 320:
            self.background.dx = 500

        if not self.background.position[0] >= 0.0:
            self.camera_movement = "right"

        if not self.background.position[0] <= -315:
            self.camera_movement = "left"

        if self.active_camera == "cam1a":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1a"]["brc"]

        elif self.active_camera == "cam1b":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["0"]

        elif self.active_camera == "cam1c":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1c"]["0"]

        elif self.active_camera == "cam2a":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam2a"]["0"]

        elif self.active_camera == "cam2b":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["0"]

        elif self.active_camera == "cam3":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam3"]["0"]

        elif self.active_camera == "cam4a":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["0"]

        elif self.active_camera == "cam4b":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["0"]

        elif self.active_camera == "cam5":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam5"]["0"]

        elif self.active_camera == "cam6":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

        elif self.active_camera == "cam7":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam7"]["0"]

        else:
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

class Powerout(Base):
    def __init__(self, main_game):
        super().__init__(main_game)

        self.setup()

    def setup(self):
        self.stage = 1

        self.background = gameObjects.Base(pyDLASYIAS.assets.Backgrounds["powerout"]["0"], (0,0))

        self.add(self.background, z=0)

    def on_enter(self):
        super().on_enter()
        if self.Game.office.left_button.door:
            self.add(self.Game.office.left_door, z=1)
            self.Game.office.left_door.open()

        if self.Game.office.right_button.door:
            self.add(self.Game.office.right_door, z=1)
            self.Game.office.right_door.open()

        #Powerout sound here

        if random.randint(0, 1):
            pyglet.clock.schedule_once(self.stage_2, 12)

        else:
            pyglet.clock.schedule_once(self.stage_2, random.randint(4, 18))

    def stage_2(self, dt=0):
        self.stage += 1

        #Musicbox here

        if random.randint(0, 1):
            pyglet.clock.schedule_once(self.stage_3, 12)
        else:
            pyglet.clock.schedule_once(self.stage_3, random.randint(3, 61))

        #Stage 3 and jumpscare here?


    def update(self, dt=0):
        super().update(dt)
        if self.stage == 2:
            self.background.image = random.choice([self.Backgrounds["powerout"]["0"], self.Backgrounds["powerout"]["0"], self.Backgrounds["powerout"]["0"], self.Backgrounds["powerout"]["1"]])

        if self.mouse_x in range(0, 150) and not self.background.position[0] >= 0.0:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = 600
                except:
                    pass
            self.moving = "left"

        if self.mouse_x in range(151, 315) and not self.background.position[0] >= 0.0:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = 400
                except:
                    pass
            self.moving = "left"

        if self.mouse_x in range(316, 540) and not self.background.position[0] >= 0.0:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = 200
                except:
                    pass
            self.moving = "left"

        if self.mouse_x in range(1140, 1280) and not self.background.position[0] <= -315:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = -600
                except:
                    pass
            self.moving = "right"

        if self.mouse_x in range(1000, 1139) and not self.background.position[0] <= -315:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = -400
                except:
                    pass
            self.moving = "right"

        if self.mouse_x in range(750, 999) and not self.background.position[0] <= -315:
            for children in self.get_children():
                try:
                    if children.isMovable:
                        children.dx = -200
                except:
                    pass
            self.moving = "right"
