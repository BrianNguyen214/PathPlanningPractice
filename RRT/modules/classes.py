from . constants import *
import pygame as pg
pg.init()

# we're allowing the Square to inherit the sprite.Sprite object class
# which is a simple base class for making visible objects on the screen
class Square(pg.sprite.Sprite):

    # we'll pass in a position coordinate when we initialize the class
    def __init__(self, color, pos):
        pg.sprite.Sprite.__init__(self)

        self.squImage = pg.Surface((SQU_SIDE_LEN, SQU_SIDE_LEN))
        # .get_rect returns the area of the rectangle, or essentially
        # creates a rect with the same of the image/pg.Surface and
        # set's it's topleft coordinate to the pos 
        self.rectArea = self.squImage.get_rect(topleft=pos)
        self.squImage.fill(color)

class SurfSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.ssImage = pg.surface.Surface((WIDTH, HEIGHT))
        self.rect = self.ssImage.get_rect()

        # .set_colorkey sets the transparent colorkey
        self.ssImage.set_colorkey(BG_COLOR)
        self.ssImage.fill(BG_COLOR)