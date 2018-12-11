import math
import time
import random
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels[0, 0] = (0,0,0)

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
    btns_update()
    
    for p in btns_pressed():
        pixels_on ^= frozenset([p])
        print(p[0], p[1])
        trellis.pixels[p[0], p[1]] = on_col if p in pixels_on else off_col
    
    time.sleep(0.05)
