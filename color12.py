import sys
import math
from typing import *
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import pygame
from pygame.locals import *
pygame.init()

def convert(l: float, c: float, h: float):
    """converts lch to rgb color"""
    lab_color = LabColor(l, c * math.cos(math.radians(h)), c * math.sin(math.radians(h)))
    rgb_color = convert_color(lab_color, sRGBColor)
    output = [round(rgb_color.rgb_r * 255), round(rgb_color.rgb_g * 255), round(rgb_color.rgb_b * 255)]
    if not all([e > 0 and e < 255 for e in output]):
        output = [255, 255, 255]
    return output

n = 70
l = 10
points = [[100 * ((i / (n - 1)) ** 0.5), 360 * (((2 * i) / (1 + (5 ** 0.5))) % 1)] for i in range(n)]
points.sort(key=lambda x: x[1])

MainClock = pygame.time.Clock()
#MainScreen = pygame.display.set_mode(((21 * n) + 1, (21 * l) + 1))
MainScreen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Color12')
pixel_size = 1
screen = pygame.Surface((MainScreen.get_width() // pixel_size, 
                         MainScreen.get_height() // pixel_size))
origin = (screen.get_width() // 2, screen.get_height() // 2)
current_input = []

running  = True
while running:
    '''
    # update number
    if K_RIGHT in current_input:
        n += 1
        color_points = [[50, 100 * ((i / (n - 1)) ** 0.5), 360 * (((2 * i) / (1 + (5 ** 0.5))) % 1)] for i in range(n)]
    if K_LEFT in current_input:
        n -= 1
        color_points = [[50, 100 * ((i / (n - 1)) ** 0.5), 360 * (((2 * i) / (1 + (5 ** 0.5))) % 1)] for i in range(n)]
    '''
    # update the screen
    screen.fill((255, 255, 255))
    
    pygame.draw.circle(screen, [20, 20, 20], origin, 250, 2)
    for point in points:
        if convert(50, point[0], point[1]) != [255, 255, 255]:
            pygame.draw.circle(screen, convert(50, point[0], point[1]), 
                            ((2.5 * point[0] * math.cos(math.radians(point[1]))) + origin[0], 
                             (2.5 * point[0] * math.sin(math.radians(point[1]))) + origin[1]), 8, 0)
        
    '''
    for i, point in enumerate(points):
        for j in range(l):
            pygame.draw.rect(screen, convert((j * 100 // l) + (50 // l), point[0], point[1]), [(i * 21) + 1, (j * 21) + 1, 20, 20], 0)
    '''
    MainScreen.blit(pygame.transform.scale(screen, (MainScreen.get_width(), MainScreen.get_height())), (0, 0))
    pygame.display.update()

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            current_input.append(event.key)
            if event.key == K_ESCAPE:
                running = False
        if event.type == KEYUP:
            current_input.remove(event.key)
    MainClock.tick(30)

pygame.quit()
sys.exit()