import pyglet

class GameObject():
    def __init__(self, img, x=0, y=0, batch=None, group=None):
        if isinstance(img, str):
            self.image = pyglet.sprite.Sprite(pyglet.image.load(img), x=x, y=y, batch=batch, group=group)

        else:
            self.image = pyglet.sprite.Sprite(img, x=x, y=y, batch=batch, group=group)

        self.x, self.y = self.image.x, self.image.y
        self.dx, self.dy = 0, 0
        self.width = self.image.width
        self.height = self.image.height

    def draw(self):
        self.image.draw()

    def update(self, dt):
        pass

class Door(GameObject):
    def __init__(self, isRight, x=0, y=0, batch=None, group=None):
        self.isRight = isRight
        self.isClosed = False
        self.Frames = []


        if not self.isRight:
            for i in range(0, 16):
                if i != 15:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\left\\%s.png" %(i)), 0.15))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\left\\%s.png" %(i)), None))

                self.animation = pyglet.image.Animation(self.Frames)
        else:
            for i in range(0, 16):
                if i != 15:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\right\\%s.png" %(i)), 0.15))
                else:
                    self.Frames.append(pyglet.image.AnimationFrame(pyglet.image.load("images\\office\\doors\\right\\%s.png" %(i)), None))

                self.animation = pyglet.image.Animation(self.Frames)

        super().__init__(self.animation, x=x, y=y, batch=batch, group=group)

    def open(self):
        self.isClosed = False

    def close(self):
        self.isClosed = True

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
        if x in range((int(self.x) + 30), (int(self.x) + 68)) and y in range((int(self.y) + 195), (int(self.y) + 247)) and button == 1:
            if self.light:
                self.light = False
            else:
                self.light = True

        if x in range((int(self.x) + 30), (int(self.x) + 68)) and y in range((int(self.y) + 61), (int(self.y) + 113)):
            if self.door:
                self.door.open()

            else:
                self.door.close()


    def update(self, dt):
        if not self.door and not self.light:
            self.image.img = self.Sprite["0"]

        if self.door and not self.light:
            self.image.img = self.Sprite["d"]

        if not self.door and self.light:
            self.image.img = self.Sprite["l"]

        if self.door and self.light:
            self.image.img = self.Sprite["dl"]

        self.x += self.dx * dt
        self.y += self.dy * dt
