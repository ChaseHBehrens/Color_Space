import pygame, sys, math
from pygame.locals import *
pygame.init()
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
mainClock = pygame.time.Clock()

def convert(l,c,h):
    lab_color = LabColor(l, c * math.cos(math.radians(h)), c * math.sin(math.radians(h)))
    rgb_color = convert_color(lab_color, sRGBColor)
    output = [round(rgb_color.rgb_r * 255), round(rgb_color.rgb_g * 255), round(rgb_color.rgb_b * 255)]
    if not all([e > 0 and e < 255 for e in output]):
        output = [255, 255, 255]
    return output

pixel_size = 20
n = 20
def lightness(x):
    #return (0.9*(1-(((n-x)/n)**0.6)))+0.05
    #return ((x+3)/(n+3))**2
    #return (x/(n+1))+(1/(2*(n+1)))
    #return (math.sin(3.14*((x/(n-1))-0.5))/2.5)+0.5
    #return ((math.asin(((2*x)-n)/n))/3.5)+0.5
    #return 0.95-((((n-1)-x)/(1.2*(n-1)))**0.8)
    #return (math.atan((2.5*(x-((n-1)/2)))/(n-1))/2)+0.5
    return (x / n) ** 1.2

def update():
    screen = pygame.display.set_mode([(n*(pixel_size))+8,(2*pixel_size)+12],32)
    for i in range(n):
        color = [round(255*lightness(i)) for l in range(3)]
        pygame.draw.rect(screen,color,[4+(i*(pixel_size)),4,pixel_size,pixel_size],0)
        color = convert(60, (200 * i/n), 320)
        pygame.draw.rect(screen,color,[4+((4+i)*(pixel_size)),8 + pixel_size,pixel_size,pixel_size],0)
    pygame.display.flip()
update()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_q:
                if n != 150:
                    n += 1
                    update()
            if event.key == K_a:
                if n != 3:
                    n -= 1
                    update()
    mainClock.tick(30)
