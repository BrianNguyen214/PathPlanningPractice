import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

x = 100
y = 100
width = 40
height = 300

x2 = 250
y2 = 250
width2 = 200
height2 = 60

vel = 5

run = True

while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # keys = pygame.key.get_pressed()
    
    # if keys[pygame.K_LEFT]:
    #     x -= vel

    # if keys[pygame.K_RIGHT]:
    #     x += vel

    # if keys[pygame.K_UP]: # movement along the y-axis is backwards; going downwards decreases the y coordinate
    #     y -= vel

    # if keys[pygame.K_DOWN]:
    #     y += vel

    win.fill((0,0,0))

    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.draw.rect(win, (255,0,0), (x2, y2, width2, height2))  
    pygame.display.update() 
    
pygame.quit()