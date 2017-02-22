from random import randrange
from geom.geomcom import Punto2D
from geom.funciones import *
import pygame, sys
from pygame.locals import *



puntos = []

ps = [(181, 40), (119, 121), (245, 226), (180, 90), (377, 225), (293, 285), (294, 46)]

for i in ps:
    puntos.append(Punto2D(i[0], i[1]))

pt = puntos.copy()



pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Drawing')

# set up the colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)

# draw on the surface object
DISPLAYSURF.fill(WHITE)

for i in puntos:
    pygame.draw.circle(DISPLAYSURF, RED, (i.x, i.y), 2, 0)








print(puntos)

envolvente = []

D = {}

for i in range(len(ps)):
    for j in range(len(ps)):
        if i is not j:

            if j > i:
                pt.remove(pt[j])
                pt.remove(pt[i])
            else:
                pt.remove(pt[i])
                pt.remove(pt[j])

        for k in pt:
            if not is_to_the_left_of_line(k, puntos[i], puntos[j]):
                break
        else:
            D[i] = j

        pt = puntos.copy()

print(ps)
print(envolvente)

print(D)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()

