import pygame

class Text(pygame.sprite.Sprite):
    '''Class for easy-to-draw text. Inherits from a sprite so it can be
       added to sprite groups.'''
    def __init__(self, string="Sample text", color=(0,0,0), x=0, y=0, size=12, *groups):
        super().__init__(groups)
        self.string = string
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(None, self.size)
        self.image = self.font.render(self.string, True, self.color)
        self.rect = self.image.get_rect()

        self.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, string=None, color=None, x=None, y=None, size=None):
        if string:
            self.string = string

        if color:
            self.color = color

        if x:
            self.x = x

        if y:
            self.y = y

        if size:
            self.size = size

        if string or color or x or y or size:
            self.font = pygame.font.Font(None, self.size)
            self.image = self.font.render(self.string, True, self.color)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
