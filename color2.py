import pygame, sys, math
from pygame.locals import *
pygame.init()
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode([730,54],32)
s = 0.6
color = [[100,255,0],[0,255,180],[0,200,255],[0,100,255],[50,0,255],[120,0,255],[180,0,255],[255,0,200],[255,0,20],[255,100,0],[255,150,0],[255,200,0],[255,240,0],[180,255,0]]
def update():
    for i in range(14):
        pygame.draw.rect(screen,[(color[i][0]*s)+(127*(1-s)),(color[i][1]*s)+(127*(1-s)),(color[i][2]*s)+(127*(1-s))],[2+(i*52),2,50,50],0)
        print([round((color[i][0]*s)+(127*(1-s))),round((color[i][1]*s)+(127*(1-s))),round((color[i][2]*s)+(127*(1-s)))])
    pygame.display.flip()
update()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_q:
                if s != 1:
                    s += 0.05
                    s = round(s*100)/100
                    update()
                    print(s)
            if event.key == K_a:
                if s != 0.05:
                    s -= 0.05
                    s = round(s*100)/100
                    update()
                    print(s)
    
    mainClock.tick(30)
