import pygame as pg
import time
from time import perf_counter
from random import randrange as rand
from math import hypot

import sys

pg.init()

class KDNode:
    def __init__(self, coords):
        self.coords = coords
        self.left = None
        self.right = None

class KDTree:
    def __init__(self, root):
        self.root = root
        self.numDimensions = len(root.coords)
        self.numNodes = 1

    def addNode(self, inputNode):
        tmpNode = self.root
        currLevel = 1

        while tmpNode != None:
            # if the currLevel is odd, then we want to place the node
            # based on the first coord
            if currLevel % 2 == 1:
                if inputNode.coords[0] < tmpNode.coords[0]:
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
                if inputNode.coords[1] < tmpNode.coords[1]:
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

screen = pg.display.set_mode((500, 500))
screen.fill((0,0,0))
pg.display.flip()

def populateRandPts():
    listOfCoords = []
    firstNode = KDNode((rand(500), rand(500)))
    listOfCoords.append(firstNode.coords)
    KDT = KDTree(firstNode)
    newNodeCirc = pg.draw.circle(screen, (255, 134, 10), firstNode.coords, 2)
    pg.display.update([newNodeCirc])

    # time to populate the other vertexes
    for i in range(9):
        nextNode = KDNode((rand(500), rand(500)))
        listOfCoords.append(nextNode.coords)
        KDT.addNode(nextNode)
        newNodeCirc = pg.draw.circle(screen, (255, 134, 10), nextNode.coords, 2)
        pg.display.update([newNodeCirc])

    x = 1

def runApp():
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return 'quit'
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    populateRandPts()
                    x = 1

runApp()




            