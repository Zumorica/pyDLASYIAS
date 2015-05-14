import pygame

class Sprite(pygame.sprite.Sprite):
    '''Class for a custom sprite.'''
    def __init__(self, image, startpos=[0,0], layer=0, *groups=None):
        super().__init__(groups)
        self.layer = layer
        self.pos = list(startpos)
        self.image = pygame.image.load("images\\" + str(image)).convert_alpha()
        self.groups = groups
        self.rect = self.image.get_rect()
        self.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tuple(self.pos)

    def change_image(self, image):
        self.image = pygame.image.load("images\\" + str(image)).convert_alpha()
        self.update()
