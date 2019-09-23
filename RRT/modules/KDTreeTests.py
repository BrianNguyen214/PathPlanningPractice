import pygame as pg
import time
from time import perf_counter
from random import randrange as rand
from math import hypot
import numpy as np

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
    
    def calcDistKDT(self, p1, p2):
        return hypot(p2[0]-p1[0], p2[1]-p1[1])
    
    def findClosest(self, givenPt):            
        tmpNode = self.root
        currLevel = 1
        minDist = float('inf')
        closestPt = self.root.coords

        while tmpNode != None:
            # if the currLevel is odd, then we want to place the node
            # based on the first coord
            dist = self.calcDistKDT(givenPt, tmpNode.coords)
            if dist < minDist and givenPt != tmpNode.coords:
                minDist = dist
                closestPt = tmpNode.coords

            if currLevel % 2 == 1:
                if givenPt[0] < tmpNode.coords[0]:
                    tmpNode = tmpNode.left
                    currLevel += 1
                else:
                    tmpNode = tmpNode.right
                    currLevel += 1
            # else, this means that the currLevel is even, so we want to place
            # the node based on the second coord
            else:
                if givenPt[1] < tmpNode.coords[1]:
                    tmpNode = tmpNode.left
                    currLevel += 1
                else:
                    tmpNode = tmpNode.right
                    currLevel += 1 

        return minDist, closestPt

screen = pg.display.set_mode((500, 500))
screen.fill((0,0,0))
pg.display.flip()

hardCodedPts = [
    (337, 230),
    (219, 123),
    (210, 329),
    (303, 322),
    (240, 239),
    (152, 28),
    (467, 480),
    (414, 319)
]

def calcDist(p1, p2):
    return hypot(p2[0]-p1[0], p2[1]-p1[1])

def populateRandPts():
    
    compMinDistArr = []
    travMinDistArr = []
    listOfCoords = []

    def testMinFuncs():

        # this is finding the distance the brute force way = comparing
        # the given pt with all of the other points and getting the smallest distance
        def compareDistWithPt(pt):
            minDist = float('inf')
            closestPt = listOfCoords[0]
            if len(listOfCoords) == 1:
                return 0, closestPt

            for i in range(len(listOfCoords)):
                dist = calcDist(pt, listOfCoords[i])
                if dist < minDist and pt != listOfCoords[i]:
                    minDist = dist
                    closestPt = listOfCoords[i]
            return minDist, closestPt

        def travKDTFindMin(pt):
            return KDT.findClosest(pt)

        # this is where we test to see if the different methods have the same results
        numTests = 5
        for i in range(numTests):
            newRandPt = (rand(500), rand(500))
            nextNode = KDNode(newRandPt)
            listOfCoords.append(nextNode.coords)
            if i == 0:
                KDT = KDTree(nextNode)
            else:
                KDT.addNode(nextNode)
            compDist = compareDistWithPt(newRandPt)
            travDist = travKDTFindMin(newRandPt)
            compMinDistArr.append(compDist)
            travMinDistArr.append(travDist)

        print(travMinDistArr)

        # checking here to see if the the algorithms have the same elements/results
        if np.array_equal(compMinDistArr, travMinDistArr):
            print('There were no differences')

        # this is where we test the runtime for the brute force way
        t1_init = time.time()
        newRandPtArr = [(rand(500), rand(500)) for i in range(numTests)]
        for i in range(numTests):
            newRandPt = newRandPtArr[i]
            nextNode = KDNode(newRandPt)
            listOfCoords.append(nextNode.coords)
            if i == 0:
                KDT = KDTree(nextNode)
            else:
                KDT.addNode(nextNode)
            compDist = compareDistWithPt(newRandPt)
        print('getting the comp runtime')
        # t1_final = time.time()
        # print(t1_init)
        # print(t1_final)
        compTotalTime = time.time() - t1_init
        print(compTotalTime)

        # this is where we test the runtime for the kdt way
        t2_init = time.time()
        for i in range(numTests):
            newRandPt = newRandPtArr[i]
            nextNode = KDNode(newRandPt)
            listOfCoords.append(nextNode.coords)
            if i == 0:
                KDT = KDTree(nextNode)
            else:
                KDT.addNode(nextNode)
            travDist = travKDTFindMin(newRandPt)
        print('getting the trav runtime')
        # t2_final = time.time()
        # print(t2_init)
        # print(t2_final)
        travTotalTime = time.time() - t2_init
        print(travTotalTime)
        x = 1
    # # looperNum = 9
    # looperNum = 8

    # for i in range(looperNum):
    #     # nextNode = KDNode((rand(500), rand(500)))
    #     nextNode = KDNode(hardCodedPts[i])
    #     listOfCoords.append(nextNode.coords)
    #     if i == 0:
    #         KDT = KDTree(nextNode)
    #     else:
    #         KDT.addNode(nextNode)
    #     newNodeCirc = pg.draw.circle(screen, (255, 134, 10), nextNode.coords, 2)
    #     pg.display.update([newNodeCirc])

    testMinFuncs()
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




            