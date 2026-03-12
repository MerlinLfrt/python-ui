import numpy as np
import time

fb = open("/dev/fb0", "r+b")

width = 800
height = 480

def fill(color):
    r, g, b = color
    pixel = bytes([b, g, r, 0])  # format BGRX
    frame = pixel * width * height
    fb.seek(0)
    fb.write(frame)

while True:

    for g in range(256):
        fill((255, g, 0))

    for r in range(255, -1, -1):
        fill((r, 255, 0))

    for b in range(256):
        fill((0, 255, b))

    for g in range(255, -1, -1):
        fill((0, g, 255))

    for r in range(256):
        fill((r, 0, 255))

    for b in range(255, -1, -1):
        fill((255, 0, b))