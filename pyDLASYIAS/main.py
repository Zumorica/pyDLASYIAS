import pyglet
import time
import sys
import os
from pyglet.gl import *
from pyglet.gl.glu import *
import pyDLASYIAS.gameObjects as gameObjects

class Main(pyglet.window.Window):
    '''Docstring WIP'''
    def __init__(self):
        '''Docstring WIP'''

        super().__init__(width=1280, height=720)

        self.hour = 0
        self.power = 100
        self.scene = "office"

        self.GameObjects = {}
        self.CameraButtons = {}

        self.Batch = {"common" : pyglet.graphics.Batch(),
                      "office" : pyglet.graphics.Batch(),
                      "camera" : pyglet.graphics.Batch(),
                      "ui"     : pyglet.graphics.Batch()}

        self.Layers = [pyglet.graphics.OrderedGroup(0),
                       pyglet.graphics.OrderedGroup(1),
                       pyglet.graphics.OrderedGroup(2),
                       pyglet.graphics.OrderedGroup(3),
                       pyglet.graphics.OrderedGroup(4),
                       pyglet.graphics.OrderedGroup(5)]

        self.mouse_x, self.mouse_y = 0, 0
        self.mouse_Click = False
        self.moving = "right"
        self.old_x, self.old_y = 0, 0

        glEnable(GL_TEXTURE_2D)

        self.setup()

    def on_draw(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()

        if self.scene == "office":
            self.Batch["office"].draw()
            self.Batch["ui"].draw()

        if self.scene == "camera":
            self.Batch["camera"].draw()
            self.Batch["ui"].draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x, self.mouse_y = x, y

    def on_mouse_press(self, x, y, button, modifier):
        if button == 1:
            self.mouse_x, self.mouse_y = x, y
            self.mouse_Click = True

    def on_mouse_release(self, x, y, button, modifier):
        if button == 1:
            self.mouse_x, self.mouse_y = x, y
            self.mouse_Click = False

    def setup(self):
        '''Initial setup.'''
        self.cam1a = gameObjects.Camera("cam1a", "images\\ui\\button\\camera\\1a.png", 983, 353, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])

        pyglet.font.add_file('FNAF.ttf')
        self.font = pyglet.font.load("Five Nights at Freddy's")
        self.CamButtons = {"cam1a" : self.cam1a,
                           "cam1b" : gameObjects.Camera("cam1b", "images\\ui\\button\\camera\\1b.png", 963, 409, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam1c" : gameObjects.Camera("cam1c", "images\\ui\\button\\camera\\1c.png", 931, 487, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam2a" : gameObjects.Camera("cam2a", "images\\ui\\button\\camera\\2a.png", 954, 574, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam2b" : gameObjects.Camera("cam2b", "images\\ui\\button\\camera\\2b.png", 956, 626, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam3" : gameObjects.Camera("cam3", "images\\ui\\button\\camera\\3.png", 877, 574, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam4a" : gameObjects.Camera("cam4a", "images\\ui\\button\\camera\\4a.png", 1060, 574, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam4b" : gameObjects.Camera("cam4b", "images\\ui\\button\\camera\\4b.png", 1060, 636, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam5" : gameObjects.Camera("cam5", "images\\ui\\button\\camera\\5.png", 857, 436, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam6" : gameObjects.Camera("cam6", "images\\ui\\button\\camera\\6.png", 1163, 556, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4]),
                           "cam7" : gameObjects.Camera("cam7", "images\\ui\\button\\camera\\7.png", 1172, 424, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])}
        self.leftdoor = gameObjects.Door(False, x=72, y=0, batch=self.Batch["office"], group=self.Layers[1])
        self.leftbutton = gameObjects.Button(False, x=0, y=180, door=self.leftdoor, batch=self.Batch["office"], group=self.Layers[1])
        self.rightdoor = gameObjects.Door(True, x=1270, y=0, batch=self.Batch["office"], group=self.Layers[1])
        self.rightbutton = gameObjects.Button(True, x=1500, y=180, door=self.rightdoor, batch=self.Batch["office"], group=self.Layers[1])
        self.background = gameObjects.Sprite("images\\office\\0.png", 0, 0, self.Batch["office"], self.Layers[0])
        self.scenebutton = gameObjects.SceneButton(x=self.width//4, y=36, batch=self.Batch["office"], group=self.Layers[1])
        self.powerlabel = pyglet.text.Label("Power left:  "+str(self.power), font_name="Five Nights at Freddy's", font_size=16, x=40, y=200, batch=self.Batch["ui"], group=self.Layers[5])
        self.usagelabel = pyglet.text.Label("Usage:", font_name="Five Nights at Freddy's", font_size=16, x=40, y=170, batch=self.Batch["ui"], group=self.Layers[5])
        self.hourlabel = pyglet.text.Label(str(self.hour)+"  AM", font_name="Five Nights at Freddy's", font_size=16, x=1020, y=640, batch=self.Batch["ui"], group=self.Layers[5])
        self.nightlabel = pyglet.text.Label("pyDLASYIAS_GL", font_name="Five Nights at Freddy's", font_size=16, x=1020, y=670, batch=self.Batch["ui"], group=self.Layers[5])

        self.setup_office()
        pyglet.clock.schedule(self.update)

        @self.leftbutton.event
        def on_button_press(button, state):
            if self.scene == "office":
                if button == "light":
                    if state == True and self.rightbutton.light:
                        self.rightbutton.light = False

        @self.rightbutton.event
        def on_button_press(button, state):
            if self.scene == "office":
                if button == "light":
                    if state == True and self.leftbutton.light:
                        self.leftbutton.light = False

        @self.scenebutton.event
        def on_button_collide():
            if self.scene == "office":
                self.scene = "camera"
                self.setup_camera()

            elif self.scene == "camera":
                self.scene = "office"
                self.setup_office()

    def setup_office(self):
        '''Office setup.'''
        try:
            self.pop_handlers()
        except AssertionError:
            pass

        self.background.x, self.background.y = self.old_x, self.old_y

        for i in self.GameObjects.values():
            pyglet.clock.unschedule(i.update)

        self.GameObjects.clear()
        self.GameObjects["leftbutton"] = self.leftbutton
        self.GameObjects["rightbutton"] = self.rightbutton
        self.GameObjects["leftdoor"] = self.leftdoor
        self.GameObjects["rightdoor"] = self.rightdoor
        self.GameObjects["background"] = self.background
        self.GameObjects["SceneButton"] = self.scenebutton

        self.background.batch = self.Batch["office"]
        self.scenebutton.batch = self.Batch["office"]

        self.push_handlers(self.scenebutton.on_mouse_motion)
        self.push_handlers(self.leftbutton.on_mouse_press)
        self.push_handlers(self.rightbutton.on_mouse_press)
        for i in self.GameObjects.values():
            pyglet.clock.schedule(i.update)
        self.scene = "office"

    def setup_camera(self):
        '''Camera setup.'''
        self.pop_handlers()
        self.background.image.opacity = 255
        self.old_X, self.old_y = self.background.x, self.background.y
        for i in self.GameObjects.values():
            pyglet.clock.unschedule(i.update)
        self.GameObjects.clear()
        self.GameObjects = self.CameraButtons.copy()
        self.GameObjects["background"] = self.background

        self.background.batch = self.Batch["camera"]
        self.scenebutton.batch = self.Batch["camera"]

        self.push_handlers(self.scenebutton.on_mouse_motion)
        self.push_handlers(self.cam1a.on_mouse_press)
        for i in self.CameraButtons.values():
            self.push_handlers(i.on_mouse_press)
            @item.event
            def on_camera_press(self, camera):
                self.camera = camera

        self.scene = "camera"

    def resetCameraSprites(self):
        for item in self.CameraButtons.values():
            if item.name != self.camera:
                item.change_image("images\\ui\\button\\camera\\0.png")

    def update(self, dt):
        if self.scene == "office":
            self.background.image.opacity = self.power * 2.55
            self.leftbutton.image.opacity = self.power * 2.55
            self.rightbutton.image.opacity = self.power * 2.55
            self.leftdoor.image.opacity = self.power * 2.55
            self.rightdoor.image.opacity = self.power * 2.55

            if self.hour == 0:
                self.hourlabel.text = "12  PM"
            else:
                self.hourlabel.text = "%s  AM" %(self.hour)

            self.powerlabel.text = "Power left:  %s" %(self.power)
            self.usagelabel = "Usage: "

            try:
                if self.mouse_x in range(0, 150) and not self.GameObjects["background"].x >= 0.0:
                    for i in self.GameObjects.values():
                        if i.movable:
                            i.x += int(600 * dt)
                            i.update(dt)

                    self.moving = "left"

                if self.mouse_x in range(151, 315) and not self.GameObjects["background"].x >= 0.0:
                    for i in self.GameObjects.values():
                        if i.movable:
                            i.x += int(400 * dt)
                            i.update(dt)

                    self.moving = "left"

                if self.mouse_x in range(316, 540) and not self.GameObjects["background"].x >= 0.0:
                    for i in self.GameObjects.values():
                        if i.movable:
                            i.x += int(200 * dt)
                            i.update(dt)

                    self.moving = "left"


                if self.mouse_x in range(1140, 1280) and not self.GameObjects["background"].x <= -315:
                    for i in self.GameObjects.values():
                        if i.movable:
                            i.x -= int(600 * dt)
                            i.update(dt)

                    self.moving = "right"

                if self.mouse_x in range(1000, 1139) and not self.GameObjects["background"].x <= -315:
                    for i in self.GameObjects.values():
                        if i.movable:
                            i.x -= int(400 * dt)
                            i.update(dt)

                    self.moving = "right"

                if self.mouse_x in range(750, 999) and not self.GameObjects["background"].x <= -315:
                    for i in self.GameObjects.values():
                        if i.movable:
                            i.x -= int(200 * dt)
                            i.update(dt)

                    self.moving = "right"
            except KeyError:
                #Probably scene has changed.
                pass

        if self.scene == "camera":
            if self.moving == "left" and not self.GameObjects["background"].x >= 0:
                self.GameObjects["background"].x -= int(500 * dt)

            if self.moving == "right" and not self.GameObjects["background"].x <= -315:
                self.GameObjects["background"].x += int(500 * dt)

            if self.GameObjects["background"].x >= 0.0:
                self.moving = "right"

            if self.GameObjects["background"].x <= -315:
                self.moving = "left"

if __name__ == "__main__":
    print("Run game.py")
    sys.exit(0)

else:
    Main.register_event_type("on_button_press")
