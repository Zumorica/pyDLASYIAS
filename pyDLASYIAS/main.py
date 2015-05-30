import pyglet
import os
import pyDLASYIAS.gameObjects as gameObjects
from pyglet.gl import *

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

        self.Sprites = {}
        self.GameObjects = {}
        self.Layers = [pyglet.graphics.OrderedGroup(0),
                       pyglet.graphics.OrderedGroup(1),
                       pyglet.graphics.OrderedGroup(2),
                       pyglet.graphics.OrderedGroup(3)]
        self.Batch = {"common" : pyglet.graphics.Batch(),
                      "office" : pyglet.graphics.Batch(),
                      "camera" : pyglet.graphics.Batch()}

        super().__init__(width=1280, height=720)

        pyglet.clock.schedule(self.update)

        self.setup_sprites()
        self.setup_gameobjects()

    def setup_sprites(self):

        self.Sprites["background"] = pyglet.sprite.Sprite(pyglet.image.load('images\\office\\0.png'),
                                                          0, 0, batch=self.Batch["common"], group=self.Layers[0])

    def setup_gameobjects(self):
        self.leftdoor = gameObjects.Door(False, batch=self.Batch["office"], group=self.Layers[1])
        self.leftbutton = gameObjects.Button(False, self, batch=self.Batch["office"], group=self.Layers[1])

        self.rightdoor = gameObjects.Door(True, batch=self.Batch["office"], group=self.Layers[1])
        self.rightbutton = gameObjects.Button(True, self.rightdoor, batch=self.Batch["office"], group=self.Layers[1])

        self.push_handlers(self.leftbutton.on_mouse_press, self.rightbutton.on_mouse_press)

        self.GameObjects["leftbutton"] = self.leftbutton
        self.GameObjects["rightbutton"] = self.rightbutton
        self.GameObjects["leftdoor"] = self.leftdoor
        self.GameObjects["rightdoor"] = self.rightdoor

    def on_draw(self):
        if self.scene == OFFICE:
            self.Batch["common"].draw()
            self.Batch["office"].draw()

        if self.scene == CAMERA:
            self.Batch["common"].draw()
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
        for key, value in self.GameObjects.items():
            value.update(dt)
