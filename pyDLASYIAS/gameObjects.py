import pyglet
import random
import time

class GameObject(pyglet.event.EventDispatcher):
    def __init__(self, img, x=0, y=0, batch=None, group=None):
        if isinstance(img, str):
            self.image = pyglet.sprite.Sprite(pyglet.image.load(img), x=x, y=y, batch=batch, group=group)

        else:
            self.image = pyglet.sprite.Sprite(img, x=x, y=y, batch=batch, group=group)

        self.batch = batch
        self.group = group
        self.x, self.y = self.image.x, self.image.y
        self.dx, self.dy = 0, 0
        self.width = self.image.width
        self.height = self.image.height
        self.movable = True

    def draw(self):
        self.image.draw()

    def update(self, dt):
        pass

GameObject.register_event_type("on_button_press")
GameObject.register_event_type("on_button_collide")
GameObject.register_event_type("on_camera_press")
GameObject.register_event_type("on_animation_end")

class Sprite(GameObject):
    def __init__(self, img, x=0, y=0, batch=None, group=None):
        super().__init__(img, x=x, y=y, batch=batch, group=group)
        self.movable = True
        self.image.x, self.image.y = x, y

    def change_image(self, img):
        self.image.delete()
        if isinstance(img, str):
            self.image = pyglet.sprite.Sprite(pyglet.image.load(img), x=self.x, y=self.y, batch=self.batch, group=self.group)
        else:
            self.image = pyglet.sprite.Sprite(img, x=self.x, y=self.y, batch=self.batch, group=self.group)

    def collidepoint(self, x, y):
        if (x in range(self.image.x, (self.image.x + self.image.width))) and (y in range(self.image.y, (self.image.y + self.image.height))):
            return True
        return False

    #     if (x in range(int(self.x), (int(self.x) + self.image.width))) and (y in range(int(self.y), (int(self.y) + self.image.height))):
    #         return True
    #     else:
    #         return False

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.image.x, self.image.y = int(self.x), int(self.y)

class Tablet(GameObject):
    def __init__(self, x=0, y=0, batch=None, group=None):
        self.isClosed = False
        self.Frames = []
        self.movable = False

        for i in range(0, 11):
            if i != 10:
                self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\cameras\\misc\\animation\\%s.png" %(i)), 0.020))
            else:
                self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\cameras\\misc\\animation\\%s.png" %(i)), None))

        self.animation_normal = pyglet.image.Animation(self.Frames)
        self.Frames = []

        for i in reversed(range(0, 11)):
            if i != 0:
                self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\cameras\\misc\\animation\\%s.png" %(i)), 0.020))
            else:
                self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\cameras\\misc\\animation\\%s.png" %(i)), None))

        self.animation_reversed = pyglet.image.Animation(self.Frames)

        super().__init__(pyglet.image.load("images\\cameras\\misc\\animation\\0.png"), x=x, y=y, batch=batch, group=group)

        self.image.visible = False

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.image.x, self.image.y = self.x, self.y
        @self.image.event
        def on_animation_end():
            self.dispatch_event("on_animation_end")

    def open(self):
        self.isClosed = False
        self.image.delete()
        self.image = pyglet.sprite.Sprite(self.animation_normal, x=self.x, y=self.y, batch=self.batch, group=self.group)
        self.image.visible = True

    def close(self):
        self.isClosed = True
        self.image.delete()
        self.image = pyglet.sprite.Sprite(self.animation_reversed, x=self.x, y=self.y, batch=self.batch, group=self.group)
        self.image.visible = True

class Static(GameObject):
    def __init__(self, opacitymin=255, opacitymax=255, batch=None, group=None):
        super().__init__(img="images\\cameras\\misc\\static\\0.png", x=0, y=0, batch=batch, group=group)
        self.opacitymin = opacitymin
        self.opacitymax = opacitymax
        self.image.opacity = random.randint(opacitymin, opacitymax)
        self.Sprites = [pyglet.image.load("images\\cameras\\misc\\static\\0.png"),
                        pyglet.image.load("images\\cameras\\misc\\static\\1.png"),
                        pyglet.image.load("images\\cameras\\misc\\static\\2.png"),
                        pyglet.image.load("images\\cameras\\misc\\static\\3.png"),
                        pyglet.image.load("images\\cameras\\misc\\static\\4.png"),
                        pyglet.image.load("images\\cameras\\misc\\static\\5.png"),
                        pyglet.image.load("images\\cameras\\misc\\static\\6.png"),
                        pyglet.image.load("images\\cameras\\misc\\static\\7.png")]

    def update(self, dt):
        self.image.delete()
        self.image = pyglet.sprite.Sprite(random.choice(self.Sprites), x=self.x, y= self.y, batch=self.batch, group=self.group)
        self.image.opacity = random.randint(self.opacitymin, self.opacitymax)

class Camera(GameObject):
    def __init__(self, name, img=None, x=0, y=0, batch=None, group=None, grouptwo=None):
        super().__init__(img="images\\ui\\button\\camera\\0.png", x=x, y=y, batch=batch, group=group)
        self.text = Sprite(img, x=(x + 10), y=(y + 7.5), batch=batch, group=grouptwo)
        self.name = name
        self.movable = False
        self.pressed = False
        self.Sprites = [pyglet.image.load("images\\ui\\button\\camera\\0.png"),
                        pyglet.image.load("images\\ui\\button\\camera\\1.png")]

    def collidepoint(self, x, y):
        if (x in range(self.image.x, (self.image.x + self.image.width))) and (y in range(self.image.y, (self.image.y + self.image.height))):
            return True
        return False

    def draw(self):
        self.image.draw()
        self.text.draw()

    def cameraPress(self):
        self.dispatch_event("on_camera_press", self.name)

    def on_camera_press(self, camera):
        pass

    def on_mouse_press(self, x, y, button, mod):
        if self.collidepoint(x, y):
            self.cameraPress()

    def update(self, dt):
        if self.pressed:
            self.image.delete()
            self.image = pyglet.sprite.Sprite(self.Sprites[1], x=self.x, y=self.y, batch=self.batch, group=self.group)
        else:
            self.image.delete()
            self.image = pyglet.sprite.Sprite(self.Sprites[0], x=self.x, y=self.y, batch=self.batch, group=self.group)

        self.x += self.dx * dt
        self.y += self.dy * dt

        self.image.x, self.image.y = int(self.x), int(self.y)

class Door(GameObject):
    def __init__(self, isRight, x=0, y=0, batch=None, group=None):
        self.isRight = isRight
        self.isClosed = False
        self.Frames = []
        self.movable = True


        if not self.isRight:
            for i in range(0, 16):
                if i != 15:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\left\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\left\\%s.png" %(i)), None))

            self.animation_normal = pyglet.image.Animation(self.Frames)
            self.Frames = []

            for i in reversed(range(0, 16)):
                if i != 0:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\left\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\left\\%s.png" %(i)), None))

            self.animation_reversed = pyglet.image.Animation(self.Frames)

            super().__init__(pyglet.image.load("images\\office\\doors\\left\\0.png"), x=x, y=y, batch=batch, group=group)

        else:
            for i in range(0, 16):
                if i != 15:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\right\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\right\\%s.png" %(i)), None))

            self.animation_normal = pyglet.image.Animation(self.Frames)
            self.Frames = []

            for i in reversed(range(0, 16)):
                if i != 0:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\right\\%s.png" %(i)), 0.025))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\right\\%s.png" %(i)), None))

            self.animation_reversed = pyglet.image.Animation(self.Frames)

            super().__init__(pyglet.image.load("images\\office\\doors\\right\\0.png"), x=x, y=y, batch=batch, group=group)


    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.image.x, self.image.y = self.x, self.y

    def open(self):
        self.isClosed = False
        self.image = pyglet.sprite.Sprite(self.animation_reversed, x=self.x, y=self.y, batch=self.batch, group=self.group)

    def close(self):
        self.isClosed = True
        self.image = pyglet.sprite.Sprite(self.animation_normal, x=self.x, y=self.y, batch=self.batch, group=self.group)



        # if not self.isRight:
        #     self.Sprites = {}
        #     for i in range(0, 16):
        #         self.Sprites[str(i)] = pyglet.image.load("images\\office\\doors\\left\\%s.png" %(i))
        # else:
        #     self.Sprites = {}
        #     for i in range(0, 16):
        #         self.Sprites[str(i)] = pyglet.image.load("images\\office\\doors\\right\\%s.png" %(i))
        #
        # super().__init__(pyglet.image.load("images\\office\\doors\\left\\0.png"), kwargs)

    def draw(self):
        self.image.draw()

    def __cmp__(self, other):
        return self.isClosed == other

    def __eq__(self, other):
        return self.isClosed == other

    def __bool__(self):
        return self.isClosed

class SceneButton(Sprite):
    def __init__(self, x=0, y=0, batch=None, group=None):
        super().__init__("images\\ui\\button\\camera.png", x=x, y=y, batch=batch, group=group)
        self.movable = False
        self.cooldown = False

    def collideButton(self):
        self.dispatch_event("on_button_collide")

    def showImage(self, dt=None):
        self.image.visible = True
        self.cooldown = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.collidepoint(x, y) and not self.cooldown:
            self.image.visible = False
            self.cooldown = True
            self.collideButton()

        if self.collidepoint(x, y) and self.cooldown:
            self.image.visible = False
            self.cooldown = True

        else:
            self.showImage()

    # Another way to do this...
    # def showImage(self, dt=None):
    #     self.image.visible = True
    #     self.cooldown = False
    #
    # def on_mouse_motion(self, x, y, dx, dy):
    #     if self.collidepoint(x, y) and self.image.visible:
    #         self.image.visible = False
    #         self.cooldown = True
    #         self.collideButton()
    #
    #     if self.collidepoint(x, y) and not self.image.visible and not self.cooldown:
    #         self.cooldown = True
    #
    #     if self.cooldown and not self.collidepoint(x, y):
    #         pyglet.clock.schedule_once(self.showImage, 2)

class Button(GameObject):
    def __init__(self, isRight, door, x=0, y=0, batch=None, group=None):
        if not isinstance(door, object):
            raise ValueError("'door' is not an object.")

        self.door = door
        self.light = False
        self.isRight = isRight
        self.movable = True
        self.cooldown = False

        if not self.isRight:
            self.Sprite = {"0" : pyglet.image.load("images\\office\\button\\left\\0.png"),
                           "d" : pyglet.image.load("images\\office\\button\\left\\d.png"),
                           "l" : pyglet.image.load("images\\office\\button\\left\\l.png"),
                           "dl" : pyglet.image.load("images\\office\\button\\left\\dl.png")}
            super().__init__(self.Sprite["0"], x=x, y=y, batch=batch, group=group)

        else:
            self.Sprite = {"0" : pyglet.image.load("images\\office\\button\\right\\0.png"),
                           "d" : pyglet.image.load("images\\office\\button\\right\\d.png"),
                           "l" : pyglet.image.load("images\\office\\button\\right\\l.png"),
                           "dl" : pyglet.image.load("images\\office\\button\\right\\dl.png")}
            super().__init__(self.Sprite["0"], x=x, y=y, batch=batch, group=group)

    def draw(self):
        self.image.draw()

    def buttonPress(self, button, state):
        self.dispatch_event("on_button_press", button, state)

    def on_button_press(self, button, state):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if x in range((int(self.x) + 30), (int(self.x) + 68)) and y in range((int(self.y) + 62), (int(self.y) + 118)) and button == 1:
            if self.light:
                self.light = False
                self.buttonPress("light", self.light)
            else:
                self.light = True
                self.buttonPress("light", self.light)

        if x in range((int(self.x) + 30), (int(self.x) + 68)) and y in range((int(self.y) + 144), (int(self.y) + 193)) and button == 1 and not self.cooldown:
            if self.door:
                self.door.open()
                self.buttonPress("door", self.door)
                self.cooldown = True

            else:
                self.door.close()
                self.buttonPress("door", self.door)
                self.cooldown = True


    def update(self, dt):
        if not self.door and not self.light:
            self.image.delete()
            self.image = pyglet.sprite.Sprite(self.Sprite["0"], x=self.x, y=self.y, batch=self.batch, group=self.group)

        if self.door and not self.light:
            self.image.delete()
            self.image = pyglet.sprite.Sprite(self.Sprite["d"], x=self.x, y=self.y, batch=self.batch, group=self.group)

        if not self.door and self.light:
            self.image.delete()
            self.image = pyglet.sprite.Sprite(self.Sprite["l"], x=self.x, y=self.y, batch=self.batch, group=self.group)

        if self.door and self.light:
            self.image.delete()
            self.image = pyglet.sprite.Sprite(self.Sprite["dl"], x=self.x, y=self.y, batch=self.batch, group=self.group)

        self.draw()

        self.x += self.dx * dt
        self.y += self.dy * dt

        self.image.x, self.image.y = self.x, self.y

        @self.door.image.event
        def on_animation_end():
            self.cooldown = False
