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

        self.mouse_x = 0
        self.mouse_y = 0
        self.mouseClick = False
        self.moving = "left"

        self.GameObjects = {}
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

        pyglet.clock.schedule(self.update)
        self.setup_gameobjects()

    def setup_gameobjects(self):
        self.leftdoor = gameObjects.Door(False, x=72, y=0, batch=self.Batch["office"], group=self.Layers[1])
        self.leftbutton = gameObjects.Button(False, x=0, y=180, door=self.leftdoor, batch=self.Batch["office"], group=self.Layers[1])

        self.rightdoor = gameObjects.Door(True, x=1270, y=0, batch=self.Batch["office"], group=self.Layers[1])
        self.rightbutton = gameObjects.Button(True, x=1500, y=180, door=self.rightdoor, batch=self.Batch["office"], group=self.Layers[1])

        self.background = gameObjects.Sprite("images\\office\\0.png", 0, 0, self.Batch["common"], self.Layers[0])
        self.camerabutton = gameObjects.Sprite("images\\ui\\button\\camera.png")

        self.push_handlers(self.leftbutton.on_mouse_press)
        self.push_handlers(self.rightbutton.on_mouse_press)



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
                    i.x += int(300 * dt)
                    i.update(dt)

                self.moving = "left"

            if self.mouse_x in range(151, 315) and not self.GameObjects["background"].x >= 0.0:
                for i in self.GameObjects.values():
                    i.x += int(200 * dt)
                    i.update(dt)

                self.moving = "left"

            if self.mouse_x in range(316, 540) and not self.GameObjects["background"].x >= 0.0:
                for i in self.GameObjects.values():
                    i.x += int(100 * dt)
                    i.update(dt)

                self.moving = "left"


            if self.mouse_x in range(1140, 1280) and not self.GameObjects["background"].x <= -315:
                for i in self.GameObjects.values():
                    i.x -= int(300 * dt)
                    i.update(dt)

                self.moving = "right"

            if self.mouse_x in range(1000, 1139) and not self.GameObjects["background"].x <= -315:
                for i in self.GameObjects.values():
                    i.x -= int(200 * dt)
                    i.update(dt)

                self.moving = "right"

            if self.mouse_x in range(750, 999) and not self.GameObjects["background"].x <= -315:
                for i in self.GameObjects.values():
                    i.x -= int(100 * dt)
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

            if scene == CAMERA:
                pass

            self.moving = "left"
            self.GameObjects["background"].x, self.GameObjects["background"].y = 0, 0
            self.scene = scene

        else:
            raise ValueError("Unknown scene '%s'." % (scene))
