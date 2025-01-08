import pygame, sys, math
from pygame.locals import *
pygame.init()
mainClock = pygame.time.Clock()
h = 13
s = 255
b = 0
def function(v,p,i):
    x = round((6*(i-((v+p)*(h/6))))/h,5)
    #return round(255*(-abs(x)+1))
    #return round(255*(-(x**2)+1))
    #return round(255*(((1-(x**2))**0.5)))
    #return round(255*(3**-((2.3*x)**2)))
    return round(255*(((((2*p)-1)*x)+1)**0.75))

def convert(x):
    return round(s*(min([max([x,0]),1])))+b
def strech(x):
    '''
    if x < h/2:
        #return (h/6)+(((((2*x)/3)-(h/6))**3)/((h/6)**2))+(x/3)
        return (h/8)+((((x/2)-(h/8))**3)/((h/8)**2))+(x/2)
        #return x
    else:
        #return ((3*h)/6)+(((((2*x)/3)-((3*h)/6))**3)/((h/6)**2))+(x/3)
        return ((3*h)/8)+((((x/2)-((3*h)/8))**3)/((h/8)**2))+(x/2)
        #return x
    '''
    #return x
    return ((h*math.sin(((12.6/h)*x)+0.5))/30)+x-((h*math.sin(0.5))/30)
def update():
    screen = pygame.display.set_mode([700,700],32)
    for i in range(h):
        if i < h/2:
            #print([convert(max([(6*strech(i))/h,0])**0.75),convert(max([(6*((h/3)-strech(i)))/h,0])**0.75),convert(max([(6*(strech(i)-(h/3)))/h,0])**0.75)])
            pygame.draw.polygon(screen,[convert(max([(6*strech(i))/h,0])**0.75),convert(max([(6*((h/3)-strech(i)))/h,0])**0.75),convert(max([(6*(strech(i)-(h/3)))/h,0])**0.75)]
                                ,[[350,350],[(300*math.cos(i*(6.28/h)))+350,(300*math.sin(i*(6.28/h)))+350],[(300*math.cos((i+1)*(6.28/h)))+350,(300*math.sin((i+1)*(6.28/h)))+350]],0)
        else:
            #print([convert(max([(6*(((2*h)/3)-strech(i)))/h,0])**0.75),convert(max([(6*(strech(i)-((2*h)/3)))/h,0])**0.75),convert(max([(6*(((3*h)/3)-strech(i)))/h,0])**0.75)])
            pygame.draw.polygon(screen,[convert(max([(6*(((2*h)/3)-strech(i)))/h,0])**0.75),convert(max([(6*(strech(i)-((2*h)/3)))/h,0])**0.75),convert(max([(6*(((3*h)/3)-strech(i)))/h,0])**0.75)]
                                ,[[350,350],[(300*math.cos(i*(6.28/h)))+350,(300*math.sin(i*(6.28/h)))+350],[(300*math.cos((i+1)*(6.28/h)))+350,(300*math.sin((i+1)*(6.28/h)))+350]],0)
    pygame.display.flip()
update()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_q:
                h += 1
                update()
            if event.key == K_a:
                if h != 3:
                    h -= 1
                    update()
    
    mainClock.tick(30)
