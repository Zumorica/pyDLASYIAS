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
        self.camera = "cam1a"

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

        self.Backgrounds = {"office" : {"0" : pyglet.image.load("images\\office\\0.png"),
                                        "1" : pyglet.image.load("images\\office\\1.png"),
                                        "2" : pyglet.image.load("images\\office\\2.png"),
                                        "r" : pyglet.image.load("images\\office\\r.png"),
                                        "c" : pyglet.image.load("images\\office\\c.png")},
                            "camera" : {"cam1a" : {"0" : pyglet.image.load("images\\cameras\\cam1a\\0.png"),
                                                   "b" : pyglet.image.load("images\\cameras\\cam1a\\b.png"),
                                                   "b-1" : pyglet.image.load("images\\cameras\\cam1a\\b-1.png"),
                                                   "bc" : pyglet.image.load("images\\cameras\\cam1a\\bc.png"),
                                                   "br" : pyglet.image.load("images\\cameras\\cam1a\\br.png"),
                                                   "brc" : pyglet.image.load("images\\cameras\\cam1a\\brc.png"),
                                                   "brc-1" : pyglet.image.load("images\\cameras\\cam1a\\brc-1.png")},
                                        "cam1b" : {"0" : pyglet.image.load("images\\cameras\\cam1b\\0.png"),
                                                   "b" : pyglet.image.load("images\\cameras\\cam1b\\b.png"),
                                                   "c" : pyglet.image.load("images\\cameras\\cam1b\\c.png"),
                                                   "c-1" : pyglet.image.load("images\\cameras\\cam1b\\c-1.png"),
                                                   "r" : pyglet.image.load("images\\cameras\\cam1b\\r.png"),
                                                   "r-1" : pyglet.image.load("images\\cameras\\cam1b\\r-1.png")},
                                        "cam1c" : {"0" : pyglet.image.load("images\\cameras\\cam1c\\0.png"),
                                                   "1" : pyglet.image.load("images\\cameras\\cam1c\\1.png"),
                                                   "2" : pyglet.image.load("images\\cameras\\cam1c\\2.png"),
                                                   "3" : pyglet.image.load("images\\cameras\\cam1c\\3.png"),
                                                   "4" : pyglet.image.load("images\\cameras\\cam1c\\4.png"),
                                                   "5" : pyglet.image.load("images\\cameras\\cam1c\\5.png")},
                                        "cam2a" : {"0" : pyglet.image.load("images\\cameras\\cam2a\\0.png"),
                                                   "1" : pyglet.image.load("images\\cameras\\cam2a\\1.png"),
                                                   "r" : pyglet.image.load("images\\cameras\\cam2a\\1.png")},
                                        "cam2b" : {"0" : pyglet.image.load("images\\cameras\\cam2b\\0.png"),
                                                   "1" : pyglet.image.load("images\\cameras\\cam2b\\1.png"),
                                                   "2" : pyglet.image.load("images\\cameras\\cam2b\\2.png"),
                                                   "r" : pyglet.image.load("images\\cameras\\cam2b\\r.png"),
                                                   "r-1" : pyglet.image.load("images\\cameras\\cam2b\\r-1.png")},
                                        "cam3" : {"0" : pyglet.image.load("images\\cameras\\cam3\\0.png"),
                                                  "r" : pyglet.image.load("images\\cameras\\cam3\\r.png")},
                                        "cam4a" : {"0" : pyglet.image.load("images\\cameras\\cam4a\\0.png"),
                                                   "1" : pyglet.image.load("images\\cameras\\cam4a\\1.png"),
                                                   "2" : pyglet.image.load("images\\cameras\\cam4a\\2.png"),
                                                   "b" : pyglet.image.load("images\\cameras\\cam4a\\b.png"),
                                                   "c" : pyglet.image.load("images\\cameras\\cam4a\\c.png"),
                                                   "c-1" : pyglet.image.load("images\\cameras\\cam4a\\c-1.png")},
                                        "cam4b" : {"0" : pyglet.image.load("images\\cameras\\cam4b\\0.png"),
                                                   "1" : pyglet.image.load("images\\cameras\\cam4b\\1.png"),
                                                   "2" : pyglet.image.load("images\\cameras\\cam4b\\2.png"),
                                                   "3" : pyglet.image.load("images\\cameras\\cam4b\\3.png"),
                                                   "4" : pyglet.image.load("images\\cameras\\cam4b\\4.png"),
                                                   "b" : pyglet.image.load("images\\cameras\\cam4b\\b.png"),
                                                   "c" : pyglet.image.load("images\\cameras\\cam4b\\c.png"),
                                                   "c-1" : pyglet.image.load("images\\cameras\\cam4b\\c-1.png"),
                                                   "c-2" : pyglet.image.load("images\\cameras\\cam4b\\c-2.png")},
                                        "cam5" : {"0" : pyglet.image.load("images\\cameras\\cam5\\0.png"),
                                                  "1" : pyglet.image.load("images\\cameras\\cam5\\1.png"),
                                                  "r" : pyglet.image.load("images\\cameras\\cam5\\r.png"),
                                                  "r-1" : pyglet.image.load("images\\cameras\\cam5\\r-1.png")},
                                        "cam6" : {"0" : pyglet.image.load("images\\cameras\\misc\\black.png")},
                                        "cam7" : {"0" : pyglet.image.load("images\\cameras\\cam7\\0.png"),
                                                  "b" : pyglet.image.load("images\\cameras\\cam7\\b.png"),
                                                  "c" : pyglet.image.load("images\\cameras\\cam7\\c.png"),
                                                  "c-1" : pyglet.image.load("images\\cameras\\cam7\\c-1.png")}}}

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

        self.fps.draw()

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
        pyglet.clock.set_fps_limit(60)
        self.cam1a = gameObjects.Camera("cam1a", "images\\ui\\button\\camera\\1a.png", 963, 387, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam1b = gameObjects.Camera("cam1b", "images\\ui\\button\\camera\\1b.png", 943, 331, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam1c = gameObjects.Camera("cam1c", "images\\ui\\button\\camera\\1c.png", 901, 253, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam2a = gameObjects.Camera("cam2a", "images\\ui\\button\\camera\\2a.png", 954, 146, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam2b = gameObjects.Camera("cam2b", "images\\ui\\button\\camera\\2b.png", 954, 104, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam3 = gameObjects.Camera("cam3", "images\\ui\\button\\camera\\3.png", 877, 146, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam4a = gameObjects.Camera("cam4a", "images\\ui\\button\\camera\\4a.png", 1060, 146, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam4b = gameObjects.Camera("cam4b", "images\\ui\\button\\camera\\4b.png", 1060, 104, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam5 = gameObjects.Camera("cam5", "images\\ui\\button\\camera\\5.png", 817, 304, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam6 = gameObjects.Camera("cam6", "images\\ui\\button\\camera\\6.png", 1163, 164, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.cam7 = gameObjects.Camera("cam7", "images\\ui\\button\\camera\\7.png", 1172, 296, batch=self.Batch["camera"], group=self.Layers[3], grouptwo=self.Layers[4])
        self.map = gameObjects.Sprite("images\\ui\\map-0.png", 848, 47, batch=self.Batch["camera"], group=self.Layers[1])
        self.static = gameObjects.Static(70, 160, batch=self.Batch["camera"], group=self.Layers[2])
        self.tablet = gameObjects.Tablet(batch=self.Batch["office"], group=self.Layers[5])

        pyglet.font.add_file('FNAF.ttf')
        self.font = pyglet.font.load("Five Nights at Freddy's")
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
        self.fps = pyglet.clock.ClockDisplay()

        self.setup_office()
        pyglet.clock.schedule(self.cam1a.update)
        pyglet.clock.schedule(self.cam1b.update)
        pyglet.clock.schedule(self.cam1c.update)
        pyglet.clock.schedule(self.cam2a.update)
        pyglet.clock.schedule(self.cam2b.update)
        pyglet.clock.schedule(self.cam3.update)
        pyglet.clock.schedule(self.cam4a.update)
        pyglet.clock.schedule(self.cam4b.update)
        pyglet.clock.schedule(self.cam5.update)
        pyglet.clock.schedule(self.cam6.update)
        pyglet.clock.schedule(self.cam7.update)
        pyglet.clock.schedule(self.static.update)
        pyglet.clock.schedule(self.tablet.update)
        pyglet.clock.schedule(self.leftdoor.update)
        pyglet.clock.schedule(self.leftbutton.update)
        pyglet.clock.schedule(self.rightdoor.update)
        pyglet.clock.schedule(self.rightbutton.update)
        pyglet.clock.schedule(self.background.update)
        pyglet.clock.schedule(self.scenebutton.update)
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
            self.tablet.visible = True
            if self.scene == "office":
                self.tablet.image.batch = self.Batch["office"]
                self.tablet.open()

            if self.scene == "camera":
                self.tablet.image.batch = self.Batch["camera"]
                self.tablet.close()

        @self.tablet.event
        def on_animation_end():
            self.tablet.visible = False
            if self.scene == "office":
                self.scene = "camera"
                self.setup_camera()

            elif self.scene == "camera":
                self.scene = "office"
                self.setup_office()
            pyglet.clock.schedule_once(self.scenebutton.showImage, 2)

        @self.cam1a.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam1a.pressed = True
            self.camera = "cam1a"

        @self.cam1b.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam1b.pressed = True
            self.camera = "cam1b"

        @self.cam1c.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam1c.pressed = True
            self.camera = "cam1c"

        @self.cam2a.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam2a.pressed = True
            self.camera = "cam2a"

        @self.cam2b.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam2b.pressed = True
            self.camera = "cam2b"

        @self.cam3.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam3.pressed = True
            self.camera = "cam3"

        @self.cam4a.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam4a.pressed = True
            self.camera = "cam4a"

        @self.cam4b.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam4b.pressed = True
            self.camera = "cam4b"

        @self.cam5.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam5.pressed = True
            self.camera = "cam5"

        @self.cam6.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam6.pressed = True
            self.camera = "cam6"

        @self.cam7.event
        def on_camera_press(camera):
            for i in self.CamButtons.values():
                i.pressed = False
            self.cam7.pressed = True
            self.camera = "cam7"

    def setup_office(self):
        '''Office setup.'''
        try:
            self.pop_handlers()
        except AssertionError:
            pass

        self.background.image.opacity = self.power * 2.55
        self.background.image.x, self.background.image.y = self.old_x, self.old_y
        self.tablet.image.visible = False
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
        self.scene = "office"

    def setup_camera(self):
        '''Camera setup.'''
        self.pop_handlers()
        self.background.image.opacity = 255
        self.old_X, self.old_y = self.background.x, self.background.y
        self.GameObjects.clear()
        self.GameObjects = self.CameraButtons.copy()
        self.GameObjects["background"] = self.background
        self.GameObjects["static"] = self.static

        self.background.image.batch = self.Batch["camera"]
        self.scenebutton.image.batch = self.Batch["camera"]

        self.push_handlers(self.scenebutton.on_mouse_motion)
        self.push_handlers(self.cam1a.on_mouse_press)
        self.push_handlers(self.cam1b.on_mouse_press)
        self.push_handlers(self.cam1c.on_mouse_press)
        self.push_handlers(self.cam2a.on_mouse_press)
        self.push_handlers(self.cam2b.on_mouse_press)
        self.push_handlers(self.cam3.on_mouse_press)
        self.push_handlers(self.cam4a.on_mouse_press)
        self.push_handlers(self.cam4b.on_mouse_press)
        self.push_handlers(self.cam5.on_mouse_press)
        self.push_handlers(self.cam6.on_mouse_press)
        self.push_handlers(self.cam7.on_mouse_press)
        self.scene = "camera"

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

            if not self.leftbutton.light and not self.rightbutton.light:
                self.background.change_image(self.Backgrounds["office"]["0"])

            if self.leftbutton.light and not self.rightbutton.light:
                self.background.change_image(self.Backgrounds["office"]["1"])

            if not self.leftbutton.light and self.rightbutton.light:
                self.background.change_image(self.Backgrounds["office"]["2"])

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
            if self.moving == "left" and not self.GameObjects["background"].x <= 0:
                self.GameObjects["background"].x -= int(500 * dt)

            if self.moving == "right" and not self.GameObjects["background"].x <= 320:
                self.GameObjects["background"].x += int(500 * dt)

            if self.GameObjects["background"].x >= 0.0:
                self.moving = "right"

            if self.GameObjects["background"].x <= -315:
                self.moving = "left"

            if self.camera == "cam1a":
                self.background.image.delete()
                self.background.image = pyglet.sprite.Sprite(self.Backgrounds["camera"]["cam1a"]["brc"], x=self.background.x, y=self.background.y, batch=self.background.batch, group=self.background.group)

            elif self.camera == "cam1b":
                self.background.image.delete()
                self.background.image = pyglet.sprite.Sprite(self.Backgrounds["camera"]["cam1a"]["brc"], x=self.background.x, y=self.background.y, batch=self.background.batch, group=self.background.group)

if __name__ == "__main__":
    print("Run game.py")
    sys.exit(0)

else:
    Main.register_event_type("on_button_press")
