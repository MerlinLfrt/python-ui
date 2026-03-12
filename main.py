import numpy as np
import time

fb = open("/dev/fb0", "r+b")

WIDTH = 800
HEIGHT = 480
RADIUS = 40

# Créer le framebuffer comme tableau numpy
frame = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)  # BGRX

def draw_circle(frame, cx, cy, radius, color):
    """Dessine un cercle rempli"""
    y, x = np.ogrid[:HEIGHT, :WIDTH]
    mask = (x - cx)**2 + (y - cy)**2 <= radius**2
    frame[mask] = color

def render(frame):
    fb.seek(0)
    fb.write(frame.tobytes())

# Position et vitesse du cercle
x, y = WIDTH // 2, HEIGHT // 2
vx, vy = 4, 3

while True:
    # Effacer l'écran (noir)
    frame[:] = 0

    # Déplacer le cercle
    x += vx
    y += vy

    # Rebondir sur les bords
    if x - RADIUS <= 0 or x + RADIUS >= WIDTH:
        vx = -vx
    if y - RADIUS <= 0 or y + RADIUS >= HEIGHT:
        vy = -vy

    # Dessiner le cercle blanc (BGRX = 255, 255, 255, 0)
    draw_circle(frame, x, y, RADIUS, [255, 255, 255, 0])

    render(frame)
    time.sleep(0.016)  # ~60 FPS