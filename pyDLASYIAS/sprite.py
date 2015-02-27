import pygame, os
import pyDLASYIAS.Globals as Globals
from pygame.locals import *

pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME, 0)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startpos=(0,0), autoupdates=True):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(startpos)
        self.image = pygame.image.load("images\\" + str(image) + ".png")

        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()
        if autoupdates:
            self.update()

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tuple(self.pos)


    def changeImg(self, image):
        self.image = pygame.image.load("images\\" + str(image) + ".png")
        self.image = self.image.convert_alpha()
        self.update()

class Animated(pygame.sprite.Sprite):
    def __init__(self, images=[], startpos=(0,0), loops=False):
        pygame.sprite.Sprite.__init__(self)
        self.pos = startpos

        self.index = 0
        self.images = list(images)

        self.image = pygame.image.load("images\\" + self.images[self.index]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

        self.loops = loops

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.index += 1

        if self.index >= len(self.images) and self.loops:
            self.index = 0

        if self.index >= len(self.images) and not self.loops:
            self.index = len(self.images)

        if not self.has_Finished():
            self.image = pygame.image.load("images\\" + self.images[self.index]).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.pos

    def has_Finished(self):
        if not self.loops and self.index == len(self.images):
            return True

        else:
            return False
