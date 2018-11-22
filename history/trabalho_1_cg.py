import time
import pygame
tela=pygame.display.set_mode((400,400))
pygame.draw.line(tela,[255,255,255],[50,50],[50,100],5)
pygame.draw.line(tela,[255,255,255],[50,100],[75,100],5)
pygame.display.update()
time.sleep(10)
pygame.quit()
quit()