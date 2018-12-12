from pygame import gfxdraw
color = (123,49,125)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
import pygame
from pygame.locals import *
import numpy
from math import *
import copy
pygame.init()
(6, 0)
pygame.display.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
screen.fill((255, 255, 255))
branco=[0,0,0]
gfxdraw.pixel(screen,100,100,branco)
gfxdraw.pixel(screen,105,105,branco)
gfxdraw.pixel(screen,102,102,branco)
gfxdraw.pixel(screen,104,104,branco)
gfxdraw.pixel(screen,103,103,branco)
gfxdraw.pixel(screen,101,101,branco)
#pygame.display.flip()

