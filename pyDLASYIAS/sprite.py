import pygame, os
import pyDLASYIAS.Globals as Globals
from pygame.locals import *

pygame.init()

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
