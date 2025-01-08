import pygame, sys, math
from pygame.locals import *
pygame.init()
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
mainClock = pygame.time.Clock()

def convert(l,c,h):
    lab_color = LabColor(l, c * math.cos(math.radians(h)), c * math.sin(math.radians(h)))
    rgb_color = convert_color(lab_color, sRGBColor)
    return [round(rgb_color.rgb_r * 255),round(rgb_color.rgb_g * 255),round(rgb_color.rgb_b * 255)]

pixel_size = 40
chroma = 50
n1 = 10
n2 = 20
def lightness(x):
    return (0.9*(1-(((n1-x)/n1)**0.75)))+0.05

def update():
    screen = pygame.display.set_mode([(n2*(pixel_size+4))+4,(n1*(pixel_size+4))+4],32)
    hue = 360/n2
    for i in range(n1):
        for j in range(n2):
            color = convert(100*lightness(i),chroma,j*hue)
            if (0 in color) or (max(color) > 255):
                color = [round(255*lightness(i)) for l in range(3)]
            pygame.draw.rect(screen,color,[4+(j*(pixel_size+4)),4+(i*(pixel_size+4)),pixel_size,pixel_size],0)
    pygame.display.flip()
update()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_q:
                if chroma != 150:
                    chroma += 1
                    update()
            if event.key == K_a:
                if chroma != 0:
                    chroma -= 1
                    update()
            if event.key == K_w:
                if n1 != 100:
                    n1 += 1
                    update()
            if event.key == K_s:
                if n1 != 1:
                    n1 -= 1
                    update()
            if event.key == K_e:
                if n2 != 100:
                    n2 += 1
                    update()
            if event.key == K_d:
                if n2 != 1:
                    n2 -= 1
                    update()
    mainClock.tick(30)
