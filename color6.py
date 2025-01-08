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
chroma_max = 53
n1 = 10
n2 = 12
shift = 0
def lightness(x):
    #return x/n1
    #return (0.9*(1-(((n1-x-1)/(n1-1))**0.7)))+0.05
    return ((x+3)/(n1+3))**2
def chroma(x):
    #return (chroma_max*x)/n1
    return -abs((chroma_max*((2*(n1*lightness(x)))-(n1-1)))/(n1-1))+chroma_max
    #return chroma_max-((((2*(chroma_max**0.5))*((n1*lightness(x))-(n1/2)))/n1)**2)
    #return chroma_max-((((chroma_max**0.5)*(x-n1))/n1)**2)

def update():
    #print(shift)
    screen = pygame.display.set_mode([((n2+1)*(pixel_size+4))+4+(pixel_size//2),(n1*(pixel_size+4))+4],32)
    s = 180/n2
    hue = 360/n2
    for i in range(n1):
        for j in range(n2):
            color = convert(100*lightness(i),chroma(i),shift+(j*hue)+(s*(i%2)))
            
            if (0 in color) or (max(color) > 255):
                color = [round(255*lightness(i)) for l in range(3)]
            pygame.draw.rect(screen,color,[4+(j*(pixel_size+4))+((i%2)*(pixel_size//2)),4+(i*(pixel_size+4)),pixel_size,pixel_size],0)
        color = [round(255*lightness(i)) for l in range(3)]
        pygame.draw.rect(screen,color,[4+(n2*(pixel_size+4))+((i%2)*(pixel_size//2)),4+(i*(pixel_size+4)),pixel_size,pixel_size],0)
    pygame.display.flip()
update()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_q:
                if chroma_max != 150:
                    chroma_max += 1
                    update()
            if event.key == K_a:
                if chroma_max != 0:
                    chroma_max -= 1
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
                if shift != 100:
                    shift += 1
                    update()
            if event.key == K_f:
                if shift != -100:
                    shift -= 1
                    update()
    mainClock.tick(30)
