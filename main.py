import numpy as np
import time

# --- Configuration ---
WIDTH = 800
HEIGHT = 480
FB_PATH = "/dev/fb0"

# Balle
BALL_RADIUS = 30
BALL_COLOR = (255, 80, 0)       # Orange vif
TRAIL_COLOR = (255, 30, 0)      # Rouge pour la traînée
BG_COLOR = (10, 10, 30)         # Fond bleu nuit

# Physique
SPEED_X = 4.5
SPEED_Y = 3.2
GRAVITY = 0.12                  # Légère gravité
DAMPING = 0.98                  # Amortissement sur rebond

# --- Framebuffer ---
fb = open(FB_PATH, "r+b")

# Buffer numpy (BGRX 32-bit)
frame = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)

def set_pixel(buf, x, y, r, g, b):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        buf[y, x] = [b, g, r, 0]

def draw_circle_filled(buf, cx, cy, radius, r, g, b, alpha=1.0):
    """Dessine un cercle plein avec anti-aliasing simple."""
    x0 = max(0, int(cx - radius - 1))
    x1 = min(WIDTH, int(cx + radius + 2))
    y0 = max(0, int(cy - radius - 1))
    y1 = min(HEIGHT, int(cy + radius + 2))

    for y in range(y0, y1):
        for x in range(x0, x1):
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if dist < radius - 1:
                buf[y, x] = [b, g, r, 0]
            elif dist < radius + 0.5:
                # Anti-aliasing
                t = 1.0 - (dist - (radius - 1))
                t = max(0.0, min(1.0, t))
                bg = buf[y, x]
                buf[y, x] = [
                    int(bg[0] * (1 - t) + b * t),
                    int(bg[1] * (1 - t) + g * t),
                    int(bg[2] * (1 - t) + r * t),
                    0
                ]

def draw_glow(buf, cx, cy, radius, r, g, b, layers=4):
    """Effet de halo lumineux autour de la balle."""
    for i in range(layers, 0, -1):
        glow_r = radius + i * 6
        alpha = 0.08 * (layers - i + 1)
        x0 = max(0, int(cx - glow_r - 1))
        x1 = min(WIDTH, int(cx + glow_r + 2))
        y0 = max(0, int(cy - glow_r - 1))
        y1 = min(HEIGHT, int(cy + glow_r + 2))
        for y in range(y0, y1):
            for x in range(x0, x1):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if dist < glow_r:
                    t = alpha * max(0, 1 - dist / glow_r)
                    bg = buf[y, x]
                    buf[y, x] = [
                        min(255, int(bg[0] + b * t)),
                        min(255, int(bg[1] + g * t)),
                        min(255, int(bg[2] + r * t)),
                        0
                    ]

def draw_trail(buf, trail, r, g, b):
    """Dessine la traînée avec fondu."""
    n = len(trail)
    for i, (tx, ty) in enumerate(trail):
        t = (i + 1) / n
        tr = int(r * t * 0.6)
        tg = int(g * t * 0.6)
        tb = int(b * t * 0.6)
        rad = int(BALL_RADIUS * t * 0.8)
        if rad > 1:
            draw_circle_filled(buf, tx, ty, rad, tr, tg, tb)

def draw_background(buf):
    """Fond dégradé bleu nuit."""
    br, bg_c, bb = BG_COLOR
    for y in range(HEIGHT):
        factor = y / HEIGHT
        r = int(br * (1 - factor * 0.5))
        g = int(bg_c * (1 - factor * 0.3))
        b = int(bb + (60 - bb) * factor)
        buf[y, :] = [b, g, r, 0]

def draw_grid(buf):
    """Grille subtile en fond."""
    grid_color = [20, 15, 35, 0]  # BGRX
    step = 40
    for x in range(0, WIDTH, step):
        buf[:, x] = grid_color
    for y in range(0, HEIGHT, step):
        buf[y, :] = grid_color

def flush(buf):
    fb.seek(0)
    fb.write(buf.tobytes())

# --- État initial ---
ball_x = WIDTH / 2.0
ball_y = HEIGHT / 2.0
vel_x = SPEED_X
vel_y = SPEED_Y
trail = []
TRAIL_LEN = 12

# Pré-dessiner le fond (statique)
bg_frame = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
draw_background(bg_frame)
draw_grid(bg_frame)

print("Balle rebondissante démarrée. Ctrl+C pour quitter.")

try:
    while True:
        t_start = time.monotonic()

        # Copier le fond
        frame[:] = bg_frame

        # Physique
        vel_y += GRAVITY
        ball_x += vel_x
        ball_y += vel_y

        # Rebonds
        bounced = False
        if ball_x - BALL_RADIUS <= 0:
            ball_x = BALL_RADIUS
            vel_x = abs(vel_x) * DAMPING
            bounced = True
        elif ball_x + BALL_RADIUS >= WIDTH:
            ball_x = WIDTH - BALL_RADIUS
            vel_x = -abs(vel_x) * DAMPING
            bounced = True

        if ball_y - BALL_RADIUS <= 0:
            ball_y = BALL_RADIUS
            vel_y = abs(vel_y) * DAMPING
            bounced = True
        elif ball_y + BALL_RADIUS >= HEIGHT:
            ball_y = HEIGHT - BALL_RADIUS
            vel_y = -abs(vel_y) * DAMPING
            bounced = True

        # Traînée
        trail.append((int(ball_x), int(ball_y)))
        if len(trail) > TRAIL_LEN:
            trail.pop(0)

        # Dessin
        draw_trail(frame, trail[:-1], *TRAIL_COLOR)
        draw_glow(frame, ball_x, ball_y, BALL_RADIUS, *BALL_COLOR)
        draw_circle_filled(frame, ball_x, ball_y, BALL_RADIUS, *BALL_COLOR)

        # Reflet sur la balle (highlight)
        draw_circle_filled(frame,
                           ball_x - BALL_RADIUS * 0.3,
                           ball_y - BALL_RADIUS * 0.3,
                           BALL_RADIUS * 0.25,
                           255, 220, 180)

        flush(frame)

        # ~60 FPS cible
        elapsed = time.monotonic() - t_start
        sleep_time = (1.0 / 60.0) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\nArrêt.")
    fb.close()