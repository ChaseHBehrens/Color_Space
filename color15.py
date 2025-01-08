import sys
import math
import random
from typing import *
from functools import partial
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import pygame
from pygame.locals import *
pygame.init()

def convert(color: list[float]):
    """converts lch to rgb color"""
    l, c, h = color
    lab_color = LabColor(l, c * math.cos(math.radians(h)), c * math.sin(math.radians(h)))
    rgb_color = convert_color(lab_color, sRGBColor)
    output = [round(rgb_color.rgb_r * 255), round(rgb_color.rgb_g * 255), round(rgb_color.rgb_b * 255)]
    if not all([e > 0 and e < 255 for e in output]):
        output = [255, 255, 255]
    return output

n = 10
points = [[(x / n) + (0.5 / n) - 0.5, (y / n) + (0.5 / n) - 0.5, (z / n) + (0.5 / n) - 0.5] for x in range(n) for y in range(n) for z in range(n)]

colors = []
for point in points:
    angle = math.degrees(math.atan2(point[2], point[0]))
    if angle < 0:
        angle += 360
    color = convert([(100 * ((point[1] + 0.5) ** 1.2)) + 5, 
                     200 * (((point[0] ** 2) + (point[2] ** 2)) ** 0.5), 
                     angle])
    colors.append(color)
#n = 50
#points = [[(1.618 * i) % 1, i / n, (((1.618 * i) % 1) / 2) + (i / (2 * n))] for i in range(n)]
'''
n = 50
points = [[(1.618 * i) % 1, i / n, j / int(n ** 0.5)] for i in range(n) for j in range(int(n ** 0.5))]
'''
MainClock = pygame.time.Clock()
MainScreen = pygame.display.set_mode((600, 600))
#MainScreen = pygame.display.set_mode(((20 * 30) + 1, (20 * 30) + 1))
pygame.display.set_caption('Color15')
pixel_size = 1
screen = pygame.Surface((MainScreen.get_width() // pixel_size, 
                         MainScreen.get_height() // pixel_size))
origin = (screen.get_width() // 2, screen.get_height() // 2)
current_input = []

class Camera:
    def __init__(self) -> None:
        self.angle1 = 0
        self.angle2 = 0
        self.controles = {K_RIGHT: partial(self.rotate, "angle1", 1),
                          K_LEFT: partial(self.rotate, "angle1", -1),
                          K_UP: partial(self.rotate, "angle2", 1),
                          K_DOWN: partial(self.rotate, "angle2", -1)}
    
    def rotate(self, attribute, speed: float):
        n = getattr(self, attribute)
        n += speed
        if n == 360:
            n = 0
        if n == -1:
            n = 359
        setattr(self, attribute, n)

    def update(self):
        rendering = False
        for key in current_input:
            if key in self.controles:
                self.controles[key]()
                rendering = True
        if rendering:
            self.render()
        
    def calcuate_point(self, point):
        rotated_point = [250 * point[0], 250 * point[1], 250 * point[2]]
        θ = math.radians(self.angle1)
        rotated_point = [(rotated_point[0] * math.cos(θ)) - (rotated_point[2] * math.sin(θ)),
                          rotated_point[1],
                         (rotated_point[0] * math.sin(θ)) + (rotated_point[2] * math.cos(θ))]
        θ = math.radians(self.angle2)
        rotated_point = [rotated_point[0],
                         (rotated_point[1] * math.cos(θ)) - (rotated_point[2] * math.sin(θ)), 
                         (rotated_point[1] * math.sin(θ)) + (rotated_point[2] * math.cos(θ))]
        return rotated_point
    
    def render(self):
        screen.fill((42, 45, 51))
        for i, point in enumerate(points):
            new_point = self.calcuate_point(point)
            
            if colors[i] != [255, 255, 255]:
                pygame.draw.circle(screen, colors[i], [new_point[0] + origin[0], 
                                                   new_point[1] + origin[1]], 8, 0)
        MainScreen.blit(pygame.transform.scale(screen, (MainScreen.get_width(), MainScreen.get_height())), (0, 0))
        pygame.display.update()

camera = Camera()
camera.render()

running  = True
while running:
    camera.update()

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