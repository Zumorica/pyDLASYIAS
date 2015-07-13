import pyglet
import random
import cocos
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
        self.usage = 1
        self.scene = "office"
        self.camera = "cam1a"

        self.GameObjects = {}
        self.CameraButtons = {}

        self.Batch = {"common" : pyglet.graphics.Batch(),
                      "office" : pyglet.graphics.Batch(),
                      "camera" : pyglet.graphics.Batch(),
                      "powerout" : pyglet.graphics.Batch(),
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
                                                  "c-1" : pyglet.image.load("images\\cameras\\cam7\\c-1.png")}},
                            "powerout" : {"0" : pyglet.image.load("images\\office\\powerout\\0.png"),
                                          "1" : pyglet.image.load("images\\office\\powerout\\1.png"),
                                          "2" : pyglet.image.load("images\\office\\powerout\\2.png")}}

        self.Sounds = {"ambience" : {"ambience" : pyglet.media.load("sounds\\ambience\\ambience.wav"),
                                     "ambience2" : pyglet.media.load("sounds\\ambience\\ambience2.wav"),
                                     "eerieambience" : pyglet.media.load("sounds\\ambience\\eerieambience.wav"),
                                     "fan" : pyglet.media.load("sounds\\ambience\\fan.wav")},

                       "camera" : {"blip" : pyglet.media.load("sounds\\camera\\blip.wav"),
                                   "camerasound" : pyglet.media.load("sounds\\camera\\camerasound.wav"),
                                   "camerasound2" : pyglet.media.load("sounds\\camera\\camerasound2.wav"),
                                   "computernoise" : pyglet.media.load("sounds\\camera\\computernoise.wav"),
                                   "deepsteps" : pyglet.media.load("sounds\\camera\\deepsteps.wav"),
                                   "garble" : pyglet.media.load("sounds\\camera\\garble.wav"),
                                   "garble2" : pyglet.media.load("sounds\\camera\\garble2.wav"),
                                   "garble3" : pyglet.media.load("sounds\\camera\\garble3.wav"),
                                   "piratesong" : pyglet.media.load("sounds\\camera\\piratesong.wav"),
                                   "pots" : pyglet.media.load("sounds\\camera\\pots.wav"),
                                   "pots2" : pyglet.media.load("sounds\\camera\\pots2.wav"),
                                   "pots3" : pyglet.media.load("sounds\\camera\\pots3.wav"),
                                   "pots4" : pyglet.media.load("sounds\\camera\\pots4.wav"),
                                   "putdown" : pyglet.media.load("sounds\\camera\\putdown.wav"),
                                   "run" : pyglet.media.load("sounds\\camera\\run.wav"),
                                   "runningfast" : pyglet.media.load("sounds\\camera\\runningfast.wav"),
                                   "static" : pyglet.media.load("sounds\\camera\\static.wav"),
                                   "static2" : pyglet.media.load("sounds\\camera\\static2.wav")},

                       "misc" : {"6AM" : pyglet.media.load("sounds\\misc\\6AM.wav"),
                                 "children" : pyglet.media.load("sounds\\misc\\children.wav"),
                                 "circus" : pyglet.media.load("sounds\\misc\\circus.wav"),
                                 "door" : pyglet.media.load("sounds\\misc\\door.wav"),
                                 "doorknocking" : pyglet.media.load("sounds\\misc\\doorknocking.wav"),
                                 "doorpounding" : pyglet.media.load("sounds\\misc\\doorpounding.wav"),
                                 "error" : pyglet.media.load("sounds\\misc\\error.wav"),
                                 "honk" : pyglet.media.load("sounds\\misc\\honk.wav"),
                                 "lighthum" : pyglet.media.load("sounds\\misc\\lighthum.wav"),
                                 "musicbox" : pyglet.media.load("sounds\\misc\\musicbox.wav"),
                                 "powerout" : pyglet.media.load("sounds\\misc\\powerout.wav"),
                                 "robotvoice" : pyglet.media.load("sounds\\misc\\robotvoice.wav")},

                       "scary" : {"breathing" : pyglet.media.load("sounds\\scary\\breathing.wav"),
                                  "breathing2" : pyglet.media.load("sounds\\scary\\breathing2.wav"),
                                  "breathing3" :    pyglet.media.load("sounds\\scary\\breathing3.wav"),
                                  "breathing4" : pyglet.media.load("sounds\\scary\\breathing4.wav"),
                                  "freddygiggle" : pyglet.media.load("sounds\\scary\\freddygiggle.wav"),
                                  "freddygiggle2" : pyglet.media.load("sounds\\scary\\freddygiggle2.wav"),
                                  "freddygiggle3" : pyglet.media.load("sounds\\scary\\freddygiggle3.wav"),
                                  "giggle" : pyglet.media.load("sounds\\scary\\giggle.wav"),
                                  "robotvoice" : pyglet.media.load("sounds\\scary\\robotvoice.wav"),
                                  "windowscare" : pyglet.media.load("sounds\\scary\\windowscare.wav"),
                                  "XSCREAM" : pyglet.media.load("sounds\\scary\\XSCREAM.wav"),
                                  "XSCREAM2" : pyglet.media.load("sounds\\scary\\XSCREAM2.wav")}}

        self.Channel = [pyglet.media.Player() for x in range(0, 31)]

        self.mouse_x, self.mouse_y = 0, 0
        self.mouse_Click = False
        self.moving = "right"
        self.old_x, self.old_y = 0, 0
        self.powerout_stage = 1
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1280, 0, 720, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_TEXTURE_2D)
        self.setup()

    def on_draw(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.scene == "office":
            self.Batch["office"].draw()
            self.Batch["ui"].draw()

        if self.scene == "camera":
            self.Batch["camera"].draw()
            self.Batch["ui"].draw()

        if self.scene == "powerout":
            self.Batch["powerout"].draw()

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

    def power_calculations(self, dt=None, old_usage=1):
        if self.power >= 0:
            if self.usage == 1:
                if old_usage == 1:
                    self.power -= 1

                if old_usage == 2:
                    self.power -= 2

                if old_usage == 3:
                    self.power -= 2

                if old_usage == 4:
                    self.power -= 2

                pyglet.clock.schedule_once(self.power_calculations, 9.6, old_usage=1)

            if self.usage == 2:
                if old_usage == 1:
                    self.power -= 1

                if old_usage == 2:
                    self.power -= 1

                if old_usage == 3:
                    self.power -= 2

                if old_usage == 4:
                    self.power -= 2

                pyglet.clock.schedule_once(self.power_calculations, 4.8, old_usage=2)

            if self.usage == 3:
                if old_usage == 1:
                    self.power -= 1

                if old_usage == 2:
                    self.power -= 1

                if old_usage == 3:
                    self.power -= 1

                if old_usage == 4:
                    self.power -= 2

                pyglet.clock.schedule_once(self.power_calculations, random.choice([2.8, 2.9, 3.9]), old_usage=3)

            if self.usage == 4:
                self.power -= 1

                pyglet.clock.schedule_once(self.power_calculations, random.choice([1.9, 2.9]), old_usage=4)

            if self.usage == 5:
                self.usage = 4
                self.power -= 1

                pyglet.clock.schedule_once(self.power_calculations, random.choice([1.9, 2.9]), old_usage=4)

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
        self.powerlabel = pyglet.text.Label("Power left:  "+str(self.power)+"%", font_name="Five Nights at Freddy's", font_size=16, x=40, y=150, batch=self.Batch["ui"], group=self.Layers[5])
        self.usagelabel = pyglet.text.Label("Usage:"+str(self.usage), font_name="Five Nights at Freddy's", font_size=16, x=40, y=120, batch=self.Batch["ui"], group=self.Layers[5])
        self.hourlabel = pyglet.text.Label(str(self.hour)+"  AM", font_name="Five Nights at Freddy's", font_size=16, x=1020, y=640, batch=self.Batch["ui"], group=self.Layers[5])
        self.nightlabel = pyglet.text.Label("pyDLASYIAS_GL", font_name="Five Nights at Freddy's", font_size=16, x=1020, y=670, batch=self.Batch["ui"], group=self.Layers[5])
        self.fps = pyglet.clock.ClockDisplay()
        self.cam1a.pressed = True

        self.power_calculations(1)
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


        for channel in self.Channel:
            channel.eos_action = channel.EOS_LOOP

        channel10_sourcegroup = pyglet.media.SourceGroup(pyglet.media.AudioFormat(1, 16, 22050), None)
        channel10_sourcegroup.loop = True
        channel10_sourcegroup.queue(self.Sounds["camera"]["garble"])
        channel10_sourcegroup.queue(self.Sounds["camera"]["garble2"])
        channel10_sourcegroup.queue(self.Sounds["camera"]["garble3"])

        channel11_sourcegroup = pyglet.media.SourceGroup(pyglet.media.AudioFormat(1, 16, 22050), None)
        channel11_sourcegroup.loop = True
        channel11_sourcegroup.queue(self.Sounds["camera"]["pots"])
        channel11_sourcegroup.queue(self.Sounds["camera"]["pots2"])
        channel11_sourcegroup.queue(self.Sounds["camera"]["pots3"])
        channel11_sourcegroup.queue(self.Sounds["camera"]["pots4"])

        self.Channel[0].queue(self.Sounds["misc"]["powerout"])
        self.Channel[1].queue(self.Sounds["ambience"]["fan"])
        self.Channel[2].queue(self.Sounds["ambience"]["ambience"])
        self.Channel[3].queue(self.Sounds["misc"]["lighthum"])
        self.Channel[4].queue(self.Sounds["misc"]["door"])
        self.Channel[7].queue(self.Sounds["camera"]["camerasound2"])
        self.Channel[9].queue(self.Sounds["scary"]["XSCREAM"])
        self.Channel[10].queue(channel10_sourcegroup)
        self.Channel[11].queue(channel11_sourcegroup)
        self.Channel[18].queue(self.Sounds["ambience"]["eerieambience"])
        self.Channel[21].queue(self.Sounds["scary"]["robotvoice"])
        self.Channel[30].queue(self.Sounds["misc"]["musicbox"])

        self.Channel[0].eos_action = self.Channel[0].EOS_PAUSE
        self.Channel[4].eos_action = self.Channel[4].EOS_PAUSE
        self.Channel[9].eos_action = self.Channel[9].EOS_PAUSE
        self.Channel[30].eos_action = self.Channel[30].EOS_PAUSE


        @self.leftbutton.event
        def on_button_press(button, state):
            if self.scene == "office":
                if button == "light":
                    if state == True and self.rightbutton.light:
                        self.rightbutton.light = False

                    elif state == True and not self.rightbutton.light:
                        self.Channel[3].play()
                        self.Channel[3].volume = 1.0
                        self.usage += 1

                    elif state == False and not self.rightbutton.light:
                        self.Channel[3].volume = 0.0
                        self.usage -= 1

                if button == "door":
                    try:
                        self.Channel[4].seek(0)
                        self.Channel[4].play()
                    except:
                        pass
                    if state == True:
                        self.usage += 1

                    if state == False:
                        self.usage -= 1

        @self.rightbutton.event
        def on_button_press(button, state):
            if self.scene == "office":
                if button == "light":
                    if state == True and self.leftbutton.light:
                        self.leftbutton.light = False

                    elif state == True and not self.leftbutton.light:
                        self.Channel[3].play()
                        self.Channel[3].volume = 1.0
                        self.usage += 1

                    elif state == False and not self.leftbutton.light:
                        self.Channel[3].volume = 0.0
                        self.usage -= 1

                if button == "door":
                    try:
                        self.Channel[4].seek(0)
                        self.Channel[4].play()
                    except:
                        pass
                    if state == True:
                        self.usage += 1

                    if state == False:
                        self.usage -= 1

        @self.scenebutton.event
        def on_button_collide():
            if self.tablet.image.visible != True:
                self.tablet.image.visible = True
                if self.scene == "office":
                    self.tablet.batch = self.Batch["office"]
                    self.tablet.open()
                    self.usage += 1
                    if self.leftbutton.light:
                        self.leftbutton.light = False
                        self.usage -= 1

                    if self.rightbutton.light:
                        self.rightbutton.light = False
                        self.usage -= 1

                    return pyglet.event.EVENT_HANDLED

                elif self.scene == "camera":
                    self.scene = "office"
                    self.setup_office()
                    self.tablet.batch = self.Batch["office"]
                    self.tablet.close()
                    self.usage -= 1
                    return pyglet.event.EVENT_HANDLED

        @self.tablet.event
        def on_animation_end():
            self.tablet.image.visible = False
            if self.scene == "office" and not self.tablet.isClosed:
                self.scene = "camera"
                self.setup_camera()
                return pyglet.event.EVENT_HANDLED

            elif self.scene == "camera":
                return pyglet.event.EVENT_HANDLED

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

        self.background.image.color = (self.power * 2.55, self.power * 2.55, self.power * 2.55)
        self.background.image.x, self.background.image.y = self.old_x, self.old_y
        self.tablet.image.visible = False
        self.GameObjects.clear()
        self.GameObjects["leftbutton"] = self.leftbutton
        self.GameObjects["rightbutton"] = self.rightbutton
        self.GameObjects["leftdoor"] = self.leftdoor
        self.GameObjects["rightdoor"] = self.rightdoor
        self.GameObjects["background"] = self.background
        self.GameObjects["SceneButton"] = self.scenebutton

        self.background.image.batch = self.Batch["office"]
        self.scenebutton.image.batch = self.Batch["office"]
        self.background.batch = self.Batch["office"]
        self.scenebutton.batch = self.Batch["office"]

        self.Channel[0].volume = 0.0
        self.Channel[1].volume = 0.5
        self.Channel[2].volume = 0.5
        self.Channel[4].volume = 0.5
        self.Channel[7].volume = 0.0
        self.Channel[10].volume = 0.0
        self.Channel[11].volume = 0.05
        self.Channel[18].volume = 0.0
        self.Channel[20].volume = 0.1
        self.Channel[21].volume = 0.0
        self.Channel[22].volume = 0.25

        self.Channel[1].play()
        self.Channel[2].play()
        self.Channel[11].play()
        self.Channel[20].play()
        self.Channel[22].play()

        self.push_handlers(self.scenebutton.on_mouse_motion)
        self.push_handlers(self.leftbutton.on_mouse_press)
        self.push_handlers(self.rightbutton.on_mouse_press)
        self.scene = "office"

    def setup_camera(self):
        '''Camera setup.'''
        try:
            self.pop_handlers()
            self.remove_handlers(self.leftbutton.on_mouse_press)
        except AssertionError:
            pass

        self.background.image.color = (255,255,255)
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

    def setup_powerout(self):
        '''Powerout setup and stage one of outage.'''
        try:
            self.pop_handlers()
            self.remove_handlers(self.leftbutton.on_mouse_press)
        except AssertionError:
            pass
        self.GameObjects.clear()
        self.GameObjects["background"] = self.background
        self.GameObjects["leftdoor"] = self.leftdoor
        self.GameObjects["rightdoor"] = self.rightdoor
        self.background.image.batch = self.Batch["powerout"]
        self.leftdoor.batch = self.Batch["powerout"]
        self.rightdoor.batch = self.Batch["powerout"]
        self.background.batch = self.Batch["powerout"]
        self.background.image.image = self.Backgrounds["powerout"]["0"]
        self.background.image.color = (255,255,255)
        self.background.image.opacity = 255
        self.background.image.visible = True
        if self.leftbutton.door:
            self.leftdoor.open()
        if self.rightbutton.door:
            self.rightdoor.open()

        self.scene = "powerout"

        sound = pyglet.media.load("sounds\\misc\\powerout.wav").play()
        if random.randint(0, 1) == 0:
            pyglet.clock.schedule_once(self.powerout_stage2, 12)

        else:
            pyglet.clock.schedule_once(self.powerout_stage2, random.randint(4, 18))

    def powerout_stage2(self, dt=None):
        self.powerout_stage = 2
        sound = pyglet.media.load("sounds\\misc\\musicbox.wav").play()
        if random.randint(0, 1) == 0:
            pyglet.clock.schedule_once(self.powerout_stage3, 12)
        else:
            pyglet.clock.schedule_once(self.powerout_stage3, random.randint(3, 61))

    def powerout_stage3(self, dt=None):
        pyglet.app.exit()

    def update(self, dt):
        if self.scene == "office":
            if self.hour == 0:
                self.hourlabel.text = "12  PM"
            else:
                self.hourlabel.text = "%s  AM" %(self.hour)

            if self.power < 0:
                self.setup_powerout()

            self.powerlabel.text = "Power left:  %s" %(self.power)
            self.usagelabel.text = "Usage:  %s" %(self.usage)

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

            if self.power > 25:
                self.background.image.color = (self.power * 2.55, self.power * 2.55, self.power * 2.55)
                self.leftbutton.image.color = (self.power * 2.55, self.power * 2.55, self.power * 2.55)
                self.rightbutton.image.color = (self.power * 2.55, self.power * 2.55, self.power * 2.55)
                self.leftdoor.image.color = (self.power * 2.55, self.power * 2.55, self.power * 2.55)
                self.rightdoor.image.color = (self.power * 2.55, self.power * 2.55, self.power * 2.55)
            else:
                self.background.image.color = (25 * 2.55, 25 * 2.55, 25 * 2.55)
                self.leftbutton.image.color = (25 * 2.55, 25 * 2.55, 25 * 2.55)
                self.rightbutton.image.color = (25 * 2.55, 25 * 2.55, 25 * 2.55)
                self.leftdoor.image.color = (25 * 2.55, 25 * 2.55, 25 * 2.55)
                self.rightdoor.image.color = (25 * 2.55, 25 * 2.55, 25 * 2.55)

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
                self.background.image.image = self.Backgrounds["camera"]["cam1a"]["brc"]
                # = pyglet.sprite.Sprite(self.Backgrounds["camera"]["cam1a"]["brc"], x=self.background.x, y=self.background.y, batch=self.background.batch, group=self.background.group)

            elif self.camera == "cam1b":
                self.background.image.image = self.Backgrounds["camera"]["cam1b"]["0"]

            elif self.camera == "cam1c":
                self.background.image.image = self.Backgrounds["camera"]["cam1c"]["0"]

            elif self.camera == "cam2a":
                self.background.image.image = self.Backgrounds["camera"]["cam2a"]["0"]

            elif self.camera == "cam2b":
                self.background.image.image = self.Backgrounds["camera"]["cam2b"]["0"]

            elif self.camera == "cam3":
                self.background.image.image = self.Backgrounds["camera"]["cam3"]["0"]

            elif self.camera == "cam4a":
                self.background.image.image = self.Backgrounds["camera"]["cam4a"]["0"]

            elif self.camera == "cam4b":
                self.background.image.image = self.Backgrounds["camera"]["cam4b"]["0"]

            elif self.camera == "cam5":
                self.background.image.image = self.Backgrounds["camera"]["cam5"]["0"]

            elif self.camera == "cam6":
                self.background.image.image = self.Backgrounds["camera"]["cam6"]["0"]

            elif self.camera == "cam7":
                self.background.image.image = self.Backgrounds["camera"]["cam7"]["0"]

            else:
                self.background.image.image = self.Backgrounds["camera"]["cam6"]["0"]

        if self.scene == "powerout":
            if self.powerout_stage == 1:
                self.background.image.image = self.Backgrounds["powerout"]["0"]

            if self.powerout_stage == 2:
                self.background.image.image = random.choice([self.Backgrounds["powerout"]["0"], self.Backgrounds["powerout"]["0"], self.Backgrounds["powerout"]["0"], self.Backgrounds["powerout"]["1"]])

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

if __name__ == "__main__":
    print("Run game.py")
    sys.exit(0)

else:
    Main.register_event_type("on_button_press")
