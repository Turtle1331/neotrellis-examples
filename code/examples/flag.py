import math
import time
import random
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels[0, 0] = (0,0,0)

k = 100
cols = [(0,k//3,k),(k,0,k),(int(k*1.5),int(k*1.5),int(k*1.5)),(k,0,k),(0,k//3,k)]

pixels_on = set()
on_col = (0,10,0)
off_col = (0,0,0)


all_btns = set((i % 8, i // 8) for i in range(32))
down_prev = frozenset()
down_curr = frozenset()

def btns_update():
    global down_prev, down_curr
    down_prev = down_curr
    down_curr = frozenset(trellis.pressed_keys)
    if len(down_curr) > 0: print(trellis.pressed_keys)

def btns_down():
    global down_curr
    return down_curr

def btns_up():
    global all_btns, down_curr
    return all_btns - down_curr

def btns_pressed():
    global down_prev, down_curr
    return down_curr - down_prev

def btns_released():
    global down_prev, down_curr
    return down_prev - down_curr


while True:
    t = 0
    while len(trellis.pressed_keys) == 0:
        for x in range(8):
            for y in range(4):
                trellis.pixels[x, y] = cols[((x + t) // 2) % len(cols)]
        t += 1
        time.sleep(0.125)

    while len(trellis.pressed_keys) != 0:
        pass

    for x in range(8):
        for y in range(4):
            trellis.pixels[x, y] = (0, 0, 0)

    while len(trellis.pressed_keys) == 0:
        pass
    while len(trellis.pressed_keys) != 0:
        pass