import sys
import math
import random
from typing import *
from functools import partial
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import pygame
from pygame.locals import *
import numpy as np
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


def translate_polar(r, theta, dx, dy):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    x_new = x + dx
    y_new = y + dy
    new_r = np.sqrt(x_new**2 + y_new**2)
    new_theta = np.arctan2(y_new, x_new)
    return new_r, new_theta

def hex_circle_packing(circle_radius, max_radius, offset2):
    d = 2 * circle_radius
    centers = []
    if offset2:
        r, theta = translate_polar(0, 0, circle_radius, (circle_radius * (3 ** 0.5)) / -3)
        centers.append((r, theta))
    else:
        centers.append((0, 0))
    ring = 1
    while ring * d <= max_radius + d:
        base_radius = ring * d
        theta_step = 2 * np.pi / 6
        for i in range(6):
            circles_per_edge = ring if ring > 1 else 1
            for j in range(circles_per_edge):
                # Base position for this edge
                r = base_radius
                theta = i * theta_step
                if circles_per_edge > 1:
                    offset = j * d
                    r = np.sqrt(base_radius**2 + offset**2 - 
                              2 * base_radius * offset * np.cos(np.pi/3))
                    theta_offset = np.arcsin(offset * np.sin(np.pi/3) / r)
                    theta += theta_offset
                if offset2:
                    r, theta = translate_polar(r, theta, circle_radius, (circle_radius * (3 ** 0.5)) / -3)
                if r <= max_radius:
                    centers.append((r, theta))
        ring += 1
    return centers

#offset = 40
offset = 22
#n = 49
n = 10
colors = []
for i in range(round(n)):
    points = hex_circle_packing((100/n), 100, False)
    for point in points:
        colors.append([100 * (((i/n) + (1/(2*n))) ** 0.9), 80 * (point[0]/100) ** 1.2, offset + math.degrees(point[1])])

colors = list(filter(lambda x: convert(x) != [255, 255, 255] and x[1] < 50, colors))
print(len(colors))

'''
hashmap = {}
for color in colors:
    hashmap[(round(color[0]), round(color[1]), round(color[2]) % 360)] = tuple(convert(color))
for x, y in hashmap.items():
    print(f"{x}: {y},")
'''
    
MainClock = pygame.time.Clock()
MainScreen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Color19')
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
                          K_DOWN: partial(self.rotate, "angle2", -1),
                          K_RSHIFT: partial(self.update_offset, 1),
                          K_LSHIFT: partial(self.update_offset, -1)}
        
    def update_offset(self, speed):
        global offset, colors
        offset += speed
        offset %= 120
        colors = []
        for i in range(round(n)):
            if i%2:
                points = hex_circle_packing((100/n), 100, True)
            else:
                points = hex_circle_packing((100/n), 100, False)
            for point in points:
                colors.append([100 * (((i/n) + (1/(2*n))) ** 0.9), 215 * (point[0]/100) ** 1.2, ((i%2)*(i+1)*30) + offset + math.degrees(point[1])])

        colors = list(filter(lambda x: convert(x) != [255, 255, 255] and x[1] < 50, colors))
        self.render()
        print(f"{offset} - {len(colors)}")
    
    def rotate(self, attribute, speed: float):
        n = getattr(self, attribute)
        n += 2*speed
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
        rotated_point = [point[0], point[1], point[2] + self.angle1]
        rotated_point = [10 * (rotated_point[1] ** (1 / 1.2)) * math.cos(math.radians(rotated_point[2])), 
                         2.5 * (75 - (rotated_point[0] ** (1 / 0.9))), 
                         10 * (rotated_point[1]  ** (1 / 1.2)) * math.sin(math.radians(rotated_point[2])),]
        θ = math.radians(self.angle2)
        rotated_point = [rotated_point[0],
                         (rotated_point[1] * math.cos(θ)) - (rotated_point[2] * math.sin(θ)), 
                         (rotated_point[1] * math.sin(θ)) + (rotated_point[2] * math.cos(θ))]
        return rotated_point
    
    def render(self):
        screen.fill((42, 45, 51))
        points = [[camera.calcuate_point(color), convert(color)] for color in colors]
        points.sort(key=lambda x: x[0][2], reverse=True)
        for point in points:
            pygame.draw.circle(screen, point[1], [point[0][0] + origin[0], 
                                                    point[0][1] + origin[1]], 8, 0)
        MainScreen.blit(pygame.transform.scale(screen, (MainScreen.get_width(), MainScreen.get_height())), (0, 0))
        pygame.display.update()

camera = Camera()
camera.render()
'''
screen.fill((255, 255, 255))
for i, color in enumerate(colors):
    print(i)
    if i < 11:
        pygame.draw.rect(screen, convert(color),[i*40, 0, 40, 300])
    else:
        pygame.draw.rect(screen, convert(color),[(i-11)*40, 300, 40, 300])
MainScreen.blit(pygame.transform.scale(screen, (MainScreen.get_width(), MainScreen.get_height())), (0, 0))
pygame.display.update()
'''

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