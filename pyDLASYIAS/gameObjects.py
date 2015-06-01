import pyglet

class GameObject():
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

    def draw(self):
        self.image.draw()

    def update(self, dt):
        pass

class Sprite(GameObject):
    def __init__(self, img, x=0, y=0, batch=None, group=None):
        super().__init__(pyglet.image.load(img), x=x, y=y, batch=batch, group=group)

    def change_img(self, img):
        self.image.remove()
        self.image = pyglet.sprite.Sprite(pyglet.image.load(img), x=self.x, y=self.y, batch=self.batch, group=self.group)

    def collidepoint(self, x, y):
        if x in range(self.x, self.x + self.image.width) and y in range(self.y, self.y + self.image.height):
            return True
        return False

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.image.x, self.image.y = int(self.x), int(self.y)


class Door(GameObject):
    def __init__(self, isRight, x=0, y=0, batch=None, group=None):
        self.isRight = isRight
        self.isClosed = False
        self.Frames = []


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

class Button(GameObject):
    def __init__(self, isRight, door, x=0, y=0, batch=None, group=None):
        if not isinstance(door, object):
            raise ValueError("'door' is not an object.")

        self.door = door
        self.light = False
        self.isRight = isRight

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

    def on_mouse_press(self, x, y, button, modifiers):
        if x in range((int(self.x) + 30), (int(self.x) + 68)) and y in range((int(self.y) + 62), (int(self.y) + 118)) and button == 1:
            if self.light:
                self.light = False
            else:
                self.light = True

        if x in range((int(self.x) + 30), (int(self.x) + 68)) and y in range((int(self.y) + 144), (int(self.y) + 193)) and button == 1:
            if self.door:
                self.door.open()

            else:
                self.door.close()


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
