import pyglet
from pyglet.gl import *

class Main(pyglet.window.Window):
    '''Class for the main game.'''
    def __init__(self):
        '''Initialize the game.'''
        self.time = 0
        self.power = 0
        self.usage = 0

        self.Sprites = {}
        self.GameObjects = []

        self.setup_sprites()
        pyglet.clock.schedule(self.update)

    def setup_sprites(self):
        self.Sprites["background"] =

    def update(self, dt):
        pass

    def on_draw(self):
        for object in self.GameObjects:
            object.draw()

class Sprite(pyglet.sprite.Sprite):
    '''Class for a custom sprite. MUST BE PNG.'''
    def __init__(self, location, filename, x=0, y=0, batch=None, group=None):
        self.image = pyglet.image.load(os.path.join(location, filename), decoder=pyglet.image.codecs.png.PNGImageDecoder())
        self.x = x
        self.y = y
        self.batch = batch
        self.group = group
        self.rekt = Rekt(self.x, self.y, self.image.width, self.image.height)

        if isinstance(position, tuple):
            self.position = position

        else:
            raise ValueError("Position is not a tuple.")

        super().__init__(self.image, self.x, self.y, batch=self.batch, group=self.group)

    def draw(self):
        self.image.blit(self.x, self.y)

    def update(self, dt):
        self.rekt.x, self.rekt.y = self.x, self.y

class Rekt():
    '''Class for rektangles.'''
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return "<rekt(%d, %d, %d, %d)>" %(self.x, self.y, self.w, self.h)

    def __getitem__(self, key):
        return (self.x, self.y, self.w, self.h)[key]

    def __setitem__(self, key, val):
        if key == 0:
            self.x = val

        elif key == 1:
            self.y = val

        elif key == 2:
            self.w = val

        elif key == 3:
            self.h = val

        else:

            raise IndexError(key)

    def get_Left(self):
        return self.x

    def set_Left(self, x):
        self.x = x

    def get_Top(self):
        return self.y

    def set_Top(self, y):
        self.y = y

    def get_Width(self):
        return self.w

    def set_Width(self, w):
        self.w = w

    def get_Height(self):
        return self.h

    def set_Height(self, h):
        self.h = h

    def collidepoint(self, point):
        '''Checks if the specified point collides with the rectangle.'''
        if (point[0] is in range(self.x, self.x + self.w)) and (point[1] is in range(self.y, self.y + self.h)):
            return True
        return False
