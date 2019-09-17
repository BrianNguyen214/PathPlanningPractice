import pygame as pg
import time
# perf_counter returns a float that represents the time in seconds
# we'll use it to record the run time of the algorithm
from time import perf_counter

# this allows you to generate a random number from a specified range
from random import randrange as rand

# turns out there's a math function to calculate the hypotenuse of two 
# coordinate points
from math import hypot

import sys

pg.init()

class Square(pg.sprite.Sprite):

    # we'll pass in a position coordinate when we initialize the class
    def __init__(self, color, pos):
        pg.sprite.Sprite.__init__(self)

        # image and rect are required members that the Sprite object must have

        self.image = pg.Surface((20, 20))
        # .get_rect returns the area of the rectangle, or essentially
        # creates a rect with the same of the image/pg.Surface and
        # set's it's topleft coordinate to the pos 
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(color)

class Vertex:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent
        self.distFromBegin = 0
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

screen = pg.display.set_mode((500, 500))
begin = Square((0, 255, 0), (120, 120))
end = Square((255, 0, 0) , (450, 450))

sprites = pg.sprite.Group(begin, end)

screen.fill((0,0,0))

treeSurf = pg.surface.Surface((500, 500))

sprites.draw(screen)
pg.display.flip()

vertices = []
# adding the begin vertex as the first vertex in the list
firstVert = Vertex(begin.rect.center, None)
vertices.append(firstVert)

hardCodedVertPos = [
    (60, 230),
    (180, 235),
    (170, 280),
    (182, 300)
]

def appLoop():
    running = True
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return 'quit'
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    putInVerts()

def calcDist(p1, p2):
    return hypot(p2[0]-p1[0], p2[1]-p1[1])

def findTheNearestVert(currVertPos):
    closestDist = float('inf')
    nearestVert = vertices[0]
    print('the current  pos')
    print(currVertPos)
    for v in vertices:
        print('compared against vert pos')
        print(v.pos)
        currDist = calcDist(v.pos, currVertPos)
        print('the dist between the two nodes')
        print(currDist)
        if currDist < closestDist:
            closestDist = currDist
            nearestVert = v
    return nearestVert, closestDist

def putInVerts():
    for vertPos in hardCodedVertPos:
        newVert = pg.draw.circle(screen, (255, 134, 10), vertPos, 2)
        nearestVert, distFromClosest = findTheNearestVert(vertPos)
        newEdge = pg.draw.line(screen, (255, 255, 255), nearestVert.pos, vertPos)
        pg.display.update([newVert, newEdge])
        newAddedVert = Vertex(vertPos, nearestVert)
        newAddedVert.distFromBegin = newAddedVert.parent.distFromBegin + distFromClosest
        vertices.append(newAddedVert)
        rewire(newAddedVert)

def rewire(givenVert):
    # 210, 110, 50
    rewireRadius = 210

    # this is for visual purposes only
    RRVert = pg.draw.circle(screen, (100, 100, 255), givenVert.pos, rewireRadius, 1)
    pg.display.update([RRVert])

    print('the parent is')
    print(givenVert.parent.pos)
    print('the parent\'s distance from beginning is ' + str(givenVert.parent.distFromBegin))
    print('the distance from beginning is ' + str(givenVert.distFromBegin))
    
    print('\n')
    for v in vertices:
        print('the vert is ' + str(v.pos))
        distAway = calcDist(givenVert.pos, v.pos)
        print('the dist before: ' + str(distAway))
        totalDist = distAway + v.distFromBegin
        print('the dist with the additional distFromBegin: '+ str(totalDist))
        if distAway < rewireRadius and totalDist < givenVert.distFromBegin:
            print('the totalDist is ' + str(totalDist))
            print('the givenVert dist from beginning is ' + str(givenVert.distFromBegin))
            oldparent = givenVert.parent
            givenVert.parent = v
            givenVert.distFromBegin = givenVert.parent.distFromBegin + distAway
            
            print('the oldparent pos is ' + str(oldparent.pos))
            print('the givenVert pos is ' + str(givenVert.pos))
            removeEdge = pg.draw.line(screen, (0, 0, 0), givenVert.pos, oldparent.pos, 3)
            print('the new givenVert dist from beginning is ' + str(givenVert.distFromBegin) + '\n')
            newEdge = pg.draw.line(screen, (255, 255, 255), givenVert.pos, v.pos)
            pg.display.update([newEdge])
            pg.display.update([removeEdge])
appLoop()
            