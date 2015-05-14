import pygame

class Line(pygame.sprite.Sprite):
    '''Class for a line.
       Inherits from a sprite so it can be easily added to sprite groups.'''
    def __init__(self, surface=None, color=(255,255,255), posOne=(0,0), posTwo=(0,0), width=1, transparent=True, *groups):
        super().__init__(groups)
        self.color = color
        self.posOne = posOne
        self.posTwo = posTwo
        self.width = width
        self.rect= None
        self.image = None
        self.surface = surface
        self.transparent = transparent

        self.update()

    def draw(self, surface):
        self.rect = pygame.draw.line(self.surface, self.color, self.posOne, self.posTwo, self.width)
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        if self.transparent:
            self.image.set_colorkey((0,0,0))
        self.surface.blit(self.image, self.rect)

    def update(self):
        self.rect = pygame.draw.line(self.surface, self.color, self.posOne, self.posTwo, self.width)
        self.image = pygame.Surface((self.rect.w, self.rect.h))
        if self.transparent:
            self.image.set_colorkey((0,0,0))
