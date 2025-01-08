import sys
import math
from typing import *
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import pygame
from pygame.locals import *
pygame.init()

def draw_pie(surface: pygame.Surface, color: list[int], center: list[int], start_angle: int, distance: int, outer_radius: int, width: int=0, boarder: int=0):
    if width == 0:
        inner_radius = 0
    else:
        inner_radius = outer_radius - width
    pygame.draw.polygon(surface, color,
                        [((inner_radius * math.cos(math.radians(angle - (start_angle + distance)))) + center[0], 
                          (inner_radius * math.sin(math.radians(angle - (start_angle + distance)))) + center[1])
                         for angle in range(distance)] +
                        [((outer_radius * math.cos(math.radians(-start_angle - angle))) + center[0], 
                          (outer_radius * math.sin(math.radians(-start_angle - angle))) + center[1]) 
                         for angle in range(distance)], boarder)
pygame.draw.pie = draw_pie

def convert(l: float, c: float, h: float):
    """converts lch to rgb color"""
    lab_color = LabColor(l, c * math.cos(math.radians(h)), c * math.sin(math.radians(h)))
    rgb_color = convert_color(lab_color, sRGBColor)
    output = [round(rgb_color.rgb_r * 255), round(rgb_color.rgb_g * 255), round(rgb_color.rgb_b * 255)]
    if not all([e > 0 and e < 255 for e in output]):
        output = [255, 255, 255]
    return output

h_number = 13
c_number = 4
l_number = 10

h_distances = [i * 360 // h_number for i in range(h_number)]

total_area = 31415.9
area = total_area / c_number
c_distances = [0 for _ in range(c_number + 1)]
c_distances[0] = round((area / (3.14159 + h_number)) ** 0.5)
for i in range(c_number - 1):
    c_distances[i + 1] = round(((area / 3.14159) + (c_distances[i] ** 2)) ** 0.5)
c_distances[-1] = 105

l_distances = [(i * 100 // l_number) + (50 // l_number) for i in range(l_number)]

MainClock = pygame.time.Clock()
MainScreen = pygame.display.set_mode((21 * c_number * h_number, 21 * l_number))
pygame.display.set_caption('Color11')
pixel_size = 1
screen = pygame.Surface((MainScreen.get_width() // pixel_size, 
                         MainScreen.get_height() // pixel_size))
origin = (screen.get_width() // 2, screen.get_height() // 2)
current_input = []

running  = True
while running:
    # update the screen
    screen.fill((255, 255, 255))
    '''
    for c in range(c_number):
        for h in range(h_number):
            color = convert(l_distances[5], c_distances[c], h_distances[h])
            pygame.draw.pie(screen, color, origin, 
                            h_distances[h], (360 // h_number) - 2,
                            2.5 * c_distances[c + 1], (2.5 * (c_distances[c + 1] - c_distances[c])) - 4, 0)
    pygame.draw.circle(screen, convert(l_distances[5], 0, 0), origin, c_distances[0] * 2.5, 0)
    '''
    for i, l in enumerate(l_distances):
        pygame.draw.rect(screen, convert(l, 0, 0), [0, i * 21, 20, 20])
        for j, c in enumerate(c_distances[:-1]):
            for k, h in enumerate(h_distances):
                pygame.draw.rect(screen, convert(l, c, h), [(j * 21) + (k * 21 * c_number) + 21, (l_number - i) * 21, 20, 20], 0)

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