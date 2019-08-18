import pygame
pygame.init()
from pygame import *

class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

x = 100
y = 100
width = 50
height = 300

x2 = 250
y2 = 250
width2 = 200
height2 = 50

vel = 5

XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
delta = 10.0
GAME_LEVEL = 1
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0
NUMNODES = 5000
pygame.init()
fpsClock = pygame.time.Clock()
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0,180,105

win.fill((255,255,255))

run = True

# defining nodes based on their top left corner
NodeDict = {}

def parser(inputNode):
    pt = inputNode.point
    x, y = pt
    s = str(x) + ' ' + str(y)
    NodeDict[s] = inputNode  

def stringer(pt):
    x, y = pt
    return str(x) + ' ' + str(y) 

for i in range(0, 500, 10):
    for j in range(0, 500, 10):
        s = stringer((i, j))
        NodeDict[s] = False

def filler():
    for i in range(x, x+width, 10):
        for j in range(y, y+height, 10):
            coord = (i, j)
            s = stringer(coord)
            NodeDict[s] = True

    for i in range(x2, x2+width2, 10):
        for j in range(y2, y2+height2, 10):
            coord = (i, j)
            s = stringer(coord)
            NodeDict[s] = True

filler()

initializedBegin = False
initializedEnd = False

while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            if initializedBegin == False and initializedEnd == False:
                initializedBegin = True
                initialPoint = Node(event.pos, None)
                xCoord, yCoord = initialPoint.point
                xCoord -= xCoord % 10
                yCoord -= yCoord % 10
                s = stringer((xCoord, yCoord))
                NodeDict[s] = True
                pygame.draw.rect(win, (0,255,0), (xCoord, yCoord, 10, 10)) 
            elif initializedEnd == False:
                initializedEnd = True
                initialPoint = Node(event.pos, None)
                xCoord, yCoord = initialPoint.point
                xCoord -= xCoord % 10
                yCoord -= yCoord % 10
                s = stringer((xCoord, yCoord))
                NodeDict[s] = True
                pygame.draw.rect(win, (0,0,255), (xCoord, yCoord, 10, 10)) 

    #drawing the horizontal lines
    for i in range(2500/50):
        pygame.draw.line(win, (0, 0, 0), (0, i*10), (500, i*10))

    #drawing the vertical lines
    for i in range(2500/50):
        pygame.draw.line(win, (0, 0, 0), (i*10, 0), (i*10, 500))
    
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.draw.rect(win, (255,0,0), (x2, y2, width2, height2))  
    pygame.display.update() 
    
pygame.quit()