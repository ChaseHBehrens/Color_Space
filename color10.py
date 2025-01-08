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

pixel_size = 10
chroma = 18
n1 = 50
n2 = 1
n3 = 50
space = 0
shift = 28
shift2 = 0

def lightness(x):
    #return 0.9-((((n1-1)-x)/(1.2*(n1-1)))**0.8)
    #return ((math.asin(((2*x)-n1)/n1))/3.5)+0.5
    #return (x/(n1+1))+(1/(2*(n1+1)))
    #return (0.9*(1-((((n1-1)-x)/(n1-1))**0.8)))+0.05
    return (math.atan((2*(x-((n1-1)/2)))/(n1-1))/1.8)+0.5

def update():
    screen = pygame.display.set_mode([(n2*(n3*(pixel_size+space)))+space,(n1*(pixel_size+space))+space],32)
    for l in range(n2):
        hue = 360/n3
        for i in range(n1):
            for j in range(n3):
                color = convert(100*lightness(i),(chroma*(l+1))+shift2,(j*hue)+shift)
                if (0 in color) or (max(color) > 255):
                    color = [round(255*lightness(i)) for l in range(3)]
                pygame.draw.rect(screen,color,[space+(n2*j*(pixel_size+space))+(l*(pixel_size+space)),space+(i*(pixel_size+space)),pixel_size,pixel_size],0)
    pygame.display.flip()
update()

color = []
for l in range(n2):
    hue = 360/n3
    for i in range(n1):
        for j in range(n3):
            c = convert(100*lightness(i),(chroma*(l+1))+shift2,(j*hue)+shift)
            if (0 in c) or (max(c) > 255):
                c = [round(255*lightness(i)) for l in range(3)]
            if not c in color:
                color.append(c)
#print(color)

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
            if event.key == K_r:
                if n3 != 100:
                    n3 += 1
                    update()
            if event.key == K_f:
                if n3 != 1:
                    n3 -= 1
                    update()
            if event.key == K_t:
                if pixel_size != 100:
                    pixel_size += 1
                    update()
            if event.key == K_g:
                if pixel_size != 1:
                    pixel_size -= 1
                    update()
            if event.key == K_y:
                if shift != 100:
                    shift += 1
                    update()
            if event.key == K_h:
                if shift != 1:
                    shift -= 1
                    update()
            if event.key == K_u:
                if shift2 != 100:
                    shift2 += 1
                    update()
            if event.key == K_j:
                if shift2 != 1:
                    shift2 -= 1
                    update()
    mainClock.tick(30)
