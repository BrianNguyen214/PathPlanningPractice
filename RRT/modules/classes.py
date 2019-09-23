from . constants import *
import pygame as pg
from math import hypot
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
        # we need the distFromBegin attribute for the rrtStar app; not the rrt app
        self.distFromBegin = 0
        self.left = None
        self.right = None
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

class KDTree:
    def __init__(self, root):
        self.root = root
        self.numNodes = 1

    def addNode(self, inputNode):
        tmpNode = self.root
        currLevel = 1
        self.numNodes += 1

        while tmpNode != None:
            # if the currLevel is odd, then we want to place the node
            # based on the first coord
            if currLevel % 2 == 1:
                if inputNode.pos[0] < tmpNode.pos[0]:
                    if tmpNode.left == None:
                        tmpNode.left = inputNode
                        break
                    else:
                        tmpNode = tmpNode.left
                        currLevel += 1
                else:
                    if tmpNode.right == None:
                        tmpNode.right = inputNode
                        break
                    else:
                        tmpNode = tmpNode.right
                        currLevel += 1
            # else, this means that the currLevel is even, so we want to place
            # the node based on the second coord
            else:
                if inputNode.pos[1] < tmpNode.pos[1]:
                    if tmpNode.left == None:
                        tmpNode.left = inputNode
                        break
                    else:
                        tmpNode = tmpNode.left
                        currLevel += 1
                else:
                    if tmpNode.right == None:
                        tmpNode.right = inputNode
                        break
                    else:
                        tmpNode = tmpNode.right
                        currLevel += 1
    
    def calcDistKDT(self, p1, p2):
        return hypot(p2[0]-p1[0], p2[1]-p1[1])
    
    def findClosest(self, givenPt):            
        tmpNode = self.root
        currLevel = 1
        minDist = float('inf')
        closestPt = self.root.pos
        closestVert = self.root

        while tmpNode != None:
            # if the currLevel is odd, then we want to place the node
            # based on the first coord
            dist = self.calcDistKDT(givenPt, tmpNode.pos)
            if dist < minDist:
                minDist = dist
                closestPt = tmpNode.pos
                closestVert = tmpNode

            if currLevel % 2 == 1:
                if givenPt[0] < tmpNode.pos[0]:
                    tmpNode = tmpNode.left
                    currLevel += 1
                else:
                    tmpNode = tmpNode.right
                    currLevel += 1
            # else, this means that the currLevel is even, so we want to place
            # the node based on the second coord
            else:
                if givenPt[1] < tmpNode.pos[1]:
                    tmpNode = tmpNode.left
                    currLevel += 1
                else:
                    tmpNode = tmpNode.right
                    currLevel += 1 

        return closestVert, minDist