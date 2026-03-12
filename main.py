import pygame
import time

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

r, g, b = 255, 0, 0

while True:

    # rouge -> jaune
    for g in range(0, 256):
        screen.fill((255, g, 0))
        pygame.display.flip()

    # jaune -> vert
    for r in range(255, -1, -1):
        screen.fill((r, 255, 0))
        pygame.display.flip()

    # vert -> cyan
    for b in range(0, 256):
        screen.fill((0, 255, b))
        pygame.display.flip()

    # cyan -> bleu
    for g in range(255, -1, -1):
        screen.fill((0, g, 255))
        pygame.display.flip()

    # bleu -> magenta
    for r in range(0, 256):
        screen.fill((r, 0, 255))
        pygame.display.flip()

    # magenta -> rouge
    for b in range(255, -1, -1):
        screen.fill((255, 0, b))
        pygame.display.flip()