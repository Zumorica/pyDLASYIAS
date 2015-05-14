import pygame
import pygame.freetype
import sys
import os
import random
import lightning.tmx as tmx
from pygame.locals import *

class Engine():
    '''Class for the engine.'''
    def __init__(self, W=800, H=600, caption=None, icon=None, debug=True):
        self.screen = pygame.display.set_mode((W, H), 0, 32)
        self.clock = pygame.time.Clock()
        self.running = True
        self.caption = caption
        self.icon = icon
        self.debug = debug
        self.tilemap = None
        self.sprites = tmx.SpriteLayer()
        self.dt = None
        self.channels = []

        pygame.mixer.init()
        pygame.mixer.set_num_channels(31)

        for i in range(0, 31):
            self.channels.append(pygame.mixer.Channel(i))

        if self.icon:
            pygame.display.set_icon(self.icon)
        else:
            self.icon = pygame.Surface((1,1))
            self.icon.set_alpha(True)
            pygame.display.set_icon(self.icon)

        if self.caption:
            pygame.display.set_caption(self.caption)

    def load_map(self, map):
        '''Loads a new map.'''
        self.tilemap = tmx.load(map, self.screen.get_size())
        self.tilemap.set_focus(0, 0)

    def load_tile_table(self, filename, width, height):
        '''Loads a tile table.'''
        img = pygame.image.load(filename).convert_alpha()
        img_w, img_g = img.get_size()
        tile_table = []
        for tile_x in range(0, img_w/width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, img_h/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table

    def handle_events(self):
        '''Safe to override.'''
        pass

    def main_loop(self):
        '''Safe to override.'''
        pass

    class Object(pygame.sprite.Sprite):
        '''Object for tilemaps' objects.'''
        def __init__(self, object):
            self.object = object
            self.px = object.px
            self.py = object.py
            self.x = object.x
            self.y = object.y
