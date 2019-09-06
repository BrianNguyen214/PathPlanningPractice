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

import sys

pg.init()

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

        # creating the surface in which the tree will be built on top of
        self.tree_surf = pg.surface.Surface((WIDTH, HEIGHT))
        
        # .set_colorkey allows you to make pixels whose color matches the key color to be 
        # to be ignored, and thus be transparent
        # this is to allow the tree to be on top of the background essentially
        # side-note: color-key transparency is used to make sure that spirtes sit on the
        # background images without being surrounded by a rectangle of dead pixels
        self.tree_surf.set_colorkey(BG_COLOR)
        self.tree_surf.fill(BG_COLOR)

        # storing the vertices/nodes of the tree
        self.vertices = None

        # surface for testing the collisions
        self.test_surf = cl.SurfSprite()

        self.sprites = pg.sprite.Group(self.beginSquare, self.goalSquare, self.obsSurf)

        # the possible states are: normal, begin_drag, goal_drag, drawing, erasing, running, path_found
        # i'm using this for debugging purposes and to allow the user to see what is going on
        # besides this, the self.state variable is used to carry out certain actions
        # depending on what the current state is
        self.state = 'normal'
        print(self.state)
        self.screen.fill(BG_COLOR)

        self.appLoop()

    def appLoop(self):
        run = True
        while run: 

            for e in pg.event.get():
                # for when user clicks the x button of the window, closing the application
                if e.type == pg.QUIT:
                    run = False
                elif e.type == pg.MOUSEBUTTONDOWN:
                    if e.button == 1: # left mouse button is clicked
                        # if the beginSquare is clicked, then set the state to begin_drag
                        if self.beginSquare.rect.collidepoint(e.pos):
                            self.state = 'begin_drag'
                        # if the goalSquare is clicked, then set the state to goal_drag
                        elif self.goalSquare.rect.collidepoint(e.pos):
                            self.state = 'goal_drag'
                        else:
                            self.state = 'drawing'
                    elif e.button == 3: # right button is clicked
                        self.state = 'erasing'
                    print(self.state)
                elif e.type == pg.MOUSEBUTTONUP:
                    self.state = 'normal'
                    print(self.state)
                elif e.type == pg.MOUSEMOTION: # it's pretty interesting that pygame can determine whether your pressing a key or dragging
                    if e.buttons[0]: # the left mouse button is being held down
                        # we're essentially continuously updating the position of the beginSquare and the goalSquare 
                        # in order to mimic dragging
                        if self.state == 'begin_drag':
                            self.beginSquare.rect.center = e.pos
                        elif self.state == 'goal_drag':
                            self.goalSquare.rect.center = e.pos
                        elif self.state == 'drawing':   
                            # .draw.line takes a surface, a color, a start position, an end position, and the width of the line
                            pg.draw.line(self.obsSurf.image, OBS_COLOR, (e.pos[0]-e.rel[0], e.pos[1]-e.rel[1]), e.pos, OBS_WIDTH)
                    elif e.buttons[2]: # the right mouse button is being held down
                        if self.state == 'erasing':
                            pg.draw.line(self.obsSurf.image, 0, (e.pos[0]-e.rel[0], e.pos[1]-e.rel[1]), e.pos, OBS_WIDTH)
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_RETURN:
                        self.state = 'running'
                        print(self.state)
                        if self.runRRT() == 'quit':
                            done = True
                        self.state = 'normal'
                        print(self.state)
            self.screen.fill(BG_COLOR)
            self.sprites.draw(self.screen)
            # .display.flip() updates the full display Surface to the screen
            # unlike .display.update() which updates a portion of the screen 
            # instead of the entire area
            pg.display.flip()
        
        pg.quit()

    def runRRT(self):
        # refresh/ clean the tree surface
        self.tree_surf.fill(BG_COLOR)

        # .mask.from_surface creates a mask form the surface; it's used for colision detection
        # creates a mask object from the surface by setting all of the opaque pixels
        # and not setting the transparent pixels
        # thus, all the pixels that are not equal to the color-key
        # are set and the pixels equal to the color-key are not set
        self.obsSurf.mask = pg.mask.from_surface(self.obsSurf.image)
        
        # need to add the first vertex as the beginning point's position
        newVert = cl.Vertex(self.beginSquare.rect.center, None)
        self.vertices = [newVert]

        # these are variables to keep track of some info about the path and the 
        # the run time of the algo
        treeHeight = 0
        linDist = dist(self.beginSquare.rect.center, self.goalSquare.rect.center)
        startTime = perf_counter()

        showInfo = True

        # if the center of the begin square is already in the goal square
        # then set done equal to True, and we're already done
        # otherwise, done will be set to False, and will have to continue running the algo until
        # there's a path between the beginSquare and the goalSquare
        done = self.goalSquare.rect.collidepoint(self.beginSquare.rect.center)
        
        while not done:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return 'quit'
                elif e.type == pg.KEYDOWN:
                    # press the 'h' key within the screen in order to toggle the
                    # info box
                    if e.key == pg.K_h:
                        showInfo = not showInfo
                        # hide the info
                        # essentially redraw ,everything besides the 
                        # info box
                        self.screen.fill(BG_COLOR)
                        self.sprites.draw(self.screen)

                        # .blit draws a source surface onto the new surface
                        # the drawing can be positioned with the second argument, which is a coordinate point
                        self.screen.blit(self.tree_surf, (0,0))
                        pg.display.flip()

            if showInfo:
                self.show_info(perf_counter() - startTime, treeHeight, len(self.vertices), linDist)
                    
        return 'quit'

    # p1 and p2 are going to be arrays that store the coordinate points
    # of the nodes
    def calcDist(p1, p2):
        return hypot(p2[0]-p1[0], p2[1]-p1[1])

    def findNearestVert(self, newRandPtCoord):
        closestDist = sys.maxint
        nearestVert = self.vertices[0]
        for i in self.vertices:
            dist = calcDist(i, newRandPtCoord)
            if dist < closestDist:
                closestDist = dist
                nearestVert = i
        print("The final closest dist is" + str(closestDist))
    def show_info(self, elapsed_time, height, nvertices, lin_dist, path_dist = None, path_len = None):
            print('showing the info')