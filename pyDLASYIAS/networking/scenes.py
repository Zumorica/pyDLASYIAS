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
from cocos.euclid import *
from cocos.actions.basegrid_actions import *
from cocos.actions import *
from cocos.director import director
from cocos.scenes import *
import pyDLASYIAS.gameObjects as gameObjects
import pyDLASYIAS.scenes as scenes

class Chicken_Camera(pyDLASYIAS.scenes.Base):
    def __init__(self, main_game):
        super().__init__(main_game)

        self.setup()

    def setup(self):
        self.name = "camera"
        self.Game.chicken.location = "cam1a"
        self.active_camera = "cam1a"
        self.camera_movement = "left"
        self.random_number = 0
        self.mouse_x = 0
        self.mouse_y = 0

        self.left_door = gameObjects.Door(False, (72, 0))
        self.right_door = gameObjects.Door(True, (1270, 0))
        self.left_door.visible = False
        self.right_door.visible = False
        self.left_button = gameObjects.Button(False, self.left_door, (0, 180), False)
        self.right_button = gameObjects.Button(True, self.right_door, (1500, 180), False)
        self.left_button.visible = False
        self.right_button.visible = False
        self.fan = gameObjects.Fan((781, 221))
        self.fan.visible = False
        self.cam1a = gameObjects.Camera("cam1a", "images\\ui\\button\\camera\\1a.png", (963, 387))
        self.cam1b = gameObjects.Camera("cam1b", "images\\ui\\button\\camera\\1b.png", (934, 331))
        self.cam4a = gameObjects.Camera("cam4a", "images\\ui\\button\\camera\\4a.png", (1060, 146))
        self.cam4b = gameObjects.Camera("cam4b", "images\\ui\\button\\camera\\4b.png", (1060, 104))
        self.cam6 = gameObjects.Camera("cam6", "images\\ui\\button\\camera\\6.png", (1163, 164))
        self.cam7 = gameObjects.Camera("cam7", "images\\ui\\button\\camera\\7.png", (1172, 296))
        self.cam_door = gameObjects.Camera("right_door", "images\\ui\\button\\camera\\door.png", (1030, 55), door_button=True)
        self.map = gameObjects.Base("images\\ui\\map-1.png", (848, 47))
        self.reddot = gameObjects.Blinking("images\\ui\\red-0.png", 0.75, (50, 625))
        self.whiteline = gameObjects.Base("images\\ui\\white-0.png", (0, 0))
        self.static = gameObjects.Static(70, 160)
        self.background = gameObjects.Base("images\\cameras\\cam1a\\brc.png", (0, 0))

        self.cooldown_label = cocos.text.Label("Cooldown:  "+str(self.Game.cooldown), position=(40, 180), font_size=16, font_name="Fnaf UI")
        self.power_label = cocos.text.Label("Power left:  "+str(self.Game.power)+"%", position=(40, 150), font_size=16, font_name="Fnaf UI")
        self.usage_label = cocos.text.Label("Guard's usage:  "+str(self.Game.usage), position=(40, 120), font_size=16, font_name="Fnaf UI")
        self.hour_label = cocos.text.Label(str(self.Game.hour)+" AM", position=(1080, 670), font_size=20, font_name="Fnaf UI", bold=True)
        self.night_label = cocos.text.Label(self.Game.night, position=(1080, 640), font_size=14, font_name="Fnaf UI")
        self.camera_label = cocos.text.Label(pyDLASYIAS.assets.Cameras[self.Game.chicken.location], position=(848, 440), font_size=24, font_name="Fnaf UI")
        self.guard_camera_label = cocos.text.Label("Guard is watching " + self.Game.guard.last_cam, position=(40, 90), font_size=16, font_name="Fnaf UI")
        self.door_time_label = cocos.text.Label("Door time:  " + str(self.Game.door_time), position=(40, 210), font_size=16, font_name="Fnaf UI")
        self.add(self.cooldown_label, z=10)
        self.add(self.power_label, z=10)
        self.add(self.usage_label, z=10)
        self.add(self.hour_label, z=10)
        self.add(self.night_label, z=10)
        self.add(self.camera_label, z=10)
        self.add(self.guard_camera_label, z=10)
        self.add(self.door_time_label, z=10)

        self.map.isMovable = False
        self.reddot.isMovable = False
        self.static.isMovable = False
        self.whiteline.isMovable = False
        self.left_button.isMovable = False
        self.right_button.isMovable = False

        self.CamButtons = {"cam1a" : self.cam1a,
                                      "cam1b" : self.cam1b,
                                      "cam4a" : self.cam4a,
                                      "cam4b" : self.cam4b,
                                      "cam6" : self.cam6,
                                      "cam7" : self.cam7,
                                      "cam_door" : self.cam_door}

        self.add(self.cam1a, z=5)
        self.add(self.cam1b, z=5)
        self.add(self.cam4a, z=5)
        self.add(self.cam4b, z=5)
        self.add(self.cam6, z=5)
        self.add(self.cam7, z=5)
        self.add(self.cam_door, z=5)
        self.add(self.map, z=4)
        self.add(self.reddot, z=5)
        self.add(self.whiteline, z=4)
        self.add(self.static, z=2)
        self.add(self.background, z=0)

        self.add(self.left_door, z=1)
        self.add(self.right_door, z=1)
        self.add(self.left_button, z=1)
        self.add(self.right_button, z=1)
        self.add(self.fan, z=1)

        @self.cam1a.event
        def on_camera_press(camera):
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["error"], 0)

        @self.cam1b.event
        def on_camera_press(camera):
            if not self.Game.cooldown and self.Game.chicken.location in ["cam1a", "cam7", "cam6", "cam4a"]:
                for camera in self.CamButtons.values():
                    camera.pressed = False
                self.cam1b.pressed = True
                self.Game.chicken.location = "cam1b"
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
                pyDLASYIAS.assets.Channel[11].set_volume(0.1)
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
                self.Game.cooldown = random.randint(500, 3000)
            else:
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["error"], 0)

        @self.cam4a.event
        def on_camera_press(camera):
            if not self.Game.cooldown and self.Game.chicken.location in ["cam1b"]:
                for camera in self.CamButtons.values():
                    camera.pressed = False
                self.cam4a.pressed = True
                self.Game.chicken.location = "cam4a"
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
                pyDLASYIAS.assets.Channel[11].set_volume(0.1)
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
                self.Game.cooldown = random.randint(500, 3000)
            else:
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["error"], 0)

        @self.cam4b.event
        def on_camera_press(camera):
            if not self.Game.cooldown and self.Game.chicken.location in ["cam4a"]:
                for camera in self.CamButtons.values():
                    camera.pressed = False
                self.cam4b.pressed = True
                self.Game.chicken.location = "cam4b"
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
                pyDLASYIAS.assets.Channel[11].set_volume(0.1)
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
                self.Game.cooldown = random.randint(500, 3000)
            else:
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["error"], 0)

        @self.cam6.event
        def on_camera_press(camera):
            if not self.Game.cooldown and self.Game.chicken.location in ["cam1b", "cam7"]:
                for camera in self.CamButtons.values():
                    camera.pressed = False
                self.cam6.pressed = True
                self.Game.chicken.location = "cam6"
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
                pyDLASYIAS.assets.Channel[11].set_volume(0.1)
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
                self.Game.cooldown = random.randint(500, 3000)
            else:
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["error"], 0)

        @self.cam7.event
        def on_camera_press(camera):
            if not self.Game.cooldown and self.Game.chicken.location in ["cam1b", "cam6"]:
                for camera in self.CamButtons.values():
                    camera.pressed = False
                self.cam7.pressed = True
                self.Game.chicken.location = "cam7"
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
                pyDLASYIAS.assets.Channel[11].set_volume(0.1)
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
                self.Game.cooldown = random.randint(500, 3000)
            else:
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["error"], 0)

        @self.cam_door.event
        def on_camera_press(camera):
            if not self.Game.cooldown and self.Game.chicken.location in ["cam4b"]:
                for camera in self.CamButtons.values():
                    camera.pressed = False
                self.cam_door.pressed = True
                self.Game.chicken.location = "right_door"
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
                pyDLASYIAS.assets.Channel[11].set_volume(0.1)
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
                self.Game.cooldown = random.randint(500, 3000)
            else:
                pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["error"], 0)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_enter(self):
        super().on_enter()
        self.static.get_random_opacity()
        self.random_number = random.randint(0, 100)

        pyDLASYIAS.assets.Channel[7].set_volume(1.0)
        pyDLASYIAS.assets.Channel[8].set_volume(0.0)
        pyDLASYIAS.assets.Channel[1].set_volume(0.03)
        pyDLASYIAS.assets.Channel[10].set_volume(0.0)
        pyDLASYIAS.assets.Channel[12].set_volume(0.0)

        pyDLASYIAS.assets.Channel[7].play(pyDLASYIAS.assets.Sounds["camera"]["camerasound2"], -1)
        pyDLASYIAS.assets.Channel[8].play(pyDLASYIAS.assets.Sounds["camera"]["static3"], -1)
        pyDLASYIAS.assets.Channel[10].play(random.choice([pyDLASYIAS.assets.Sounds["camera"]["garble"], \
                                                          pyDLASYIAS.assets.Sounds["camera"]["garble2"], \
                                                          pyDLASYIAS.assets.Sounds["camera"]["garble3"]]), -1)

    def on_exit(self):
        super().on_exit()

    def update(self, dt=0):

        self.left_door.visible = False
        self.right_door.visible = False
        self.left_button.visible = False
        self.right_button.visible = False
        self.fan.visible = False

        for cam in self.CamButtons: self.CamButtons[cam].pressed = False
        exec("self.%s.pressed = True" %(self.active_camera))

        if self.Game.cooldown and not (self.Game.guard.last_cam == self.Game.chicken.location and self.Game.guard.scene == "camera"):
            self.Game.cooldown -= 1

        if self.Game.door_time >= 0 and self.Game.chicken.location == "right_door":
            self.Game.door_time -= 2
            if self.Game.door_time < 0:
                self.Game.door_time = 0

        if self.Game.chicken.location == "cam7":
            self.Game.door_time += 1

        if self.Game.chicken.location == "cam6":
            self.Game.door_time += 2

        if not self.Game.door_time and self.Game.chicken.location == "right_door":
            self.door_time = 100
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam1b.pressed = True
            self.Game.chicken.location = "cam1b"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            self.Game.cooldown = random.randint(300, 1200)

        if self.static.opacity != 255:
            pyDLASYIAS.assets.Channel[10].set_volume(0.0)
            pyDLASYIAS.assets.Channel[7].set_volume(1.0)
            pyDLASYIAS.assets.Channel[8].set_volume(0.0)
        else:
            pyDLASYIAS.assets.Channel[10].set_volume(0.75)
            pyDLASYIAS.assets.Channel[7].set_volume(0.25)
            pyDLASYIAS.assets.Channel[8].set_volume(1.0)

        self.cooldown_label.element.text = "Cooldown:  "+str(self.Game.cooldown)
        self.power_label.element.text = "Power left:  "+str(self.Game.power)+"%"
        self.usage_label.element.text = "Guard's usage:  "+str(self.Game.usage)
        if self.Game.guard.scene == "camera":
            self.guard_camera_label.element.text = "Guard is watching " + self.Game.guard.last_cam
        else:
            self.guard_camera_label.element.text = "Guard isn't watching the cameras"
        if self.Game.hour == 0:
            self.hour_label.element.text = "12 PM"
        else:
            self.hour_label.element.text = str(self.Game.hour)+" AM"
        self.camera_label.element.text = pyDLASYIAS.assets.Cameras[self.active_camera]
        self.door_time_label.element.text = "Door time:  " + str(self.Game.door_time)

        self.active_camera = self.Game.chicken.location

        if self.Game.power < 0:
            director.run(self.Game.office)

        if self.camera_movement == "left" and not self.background.position[0] >= 0.0:
            self.background.dx = 89
            self.left_door.dx = 89
            self.right_door.dx = 89
            self.left_button.dx = 89
            self.right_button.dx = 89
            self.fan.dx = 89

        if self.camera_movement == "right" and not self.background.position[0] <= -315.0:
            self.background.dx = -95
            self.left_door.dx = -95
            self.right_door.dx = -95
            self.left_button.dx = -95
            self.right_button.dx = -95
            self.fan.dx = -95

        if self.background.position[0] >= 0.0:
            self.camera_movement = "right"

        if self.background.position[0] <= -315.0:
            self.camera_movement = "left"

        if self.active_camera == "cam1a":
            if self.Game.bear.location == "cam1a" and self.Game.rabbit.location == "cam1a" and self.Game.chicken.location == "cam1a":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1a"]["brc"]
            elif self.Game.bear.location == "cam1a" and self.Game.rabbit.location == "cam1a" and not self.Game.chicken.location == "cam1a":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1a"]["br"]
            elif self.Game.bear.location == "cam1a" and not self.Game.rabbit.location == "cam1a" and self.Game.chicken.location == "cam1a":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1a"]["bc"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
        elif self.active_camera == "cam1b":
            if not self.Game.rabbit.location == "cam1b" and self.Game.chicken.location == "cam1b":
                if self.random_number in range(10, 60):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["c"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["c-1"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
        elif self.active_camera == "cam4a":
            if self.Game.chicken.location == "cam4a":
                if self.random_number in range(0, 50):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["c"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["c-1"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
        elif self.active_camera == "cam4b":
            if self.Game.chicken.location == "cam4b":
                 self.background.image = random.choice([pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c-1"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c-2"]])
                 pyDLASYIAS.assets.Channel[21].set_volume(random.uniform(0.1, 0.5), random.uniform(0.3, 0.7))
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
        elif self.active_camera == "cam6":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
            pyDLASYIAS.assets.Channel[11].set_volume(random.uniform(0.6, 0.8))
            pyDLASYIAS.assets.Channel[13].set_volume(random.uniform(0.6, 0.8))
            if self.Game.chicken.location == "cam6":
                pyDLASYIAS.assets.Channel[13].queue(random.choice([pyDLASYIAS.assets.Sounds["camera"]["pots"], pyDLASYIAS.assets.Sounds["camera"]["pots2"], pyDLASYIAS.assets.Sounds["camera"]["pots3"], pyDLASYIAS.assets.Sounds["camera"]["pots4"]]))
            if self.Game.bear.location == "cam6":
                pyDLASYIAS.assets.Channel[11].play(pyDLASYIAS.assets.Sounds["misc"]["musicbox"], -1)
        elif self.active_camera == "cam7":
            if self.Game.chicken.location == "cam7":
                if self.random_number in range(0, 50):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam7"]["c"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam7"]["c-1"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
        elif self.active_camera == "right_door":
            self.left_door.visible = True
            self.right_door.visible = True
            self.left_button.visible = True
            self.right_button.visible = True
            self.fan.visible = True
            if not self.Game.guard.left_light and not self.Game.guard.right_light:
                self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["0"]
            elif not self.Game.guard.left_light and self.Game.guard.right_light:
                self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["c"]
            elif self.Game.guard.left_light and not self.Game.guard.right_light:
                if self.Game.rabbit.location == "left_door":
                    self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["r"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["1"]
        else:
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
