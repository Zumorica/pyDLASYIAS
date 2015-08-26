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
        self.left_discovered = False
        self.right_discovered = False
        self.about_to_get_scarejumped = False

        # -GameObjects here- #
        self.left_door = gameObjects.Door(False, (72, 0))
        self.right_door = gameObjects.Door(True, (1270, 0))

        self.left_button = gameObjects.Button(False, self.left_door, (0, 180))
        self.right_button = gameObjects.Button(True, self.right_door, (1500, 180))

        self.background = gameObjects.Base("images\\office\\0.png", (0, 0))
        self.scene_button = gameObjects.SceneButton((director.window.width//4, 36))

        self.fan = gameObjects.Fan((781, 221))

        self.power_label = cocos.text.Label("Power left:  "+str(self.Game.power)+"%", position=(40, 150), font_size=16, font_name="Fnaf UI")
        self.usage_label = cocos.text.Label("Usage:  "+str(self.Game.usage), position=(40, 120), font_size=16, font_name="Fnaf UI")
        self.hour_label = cocos.text.Label(str(self.Game.hour)+" AM", position=(1080, 670), font_size=20, font_name="Fnaf UI", bold=True)
        self.night_label = cocos.text.Label(self.Game.night, position=(1080, 640), font_size=14, font_name="Fnaf UI")
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
        self.add(self.fan, z=1)

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

                    if state == True and self.Game.rabbit.location == "left_door":
                        if not self.left_discovered:
                            pyDLASYIAS.assets.Channel[4].play(pyDLASYIAS.assets.Sounds["scary"]["windowscare"], 0)
                            self.left_discovered = True

                if button == "door":
                    pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["door"], 0)
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

                    if state == True and self.Game.chicken.location == "right_door":
                        if not self.right_discovered:
                            pyDLASYIAS.assets.Channel[4].play(pyDLASYIAS.assets.Sounds["scary"]["windowscare"], 0)
                            self.right_discovered = True

                if button == "door":
                    pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["door"], 0)
                    if state == True:
                        self.Game.usage += 1

                    if state == False:
                        self.Game.usage -= 1

        @self.scene_button.event
        def on_button_collide():
            if self.isActive and not self.tablet.isAnimPlaying and not self.Game.power < 0 and not self.about_to_get_scarejumped:
                self.tablet.open()
                pyDLASYIAS.assets.Channel[25].play(pyDLASYIAS.assets.Sounds["camera"]["putdown"], 0)
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
        if not self.game_start and not self.Game.hour >= 6:
            self.tablet.close()
            pyDLASYIAS.assets.Channel[25].play(pyDLASYIAS.assets.Sounds["camera"]["putdown"], 0)
            self.Game.usage -= 1

            if self.Game.rabbit.location == "security_office" and not self.Game.fox.status == 5:
                self.Game.scarejump.death_cause = "rabbit"
                self.about_to_get_scarejumped = True
                self.fan.kill()
                self.background.image = pyglet.image.load("images\\office\\scarejump\\rabbit\\0.png")

            if self.Game.chicken.location == "security_office" and not self.Game.fox.status == 5:
                self.Game.scarejump.death_cause = "chicken"
                self.about_to_get_scarejumped = True
                self.fan.kill()
                self.background.image = pyglet.image.load("images\\office\\scarejump\\chicken\\0.png")
        else:
            self.game_start = False
            pyDLASYIAS.assets.Channel[1].play(pyDLASYIAS.assets.Sounds["ambience"]["fan"], -1)
            pyDLASYIAS.assets.Channel[2].play(pyDLASYIAS.assets.Sounds["ambience"]["ambience"], -1)
            pyDLASYIAS.assets.Channel[3].play(pyDLASYIAS.assets.Sounds["misc"]["lighthum"], -1)
            pyDLASYIAS.assets.Channel[18].play(pyDLASYIAS.assets.Sounds["ambience"]["eerieambience"], -1)
            pyDLASYIAS.assets.Channel[21].play(pyDLASYIAS.assets.Sounds["scary"]["robotvoice"], -1)

            pyDLASYIAS.assets.Channel[2].set_volume(0.5)
            pyDLASYIAS.assets.Channel[18].set_volume(0.0)
            pyDLASYIAS.assets.Channel[20].set_volume(0.1)
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[22].set_volume(0.25)
            pyDLASYIAS.assets.Channel[11].set_volume(0.05)
            pyDLASYIAS.assets.Channel[10].set_volume(0.0)
            pyDLASYIAS.assets.Channel[4].set_volume(0.5)

        pyDLASYIAS.assets.Channel[1].set_volume(0.7)
        pyDLASYIAS.assets.Channel[11].set_volume(0.05)
        pyDLASYIAS.assets.Channel[7].set_volume(0.0)
        pyDLASYIAS.assets.Channel[8].set_volume(0.0)
        pyDLASYIAS.assets.Channel[21].set_volume(0.0)
        pyDLASYIAS.assets.Channel[10].set_volume(0.0)


    def on_exit(self):
        super().on_exit()

    def update(self, dt=0):
        super().update(dt)

        if self.Game.hour >= 6:
            director.run(FadeTransition(self.Game.night_end, duration=1, src=self, color=(0, 0, 0)))

        if self.Game.bear.location == "security_office" and self.moving == "right" and not self.tablet.isAnimPlaying:
            self.Game.scarejump.death_cause = "bear"
            director.run(self.Game.scarejump)

        if self.Game.fox.status == 5 and not self.tablet.isAnimPlaying:
            if self.left_door:
                pyDLASYIAS.assets.Channel[12].set_volume(0.7, 0.3)
                pyDLASYIAS.assets.Channel[12].play(random.choice([pyDLASYIAS.assets.Sounds["misc"]["doorpounding"], pyDLASYIAS.assets.Sounds["misc"]["doorknocking"]]), 0)
                self.Game.fox.status = random.randint(1, 2)
                self.Game.power -= random.randint(3, 15)
            else:
                self.Game.scarejump.death_cause = "fox"
                director.run(self.Game.scarejump)

        if self.Game.scarejump.death_cause in ["rabbit", "chicken"] and not self.tablet.isAnimPlaying:
            director.run(self.Game.scarejump)

        self.power_label.element.text = "Power left:  "+str(self.Game.power)+"%"
        self.usage_label.element.text = "Usage:  "+str(self.Game.usage)
        if self.Game.hour == 0: self.hour_label.element.text = "12 PM"
        else: self.hour_label.element.text = str(self.Game.hour)+" AM"

        if self.Game.power < 0 and not self.tablet.isAnimPlaying and not pyDLASYIAS.assets.Channel[25].get_busy():
            director.run(self.Game.powerout)

        if not self.left_button.light and not self.right_button.light:
            pyDLASYIAS.assets.Channel[3].set_volume(0.0)

        if self.left_button.light:
            pyDLASYIAS.assets.Channel[3].set_volume(0.7, 0.3)

        if self.right_button.light:
            pyDLASYIAS.assets.Channel[3].set_volume(0.3, 0.7)

        if self.Game.power > 25 and self.Game.power <= 100:
            self.background.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.left_button.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.right_button.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.left_door.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.right_door.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)
            self.fan.color = (self.Game.power * 2.55, self.Game.power * 2.55, self.Game.power * 2.55)

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

        if not self.about_to_get_scarejumped:
            if not self.left_button.light and not self.right_button.light:
                self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["0"]

            if self.left_button.light and not self.right_button.light:
                if self.Game.rabbit.location == "left_door":
                    self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["r"]
                else:
                    self.left_discovered = False
                    self.background.image = random.choice([pyDLASYIAS.assets.Backgrounds["office"]["0"], pyDLASYIAS.assets.Backgrounds["office"]["1"]])

            if not self.left_button.light and self.right_button.light:
                if self.Game.chicken.location == "right_door":
                    self.background.image = pyDLASYIAS.assets.Backgrounds["office"]["c"]
                else:
                    self.right_discovered = False
                    self.background.image = random.choice([pyDLASYIAS.assets.Backgrounds["office"]["0"], pyDLASYIAS.assets.Backgrounds["office"]["2"]])

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
        self.fox_animation = gameObjects.Animation("images\\cameras\\cam2a\\animation", 26, 0.025, (0,0), autostart=False, looping=False, isMovable=True)

        self.power_label = cocos.text.Label("Power left:  "+str(self.Game.power)+"%", position=(40, 150), font_size=16, font_name="Fnaf UI")
        self.usage_label = cocos.text.Label("Usage:  "+str(self.Game.usage), position=(40, 120), font_size=16, font_name="Fnaf UI")
        self.hour_label = cocos.text.Label(str(self.Game.hour)+" AM", position=(1080, 670), font_size=20, font_name="Fnaf UI", bold=True)
        self.night_label = cocos.text.Label(self.Game.night, position=(1080, 640), font_size=14, font_name="Fnaf UI")
        self.camera_label = cocos.text.Label(pyDLASYIAS.assets.Cameras[self.active_camera], position=(848, 440), font_size=24, font_name="Fnaf UI")
        self.add(self.power_label, z=10)
        self.add(self.usage_label, z=10)
        self.add(self.hour_label, z=10)
        self.add(self.night_label, z=10)
        self.add(self.camera_label, z=10)

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
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam1b.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam1b.pressed = True
            self.active_camera = "cam1b"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam1c.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam1c.pressed = True
            self.active_camera = "cam1c"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            self.Game.fox.cooldown = True
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam2a.event
        def on_camera_press(camera):
            if self.Game.fox.status >= 4 and self.active_camera != "cam2a" and not self.Game.rabbit.location in ["left_door", "cam2a", "cam2b"]:
                self.add(self.fox_animation, z=1)
                self.fox_animation.play()
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam2a.pressed = True
            self.active_camera = "cam2a"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)

        @self.cam2b.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam2b.pressed = True
            self.active_camera = "cam2b"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam3.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam3.pressed = True
            self.active_camera = "cam3"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass
        @self.cam4a.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam4a.pressed = True
            self.active_camera = "cam4a"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam4b.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam4b.pressed = True
            self.active_camera = "cam4b"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam5.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam5.pressed = True
            self.active_camera = "cam5"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam6.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam6.pressed = True
            self.active_camera = "cam6"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

        @self.cam7.event
        def on_camera_press(camera):
            for camera in self.CamButtons.values():
                camera.pressed = False
            self.cam7.pressed = True
            self.active_camera = "cam7"
            pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            pyDLASYIAS.assets.Channel[11].set_volume(0.1)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["camera"]["blip"], 0)
            try:
                if self.Game.fox.status >= 4:
                    self.fox_animation.kill()
            except Exception:
                pass

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

        self.Game.fox.cooldown = True

    def update(self, dt=0):
        super().update(dt)

        try:
            if self.Game.fox.status >= 4 and self.fox_animation._frame_index == 26 and self.fox_animation in self.get_children():
                self.fox_animation.kill()
                self.Game.fox.status += 1
                director.run(self.Game.office)
        except AttributeError:
            pass    # Animation not playing

        if self.static.opacity != 255:
            pyDLASYIAS.assets.Channel[10].set_volume(0.0)
            pyDLASYIAS.assets.Channel[7].set_volume(1.0)
            pyDLASYIAS.assets.Channel[8].set_volume(0.0)
        else:
            pyDLASYIAS.assets.Channel[10].set_volume(0.75)
            pyDLASYIAS.assets.Channel[7].set_volume(0.25)
            pyDLASYIAS.assets.Channel[8].set_volume(1.0)

        self.power_label.element.text = "Power left:  "+str(self.Game.power)+"%"
        self.usage_label.element.text = "Usage:  "+str(self.Game.usage)
        if self.Game.hour == 0: self.hour_label.element.text = "12 PM"
        else: self.hour_label.element.text = str(self.Game.hour)+" AM"
        self.camera_label.element.text = pyDLASYIAS.assets.Cameras[self.active_camera]

        if self.Game.power < 0:
            director.run(self.Game.office)

        if self.camera_movement == "left" and not self.background.position[0] >= 0.0:
            self.background.dx = 89

        if self.camera_movement == "right" and not self.background.position[0] <= -315.0:
            self.background.dx = -95

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
            elif self.Game.bear.location == "cam1a" and not self.Game.rabbit.location == "cam1a" and not self.Game.chicken.location == "cam1a":
                if self.random_number in range(60, 70):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1a"]["b-1"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1a"]["b"]
            elif not self.Game.bear.location == "cam1a" and not self.Game.rabbit.location == "cam1a" and not self.Game.chicken.location == "cam1a":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1a"]["0"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

        elif self.active_camera == "cam1b":
            if self.Game.bear.location == "cam1b" and not self.Game.rabbit.location == "cam1b" and not self.Game.chicken.location == "cam1b":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["b"]
            elif self.Game.rabbit.location == "cam1b" and not self.Game.chicken.location == "cam1b":
                if self.random_number in range(0, 50):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["r"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["r-1"]
            elif not self.Game.rabbit.location == "cam1b" and self.Game.chicken.location == "cam1b":
                if self.random_number in range(10, 60):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["c"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["c-1"]
            elif not self.Game.rabbit.location == "cam1b" and not self.Game.chicken.location == "cam1b":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1b"]["0"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]


        elif self.active_camera == "cam1c":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam1c"][str(self.Game.fox.status)]

        elif self.active_camera == "cam2a":
            if self.Game.rabbit.location == "cam2a":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam2a"]["r"]
            elif not self.Game.rabbit.location == "cam2a":
                self.background.image = random.choice([pyDLASYIAS.assets.Backgrounds["camera"]["cam2a"]["0"], pyDLASYIAS.assets.Backgrounds["camera"]["cam2a"]["1"]])
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

        elif self.active_camera == "cam2b":
            if self.Game.rabbit.location == "cam2b":
                self.background.image = random.choice([pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["r"], pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["r"], pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["r"], pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["r-1"]])
                pyDLASYIAS.assets.Channel[21].set_volume(random.uniform(0.3, 0.7), random.uniform(0.1, 0.5))
            elif not self.Game.rabbit.location == "cam2b":
                if self.random_number == 87:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["2"]
                elif self.random_number in range(88, 93):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["1"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam2b"]["0"]
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)

        elif self.active_camera == "cam3":
            if self.Game.rabbit.location == "cam3":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam3"]["r"]
            elif not self.Game.rabbit.location == "cam3":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam3"]["0"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

        elif self.active_camera == "cam4a":
            if self.Game.bear.location == "cam4a" and not self.Game.chicken.location == "cam4a":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["b"]
            elif self.Game.chicken.location == "cam4a":
                if self.random_number in range(0, 50):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["c"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["c-1"]
            elif not self.Game.chicken.location == "cam4a":
                if self.random_number == 87:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["2"]
                elif self.random_number == 83:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["1"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4a"]["0"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

        elif self.active_camera == "cam4b":
            if self.Game.bear.location == "cam4b" and not self.Game.chicken.location == "cam4b":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["b"]
                pyDLASYIAS.assets.Channel[21].set_volume(random.uniform(0.1, 0.4), random.uniform(0.3, 0.8))
            elif self.Game.chicken.location == "cam4b":
                 self.background.image = random.choice([pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c-1"], pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["c-2"]])
                 pyDLASYIAS.assets.Channel[21].set_volume(random.uniform(0.1, 0.5), random.uniform(0.3, 0.7))
            elif not self.Game.chicken.location == "cam4b":
                if self.random_number == 87:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["4"]
                elif self.random_number == 86:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["3"]
                elif self.random_number == 85:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["2"]
                elif self.random_number == 84:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["1"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam4b"]["0"]
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
                pyDLASYIAS.assets.Channel[21].set_volume(0.0)

        elif self.active_camera == "cam5":
            if self.Game.rabbit.location == "cam5":
                if self.random_number > 75:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam5"]["r-1"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam5"]["r"]
            elif not self.Game.rabbit.location == "cam5":
                if self.random_number > 87:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam5"]["1"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam5"]["0"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

        elif self.active_camera == "cam6":
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]
            pyDLASYIAS.assets.Channel[11].set_volume(random.uniform(0.6, 0.8))
            if self.Game.chicken.location == "cam6":
                pyDLASYIAS.assets.Channel[11].queue(random.choice([pyDLASYIAS.assets.Sounds["camera"]["pots"], pyDLASYIAS.assets.Sounds["camera"]["pots2"], pyDLASYIAS.assets.Sounds["camera"]["pots3"], pyDLASYIAS.assets.Sounds["camera"]["pots4"]]))
            if self.Game.bear.location == "cam6":
                pyDLASYIAS.assets.Channel[11].play(pyDLASYIAS.assets.Sounds["misc"]["musicbox"], -1)

        elif self.active_camera == "cam7":
            if self.Game.bear.location == "cam7" and not self.Game.chicken.location == "cam7":
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam7"]["b"]
            elif self.Game.chicken.location == "cam7":
                if self.random_number in range(0, 50):
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam7"]["c"]
                else:
                    self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam7"]["c-1"]
            else:
                self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam7"]["0"]

        else:
            self.background.image = pyDLASYIAS.assets.Backgrounds["camera"]["cam6"]["0"]

class Powerout(Base):
    def __init__(self, main_game):
        super().__init__(main_game)

        self.setup()

    def setup(self):
        self.stage = 1
        self.mouse_x = 0
        self.mouse_y = 0

        self.background = gameObjects.Base(pyDLASYIAS.assets.Backgrounds["powerout"]["0"], (0,0))
        self.left_door = gameObjects.Animation("images\\office\\doors\\left", 15, 0.025, (0,0), autostart=False, looping=False)
        self.right_door = gameObjects.Animation("images\\office\\doors\\right", 15, 0.025, (0,0), autostart=False, looping=False)

        self.add(self.background, z=0)
        self.add(self.left_door, z=1)
        self.add(self.right_door, z=1)

    def on_enter(self):
        super().on_enter()
        pygame.mixer.stop()
        self.mouse_x = self.Game.office.mouse_x
        self.mouse_y = self.Game.office.mouse_y
        self.background.position = self.Game.office.background.position
        self.left_door.position = self.Game.office.left_door.position
        self.right_door.position = self.Game.office.right_door.position
        if self.Game.office.left_door.isClosed:
            self.left_door.play_reversed()
            pyDLASYIAS.assets.Channel[8].set_volume(0.7, 0.3)
            pyDLASYIAS.assets.Channel[8].play(pyDLASYIAS.assets.Sounds["misc"]["door"], 0)

        if self.Game.office.right_door.isClosed:
            self.right_door.play_reversed()
            pyDLASYIAS.assets.Channel[9].set_volume(0.3, 0.7)
            pyDLASYIAS.assets.Channel[9].play(pyDLASYIAS.assets.Sounds["misc"]["door"], 0)

        pyDLASYIAS.assets.Channel[1].set_volume(1.0)
        pyDLASYIAS.assets.Channel[2].set_volume(0.5)
        pyDLASYIAS.assets.Channel[4].set_volume(1.0)

        pyDLASYIAS.assets.Channel[1].play(pyDLASYIAS.assets.Sounds["misc"]["powerout"], 0)
        pyDLASYIAS.assets.Channel[2].play(pyDLASYIAS.assets.Sounds["ambience"]["ambience2"], -1)

        pyDLASYIAS.assets.Channel[1].fadeout(18000)

        if random.randint(0, 1):
            pyglet.clock.schedule_once(self.stage_2, 12)

        else:
            pyglet.clock.schedule_once(self.stage_2, random.randint(4, 21))

    def stage_2(self, dt=0):
        self.stage += 1

        pyDLASYIAS.assets.Channel[30].set_volume(0.7, 0.3)
        if random.randint(0, 1):
            pyDLASYIAS.assets.Channel[30].play(pyDLASYIAS.assets.Sounds["misc"]["musicbox"])
            pyDLASYIAS.assets.Channel[30].fadeout(random.randint(3000, int(pyDLASYIAS.assets.Sounds["misc"]["musicbox"].get_length() * 1000)))
        else:
            pyDLASYIAS.assets.Channel[30].play(pyDLASYIAS.assets.Sounds["misc"]["musicbox"])
            pyDLASYIAS.assets.Channel[30].fadeout(26000)

    def stage_3(self, dt=0):
        pygame.mixer.stop()
        if random.randint(0, 1):
            pyDLASYIAS.assets.Channel[1].set_volume(0.0)
            pyDLASYIAS.assets.Channel[2].set_volume(0.35)
            pyDLASYIAS.assets.Channel[1].play(pyDLASYIAS.assets.Sounds["misc"]["lighthum"], -1)
            pyDLASYIAS.assets.Channel[2].play(pyDLASYIAS.assets.Sounds["ambience"]["eerieambience"], -1)
            pyDLASYIAS.assets.Channel[30].play(pyDLASYIAS.assets.Sounds["camera"]["deepsteps"], -1)
            pyglet.clock.schedule_once(self.change_volume, 2, pyDLASYIAS.assets.Channel[30], 0.6, 0.4)
            pyglet.clock.schedule_once(self.change_volume, 3, pyDLASYIAS.assets.Channel[2], 0.5, None)
            pyglet.clock.schedule_once(self.change_volume, 5, pyDLASYIAS.assets.Channel[30], 0.5, 0.5)

        for children in self.get_children():
            children.color = (0, 0, 0)

        self.left_door.color = (255, 255, 255)
        self.right_door.color = (255, 255, 255)

        pyglet.clock.schedule_once(self.change_scene, delay=random.randint(2, 7))

    def change_scene(self, dt=0):
        self.stage += 1

    def change_volume(self, dt=0, channel=None, left=1.0, right=None):
        if right != None:
            channel.set_volume(left, right)
        else:
            channel.set_volume(left)

    def on_mouse_motion(self, x, y, dx, dy):
        real_pos = director.get_virtual_coordinates(x, y)
        self.mouse_x = real_pos[0]
        self.mouse_y = real_pos[1]

    def update(self, dt=0):
        super().update(dt)
        if self.stage == 2:
            self.background.image = random.choice([pyDLASYIAS.assets.Backgrounds["powerout"]["0"], pyDLASYIAS.assets.Backgrounds["powerout"]["0"], pyDLASYIAS.assets.Backgrounds["powerout"]["0"], pyDLASYIAS.assets.Backgrounds["powerout"]["1"]])
            if not pyDLASYIAS.assets.Channel[30].get_busy():
                self.stage += 1
                self.stage_3()

        if self.stage == 4:
            self.Game.scarejump.death_cause = "powerout"
            director.run(self.Game.scarejump)

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

class Scarejump(Base):
    def __init__(self, main_game):
        super().__init__(main_game)

        self.death_cause = None
        self.end_game_now = False

        self.setup()

    def setup(self):
        self.powerout_scarejump = gameObjects.Animation("images\\office\\scarejump\\bear\\powerout", 19, 0.030, img_pos=(0,0), looping=False, isMovable=True, autostart=False)
        self.bear_scarejump = gameObjects.Animation("images\\office\\scarejump\\bear\\normal", 29, 0.0325, img_pos=(0,0), looping=False, isMovable=True, autostart=False)
        self.rabbit_scarejump = gameObjects.Animation("images\\office\\scarejump\\rabbit", 10, 0.030, img_pos=(0,0), looping=True, isMovable=True, autostart=False)
        self.chicken_scarejump = gameObjects.Animation("images\\office\\scarejump\\chicken", 12, 0.030, img_pos=(0,0), looping=True, isMovable=True, autostart=False)
        self.fox_scarejump = gameObjects.Animation("images\\office\\scarejump\\fox", 18, 0.030, img_pos=(0,0), looping=False, isMovable=True, autostart=False)

    def on_enter(self):
        pygame.mixer.stop()
        if self.death_cause == "powerout":
            self.add(self.powerout_scarejump, z=0)
            self.powerout_scarejump.play()
            pyglet.clock.schedule_once(self.static_end, delay=0.06*19)

        elif self.death_cause == "bear":
            self.add(self.bear_scarejump, z=0)
            self.bear_scarejump.position = self.Game.office.background.position
            self.bear_scarejump.play()
            pyglet.clock.schedule_once(self.static_end, delay=0.0325*29)

        elif self.death_cause == "rabbit":
            self.add(self.rabbit_scarejump, z=0)
            self.rabbit_scarejump.position = self.Game.office.background.position
            self.rabbit_scarejump.play()
            pyglet.clock.schedule_once(self.static_end, delay=0.06*10)

        elif self.death_cause == "chicken":
            self.add(self.chicken_scarejump, z=0)
            self.chicken_scarejump.position = self.Game.office.background.position
            self.chicken_scarejump.play()
            pyglet.clock.schedule_once(self.static_end, delay=0.06*12)

        elif self.death_cause == "fox":
            self.add(self.fox_scarejump, z=0)
            self.add(self.Game.office.fan, z=0)
            self.fox_scarejump.position = self.Game.office.background.position
            self.fox_scarejump.play()
            pyglet.clock.schedule_once(self.static_end, delay=0.06*18)

        else:
            raise ValueError("value of death_cause variable unknown")

        pyglet.clock.schedule(self.update)
        self.Game.bear.isActive = False
        self.Game.rabbit.isActive = False
        self.Game.chicken.isActive = False
        self.Game.fox.isActive = False

        pyDLASYIAS.assets.Channel[11].set_volume(1.0)
        pyDLASYIAS.assets.Channel[11].play(pyDLASYIAS.assets.Sounds["scary"]["XSCREAM"])

    def static_end(self, dt=0):
        pygame.mixer.stop()

        self.static = gameObjects.Static()
        self.add(self.static, z=1)
        pyglet.clock.schedule(self.static.update)

        pyDLASYIAS.assets.Channel[11].play(pyDLASYIAS.assets.Sounds["camera"]["static"], 0)

        self.end_game_now = True

    def update(self, dt=0):
        super().update(dt)
        if not self.end_game_now and self.Game.hour >= 6:
            pyDLASYIAS.assets.Channel[11].set_volume(0.0)
            director.run(FadeTransition(self.Game.night_end, duration=1, src=cocos.scene.Scene(gameObjects.Base(self.powerout_scarejump.animation.frames[self.powerout_scarejump._frame_index].image, (0,0))), color=(0, 0, 0)))

            pyglet.clock.unschedule(self.update)

        if self.end_game_now and not pyDLASYIAS.assets.Channel[11].get_busy():
            director.run(FadeTransition(self.Game.stuffed, duration=3, src=cocos.scene.Scene(self.static), color=(0, 0, 0)))

            pyglet.clock.unschedule(self.update)

class Stuffed(Base):
    def __init__(self, main_game):
        super().__init__(main_game)

        self.setup()

    def setup(self):
        self.background = gameObjects.Base("images\\intro\\stuffed.png", (0,0))
        self.label = cocos.text.Label("Game over", position=(1024, 128), font_size=24, font_name="Fnaf UI")


        self.add(self.background, z=0)
        self.add(self.label, z=1)

    def on_enter(self):
        super().on_enter()

        pyglet.clock.schedule(self.update)

    def on_exit(self):
        super().on_exit()

        pyglet.clock.unschedule(self.update)

    def update(self, dt=0):
        pygame.mixer.stop()

class Night_End(Base):
    def __init__(self, redirect, main_game):
        super().__init__(main_game)

        self.redirect = redirect

        self.setup()

    def setup(self):
        self.redirect_now = False

        self.label = cocos.text.Label("5 AM", position=((director.window.width//2) - 32, director.window.height//2), font_size=32, font_name="Fnaf UI", bold=True)
        self.layer = cocos.layer.util_layers.ColorLayer(0, 0, 0, 255)

        self.add(self.layer, z=0)
        self.add(self.label, z=0)

    def on_enter(self):
        super().on_enter()

        #pyDLASYIAS.assets.Channel[11].set_volume(0.0)
        pyDLASYIAS.assets.Channel[1].set_volume(1.0)
        if not pyDLASYIAS.assets.Channel[1].get_busy():
            pyDLASYIAS.assets.Channel[1].play(pyDLASYIAS.assets.Sounds["misc"]["6AM"], 0)

            pyglet.clock.schedule_once(self.stage_2, delay=3)
            pyglet.clock.schedule(self.update)

    def on_exit(self):
        super().on_exit()
        pyglet.clock.unschedule(self.update)

    def stage_2(self, dt=0):
        pyDLASYIAS.assets.Channel[2].set_volume(1.0)
        if not pyDLASYIAS.assets.Channel[2].get_busy():
            pyDLASYIAS.assets.Channel[2].play(pyDLASYIAS.assets.Sounds["misc"]["children"], 0)

        self.label.element.text = "6 AM"

        pyglet.clock.schedule_once(self.stage_3, delay=7)

    def stage_3(self, dt=0):
        self.redirect_now = True

    def update(self, dt=0):
        pyDLASYIAS.assets.Channel[1].set_volume(1.0)
        pyDLASYIAS.assets.Channel[2].set_volume(1.0)
        if self.redirect_now:
            director.run(FadeTransition(self.redirect, duration=1, src=cocos.scene.Scene(self.layer, self.label), color=(0, 0, 0)))

class Ending(Base):
    def __init__(self, ending, main_game):
        self.ending = ending
        super().__init__(main_game)

        self.setup()

    def setup(self):
        self.background = gameObjects.Base("images\\ending\\%s.png"%(self.ending))

        self.add(self.background, z=0)

    def on_enter(self):
        super().on_enter()
        pyDLASYIAS.assets.Channel[1].set_volume(0.0)
        pyDLASYIAS.assets.Channel[2].set_volume(0.0)
        if not pyDLASYIAS.assets.Channel[30].get_busy():
            pyDLASYIAS.assets.Channel[30].set_volume(1.0)
            pyDLASYIAS.assets.Channel[30].play(pyDLASYIAS.assets.Sounds["misc"]["musicbox"], 0)
