import pyDLASYIAS.networking.netObjects
import pyDLASYIAS.networking.scenes

import copy
import socket
import pyDLASYIAS
import cocos
import pyglet
import pickle
import threading
import traceback
import pygame.mixer
import time
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

class Guard_Main(pyDLASYIAS.main.Main):
    def __init__(self, online_hall, sock, address):

        for channel in pyDLASYIAS.assets.Channel: channel.set_volume(1.0)

        self.usage = 1
        self.power = 100
        self.hour = 0
        self.night = "Online"
        self.networking = True
        self.address =address
        self.socket = sock
        self.data = b""
        self.mods = []

        self.guard = netObjects.Guard()
        self.bear = netObjects.Bear()
        self.rabbit = netObjects.Rabbit()
        self.chicken = netObjects.Chicken()
        self.fox = netObjects.Fox()

        self.window = director.window
        self.main_menu = online_hall        # Use online hall as a menu
        self.office = pyDLASYIAS.scenes.Office(self)
        self.camera = pyDLASYIAS.scenes.Camera(self)
        self.powerout = pyDLASYIAS.scenes.Powerout(self)
        self.scarejump = pyDLASYIAS.scenes.Scarejump(self)
        self.stuffed = pyDLASYIAS.scenes.Stuffed(self)
        self.ending = pyDLASYIAS.scenes.Ending("custom", self)
        self.night_end = pyDLASYIAS.scenes.Night_End(self.main_menu, self)

        self.animatronics = {"Bear" : self.bear,
                             "Rabbit" : self.rabbit,
                             "Chicken" : self.chicken,
                             "Fox" : self.fox}

        #threading.Thread(target=self.update_networking).start()
        pyglet.clock.schedule(self.update_networking)
        director.run(self.office)

    def change_static_opacity(self, location, local=True):
        if local:
            if location == self.camera.active_camera:
                self.camera.static.opacity = 255
                pyglet.clock.schedule_once(self.camera.static.get_random_opacity, random.randint(2, 5))
        else:
            self.camera.static.opacity = 255
            pyglet.clock.schedule_once(self.camera.static.get_random_opacity, random.randint(2, 5))

    def send_data(self):
        self.socket.sendto(self.guard.get_pickled(), self.address)

    def receive_data(self):
        self.data = self.socket.recv(2048)
        try:
            obj = pickle.loads(self.data)
            if obj.kind == "world":
                self.power = obj.power
                self.hour = obj.hour

                if obj.chicken.location != self.chicken.location:
                    self.change_static_opacity(self.chicken.location)
                    self.change_static_opacity(obj.chicken.location)
                    self.chicken = obj.chicken

                if obj.rabbit.location != self.rabbit.location:
                    self.change_static_opacity(self.rabbit.location)
                    self.change_static_opacity(obj.rabbit.location)
                    self.rabbit = obj.rabbit

                if obj.bear.location != self.bear.location:
                    self.change_static_opacity(self.bear.location)
                    self.change_static_opacity(obj.bear.location)
                    self.bear = obj.bear

                self.fox = obj.fox

            elif obj.kind == "event":
                if obj.event == "scarejump":
                    pass

            else:
                print("WARNING: Unknown object received:")
                print(repr(obj))
                print()

        except Exception as err:
            print(traceback.format_exc())

    def update_networking(self, dt=0):
        self.guard.left_door = self.office.left_door.isClosed
        self.guard.left_light = self.office.left_button.light
        self.guard.right_door = self.office.right_door.isClosed
        self.guard.right_light = self.office.right_button.light
        self.guard.last_cam = self.camera.active_camera
        try:
            self.guard.scene = director.scene.name
        except Exception as err:
            print(traceback.format_exc())
            self.guard.scene = "office"
        self.guard.usage = self.usage
        self.send_data()
        self.receive_data()


class Chicken_Main(pyDLASYIAS.main.Main):
    def __init__(self, online_hall, sock, address):

        for channel in pyDLASYIAS.assets.Channel: channel.set_volume(1.0)

        self.usage = 1
        self.power = 100
        self.hour = 0
        self.cooldown = 1000
        self.door_time = 100
        self.night = "Online"
        self.networking = True
        self.address =address
        self.socket = sock
        self.data = b""
        self.mods = []

        self.guard = netObjects.Guard()
        self.bear = netObjects.Bear()
        self.rabbit = netObjects.Rabbit()
        self.chicken = netObjects.Chicken()
        self.fox = netObjects.Fox()

        self.window = director.window
        self.main_menu = online_hall        # Use online hall as a menu
        self.camera = pyDLASYIAS.networking.scenes.Chicken_Camera(self)
        self.powerout = pyDLASYIAS.scenes.Powerout(self)
        self.scarejump = pyDLASYIAS.scenes.Scarejump(self)
        self.stuffed = pyDLASYIAS.scenes.Stuffed(self)
        self.ending = pyDLASYIAS.scenes.Ending("custom", self)
        self.night_end = pyDLASYIAS.scenes.Night_End(self.main_menu, self)

        self.animatronics = {"Bear" : self.bear,
                             "Rabbit" : self.rabbit,
                             "Chicken" : self.chicken,
                             "Fox" : self.fox}

        #threading.Thread(target=self.update_networking).start()

        pyglet.clock.schedule(self.update_networking)

        director.run(self.camera)

    def send_data(self):
        self.socket.sendto(self.chicken.get_pickled(), self.address)

    def receive_data(self):
        self.data = self.socket.recv(2048)
        try:
            obj = pickle.loads(self.data)
            if obj.kind == "world":
                self.power = obj.power
                self.hour = obj.hour

                if self.guard.left_door == False and obj.guard.left_door == True:
                    self.camera.left_door.close()
                if self.guard.left_door == True and obj.guard.left_door == False:
                    self.camera.left_door.open()

                if self.guard.right_door == False and obj.guard.right_door == True:
                    self.camera.right_door.close()
                if self.guard.right_door == True and obj.guard.right_door == False:
                    self.camera.right_door.open()

                if obj.guard.last_cam == self.chicken.location:
                    self.chicken.isOnCamera = True
                else:
                    self.chicken.isOnCamera = False

                self.camera.left_button.light = obj.guard.left_light
                self.camera.right_button.light = obj.guard.left_light
                self.usage = obj.guard.usage

                self.guard = obj.guard

                if obj.rabbit.location != self.rabbit.location:
                    self.change_static_opacity(self.rabbit.location)
                    self.change_static_opacity(obj.rabbit.location)
                    self.rabbit = obj.rabbit

                if obj.bear.location != self.bear.location:
                    self.change_static_opacity(self.bear.location)
                    self.change_static_opacity(obj.bear.location)
                    self.bear = obj.bear

                self.fox = obj.fox


            elif obj.kind == "event":
                if obj.event == "scarejump":
                    pass

            else:
                print("WARNING: Unknown object received:")
                print(repr(obj))
                print()

        except Exception as err:
            print(traceback.format_exc())

    # def receive_data(self):
    #     self.data = self.socket.recv(2048)
    #     try:
    #         obj = pickle.loads(self.data)
    #         if obj.kind == "chicken":
    #             pass
    #
    #         elif obj.kind == "rabbit":
    #             self.rabbit = obj
    #
    #         elif obj.kind == "fox":
    #             self.fox = obj
    #
    #         elif obj.kind == "bear":
    #             self.bear = obj
    #
    #         elif obj.kind == "guard":
    #             if self.guard.left_door == False and obj.left_door == True:
    #                 self.camera.left_door.close()
    #             if self.guard.left_door == True and obj.left_door == False:
    #                 self.camera.left_door.open()
    #
    #             if self.guard.right_door == False and obj.right_door == True:
    #                 self.camera.right_door.close()
    #             if self.guard.right_door == True and obj.right_door == False:
    #                 self.camera.right_door.open()
    #
    #             if obj.last_cam == self.chicken.location:
    #                 self.chicken.isOnCamera = True
    #             else:
    #                 self.chicken.isOnCamera = False
    #
    #             self.camera.left_button.light = obj.left_light
    #             self.camera.right_button.light = obj.left_light
    #
    #             self.guard = copy.copy(obj)
    #
    #         elif obj.kind == "night_state":
    #             self.hour = obj.hour
    #             self.power = obj.power
    #
    #         elif obj.kind == "event":
    #             if obj.event == "scarejump":
    #                 pass
    #
    #         else:
    #             print("UNKNOWN OBJECT RECEIVED!", str(obj))
    #
    #     except:
    #         raise
    #         print("Not an pickled object?")

    def update_networking(self, dt=0):
        self.send_data()
        self.receive_data()
