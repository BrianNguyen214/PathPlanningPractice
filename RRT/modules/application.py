import pygame as pg

# perf_counter returns a float that represents the time in seconds
# we'll use it to record the run time of the algorithm
from time import perf_counter

# this allows you to generate a random number from a specified range
from random import randrange as rand

# turns out there's a math function to return the hypotenuse if you give it
# two coordinate points
from math import hypot

# we'll make use of the classes and the constants defined in 
from . import classes as cl
from . constants import *

pg.init()

# p1 and p2 are going to be arrays that store the coordinate points
# of the nodes
def dist(p1, p2):
    return hypot(p2[0]-p1[0], p2[1]-p1[1])

class Application:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        icon = pg.surface.Surface((32,32))
        icon.fill(BEGIN_COLOR)
        pg.display.set_icon(icon)
        pg.display.set_caption(CAPTION)

        # creating the begin square, the goal square, and the surface
        self.beginSquare = cl.Square(BEGIN_COLOR, BEGIN_INIT_POS)
        self.goalSquare = cl.Square(TARGET_COLOR, TARGET_INIT_POS)
        self.obsSurf = cl.SurfSprite()

        self.sprites = pg.sprite.Group(self.beginSquare, self.goalSquare, self.obsSurf)

        self.appLoop()

    def appLoop(self):
        run = True
        while True: 
            self.screen.fill(BG_COLOR)
            self.sprites.draw(self.screen)
            # .display.flip() updates the full display Surface to the screen
            pg.display.flip()
        
        pg.quit()


