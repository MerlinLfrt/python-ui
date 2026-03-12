import os
import pygame

# utiliser le framebuffer au lieu de X11 / EGL
os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"

pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

while True:

    # rouge -> jaune
    for g in range(256):
        screen.fill((255, g, 0))
        pygame.display.update()

    # jaune -> vert
    for r in range(255, -1, -1):
        screen.fill((r, 255, 0))
        pygame.display.update()

    # vert -> cyan
    for b in range(256):
        screen.fill((0, 255, b))
        pygame.display.update()

    # cyan -> bleu
    for g in range(255, -1, -1):
        screen.fill((0, g, 255))
        pygame.display.update()

    # bleu -> magenta
    for r in range(256):
        screen.fill((r, 0, 255))
        pygame.display.update()

    # magenta -> rouge
    for b in range(255, -1, -1):
        screen.fill((255, 0, b))
        pygame.display.update()