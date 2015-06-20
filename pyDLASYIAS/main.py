import pyglet
import os
import pyDLASYIAS.gameObjects as gameObjects
from pyglet.gl import *
from pyglet.gl.glu import *

OFFICE = "office"
CAMERA = "camera"

class Main(pyglet.window.Window):
    '''Class for the main game.'''
    def __init__(self):
        '''Initialize the game.'''
        self.hour = 0
        self.power = 100
        self.scene = OFFICE
        self.camera = "cam1a"
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouseClick = False
        self.moving = "left"

        self.GameObjects = {}
        self.CamButtons = {}
        self.Layers = [pyglet.graphics.OrderedGroup(0),
                       pyglet.graphics.OrderedGroup(1),
                       pyglet.graphics.OrderedGroup(2),
                       pyglet.graphics.OrderedGroup(3)]
        self.Batch = {"common" : pyglet.graphics.Batch(),
                      "office" : pyglet.graphics.Batch(),
                      "camera" : pyglet.graphics.Batch(),
                      "ui" : pyglet.graphics.Batch()}

        super().__init__(width=1280, height=720)

        glEnable(GL_TEXTURE_2D)

        self.setup_gameobjects()
        self.change_scene(OFFICE)
        pyglet.clock.schedule(self.update)

    def setup_gameobjects(self):
        self.leftdoor = gameObjects.Door(False, x=72, y=0, batch=self.Batch["office"], group=self.Layers[1])
        self.leftbutton = gameObjects.Button(False, x=0, y=180, door=self.leftdoor, batch=self.Batch["office"], group=self.Layers[1])

        self.rightdoor = gameObjects.Door(True, x=1270, y=0, batch=self.Batch["office"], group=self.Layers[1])
        self.rightbutton = gameObjects.Button(True, x=1500, y=180, door=self.rightdoor, batch=self.Batch["office"], group=self.Layers[1])
        # self.camerabutton = gameObjects.Camera(243, 635, self.Batch["office"], self.Layers[2], True)

        self.CamButtons = {"cam1a" : gameObjects.Camera("images\\ui\\button\\camera\\1a.png", 983, 353, self.Batch["camera"], self.Layers[3]),
                           "cam1b" : gameObjects.Camera("images\\ui\\button\\camera\\1b.png", 963, 409, self.Batch["camera"], self.Layers[3]),
                           "cam1c" : gameObjects.Camera("images\\ui\\button\\camera\\1c.png", 931, 487, self.Batch["camera"], self.Layers[3]),
                           "cam2a" : gameObjects.Camera("images\\ui\\button\\camera\\2a.png", 954, 574, self.Batch["camera"], self.Layers[3]),
                           "cam2b" : gameObjects.Camera("images\\ui\\button\\camera\\2b.png", 956, 626, self.Batch["camera"], self.Layers[3]),
                           "cam3" : gameObjects.Camera("images\\ui\\button\\camera\\3.png", 877, 574, self.Batch["camera"], self.Layers[3]),
                           "cam4a" : gameObjects.Camera("images\\ui\\button\\camera\\4a.png", 1060, 574, self.Batch["camera"], self.Layers[3]),
                           "cam4b" : gameObjects.Camera("images\\ui\\button\\camera\\4b.png", 1060, 636, self.Batch["camera"], self.Layers[3]),
                           "cam5" : gameObjects.Camera("images\\ui\\button\\camera\\5.png", 857, 436, self.Batch["camera"], self.Layers[3]),
                           "cam6" : gameObjects.Camera("images\\ui\\button\\camera\\6.png", 1163, 556, self.Batch["camera"], self.Layers[3]),
                           "cam7" : gameObjects.Camera("images\\ui\\button\\camera\\7.png", 1172, 424, self.Batch["camera"], self.Layers[3])}

        self.background = gameObjects.Sprite("images\\office\\0.png", 0, 0, self.Batch["common"], self.Layers[0])

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        if self.scene == OFFICE:
            self.Batch["common"].draw()
            self.Batch["ui"].draw()
            self.Batch["office"].draw()

        if self.scene == CAMERA:
            self.Batch["common"].draw()
            self.Batch["ui"].draw()
            self.Batch["camera"].draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifier):
        self.mouse_x = x
        self.mouse_y = y
        if button == 0:
            self.mouseClick = True

    def on_mouse_release(self, x, y, button, modifier):
        self.mouse_x = x
        self.mouse_y = y
        if button == 0:
            self.mouseClick = False

    def update(self, dt):

        for value in self.GameObjects.values():
            value.update(dt)

        if self.scene == OFFICE:
            if self.mouse_x in range(0, 150) and not self.GameObjects["background"].x >= 0.0:
                for i in self.GameObjects.values():
                    i.x += int(600 * dt)
                    i.update(dt)

                self.moving = "left"

            if self.mouse_x in range(151, 315) and not self.GameObjects["background"].x >= 0.0:
                for i in self.GameObjects.values():
                    i.x += int(400 * dt)
                    i.update(dt)

                self.moving = "left"

            if self.mouse_x in range(316, 540) and not self.GameObjects["background"].x >= 0.0:
                for i in self.GameObjects.values():
                    i.x += int(200 * dt)
                    i.update(dt)

                self.moving = "left"


            if self.mouse_x in range(1140, 1280) and not self.GameObjects["background"].x <= -315:
                for i in self.GameObjects.values():
                    i.x -= int(600 * dt)
                    i.update(dt)

                self.moving = "right"

            if self.mouse_x in range(1000, 1139) and not self.GameObjects["background"].x <= -315:
                for i in self.GameObjects.values():
                    i.x -= int(400 * dt)
                    i.update(dt)

                self.moving = "right"

            if self.mouse_x in range(750, 999) and not self.GameObjects["background"].x <= -315:
                for i in self.GameObjects.values():
                    i.x -= int(200 * dt)
                    i.update(dt)

                self.moving = "right"

        if self.scene == CAMERA:
            if self.moving == "left" and not self.GameObjects["background"].x >= 0.0:
                self.GameObjects["background"].x += int(500 * dt)

            if self.moving == "right" and not self.GameObjects["background"].x <= -315:
                self.GameObjects["background"].x -= int(500 * dt)

            if self.GameObjects["background"].x >= 0.0:
                self.moving = "right"

            if self.GameObjects["background"].x <= -315:
                self.moving = "left"

    def change_scene(self, scene=None):
        if scene in [OFFICE, CAMERA]:
            if scene == OFFICE:
                self.GameObjects = {}
                self.GameObjects["leftbutton"] = self.leftbutton
                self.GameObjects["rightbutton"] = self.rightbutton
                self.GameObjects["leftdoor"] = self.leftdoor
                self.GameObjects["rightdoor"] = self.rightdoor
                self.GameObjects["background"] = self.background
                # self.GameObjects["camerabutton"] = self.camerabutton
                self.push_handlers(self.leftbutton.on_mouse_press)
                self.push_handlers(self.rightbutton.on_mouse_press)
                # self.push_handlers(self.camerabutton.on_mouse_press)
                try:
                    for i in self.CamButtons.values():
                        self.remove_handler(i.on_mouse_press)
                except:
                    pass

            if scene == CAMERA:
                self.GameObjects = {}

                for key, value in self.CamButtons.items():
                    self.GameObjects[key] = value
                    self.push_handler(value.on_mouse_press)

                try:
                    self.remove_handler(self.leftbutton.on_mouse_press)
                    self.remove_handler(self.rightbutton.on_mouse_press)
                    self.remove_handler(self.camerabutton.on_mouse_press)
                except:
                    pass

            self.moving = "left"
            self.GameObjects["background"].x, self.GameObjects["background"].y = 0, 0
            self.scene = scene

        else:
            raise ValueError("Unknown scene '%s'." % (scene))
