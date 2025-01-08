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

pixel_size = 30
chroma_max = 65
n1 = 10
n2 = 12
shift = 0
def lightness(x):
    return ((x/n1)*0.9)+0.05
    #return (0.9*(1-(((n1-x-1)/(n1-1))**0.7)))+0.05
    #return ((x+3)/(n1+3))**2
def chroma(x):
    return chroma_max
    #return (chroma_max*x)/n1
    #return -abs((chroma_max*((2*x)-(n1-1)))/(n1-1))+chroma_max
    #return chroma_max-((((2*(chroma_max**0.5))*((n1*lightness(x))-(n1/2)))/n1)**2)
    #return chroma_max-((((chroma_max**0.5)*(x-n1))/n1)**2)

map3d = [[None for i in range(360)]for j in range(n1)]
colors = [[] for i in range(n1)]
angles = [[] for i in range(n1)]

for l in range(n1):
    for d in range(360):
        color = convert(100*lightness(l),chroma(l),d)
        k = 0
        while (0 in color) or (max(color) > 255):
            k += 0.5
            color = convert(100*lightness(l),chroma(l)-k,d)
        map3d[l][d] = chroma(l)-k
    distances = []
    for d in range(360):
        distances.append(((map3d[l][d-1]**2)+(map3d[l][d]**2)-(2*map3d[l][d]*map3d[l][d-1]*math.cos(math.radians(1))))**0.5)

    #distance = 30
    #distance += (sum(distances)%distance)/(sum(distances)//distance)
    distance = sum(distances)/10
    print(int(sum(distances)/distance))
    for i in range(int(sum(distances)/distance)):
        k = 0
        d = distances[0]
        while i*distance > d:
            k += 1
            d += distances[k]
        colors[l].append(convert(100*lightness(l),map3d[l][k],k))
        angles[l].append(k)


screen = pygame.display.set_mode([800,800],32)
screen.fill([200,200,200])
max_length = (max([len(colors[i]) for i in range(len(colors))])*(pixel_size+4))+4
for i in range(n1):
    length = (len(colors[i])*(pixel_size+4))+4
    strech = (max_length-length)/len(colors[i])
    for j in range(len(colors[i])):
        pygame.draw.rect(screen,colors[i][j],[angles[i][j]*2,(i*(pixel_size+4))+4,pixel_size,pixel_size],0)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    mainClock.tick(30)
