import sys
import math
import numpy as np
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

n = 20
l = 10
colors = []
for j in range(l):
    colors += [[(j * 100 // l) + (50 // l),
                100 * ((i / (n - 1)) ** 0.5), 
                360 * (((2 * i) / (1 + (5 ** 0.5))) % 1)] for i in range(n)]
colors.sort(key=lambda x: x[1])

points = []
for a in range(0, 360, 10): 
    for r in range(50, 100, 50): 
        for h in range(0, 100, 10):
            points.append([h, r, a])

MainClock = pygame.time.Clock()
MainScreen = pygame.display.set_mode((600, 600))
#MainScreen = pygame.display.set_mode(((20 * 30) + 1, (20 * 30) + 1))
pygame.display.set_caption('Color13')
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
        for key in current_input:
            if key in self.controles:
                self.controles[key]()
        
    def calcuate_point(self, point):
        def quaternion_multiply(q1, q2):
            w1, x1, y1, z1 = q1
            w2, x2, y2, z2 = q2
            
            w = w1*w2 - x1*x2 - y1*y2 - z1*z2
            x = w1*x2 + x1*w2 + y1*z2 - z1*y2
            y = w1*y2 - x1*z2 + y1*w2 + z1*x2
            z = w1*z2 + x1*y2 - y1*x2 + z1*w2
            
            return np.array([w, x, y, z])
        def quaternion_rotation(point, axis, angle):
            # Compute quaternion components
            half_angle = angle / 2
            w = np.cos(half_angle)
            x = axis[0] * np.sin(half_angle)
            y = axis[1] * np.sin(half_angle)
            z = axis[2] * np.sin(half_angle)
            
            # Create quaternion and its conjugate
            q = np.array([w, x, y, z])
            q_conj = np.array([w, -x, -y, -z])
            
            # Convert point to a pure quaternion
            p = np.array([0, point[0], point[1], point[2]])
            
            # Perform quaternion multiplication q * p * q_conj
            temp = quaternion_multiply(q, p)
            p_prime = quaternion_multiply(temp, q_conj)
            
            # Extract the rotated point
            rotated_point = p_prime[1:]  # Skip the scalar part
            return rotated_point

        rotated_point = quaternion_rotation(point, [0, 1, 0], np.radians(self.angle1))
        rotated_point = quaternion_rotation(rotated_point, [1, 0, 0], np.radians(self.angle2))
        return rotated_point

camera = Camera()

running  = True
while running:
    camera.update()
    '''
    # update number of colors
    if K_RIGHT in current_input:
        n += 1
        color_points = [[50, 100 * ((i / (n - 1)) ** 0.5), 360 * (((2 * i) / (1 + (5 ** 0.5))) % 1)] for i in range(n)]
    if K_LEFT in current_input:
        n -= 1
        color_points = [[50, 100 * ((i / (n - 1)) ** 0.5), 360 * (((2 * i) / (1 + (5 ** 0.5))) % 1)] for i in range(n)]
    '''
    # update the screen
    screen.fill((42, 45, 51))
    '''
    counter = 0
    for i, color in enumerate(colors):
        if convert(color) != [255, 255, 255]:
            pygame.draw.rect(screen, convert(color), 
                             [(((i - counter) % 30) * 20) + 1, 
                              (((i - counter) // 30) * 20) + 1, 19, 19], 0)
        else:
            counter += 1
    '''
    points = [[camera.calcuate_point([2.5 * color[1] * math.cos(math.radians(color[2])), 
                                      2.5 * (color[0] - 50), 
                                      2.5 * color[1] * math.sin(math.radians(color[2])),]), convert(color)] for color in colors]
    points.sort(key=lambda x: x[0][2], reverse=True)
    for point in points:
        if point[1] != [255, 255, 255]:
            pygame.draw.circle(screen, point[1], [point[0][0] + origin[0], 
                                                  point[0][1] + origin[1]], 10, 0)
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