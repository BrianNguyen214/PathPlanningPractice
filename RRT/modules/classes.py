from . constants import *
import pygame as pg
pg.init()

# we're allowing the Square to inherit the sprite.Sprite object class
# which is a simple base class for making visible objects on the screen
class Square(pg.sprite.Sprite):

    # we'll pass in a position coordinate when we initialize the class
    def __init__(self, color, pos):
        pg.sprite.Sprite.__init__(self)

        # image and rect are required members that the Sprite object must have

        self.image = pg.Surface((SQU_SIDE_LEN, SQU_SIDE_LEN))
        # .get_rect returns the area of the rectangle, or essentially
        # creates a rect with the same of the image/pg.Surface and
        # set's it's topleft coordinate to the pos 
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(color)

class SurfSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.surface.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()

        # .set_colorkey sets the transparent colorkey
        self.image.set_colorkey(BG_COLOR)
        self.image.fill(BG_COLOR)

class Vertex:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0