import math
import time
import random
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.fill((0,0,0))
trellis.pixels.auto_write = False

on_col = (0, 25, 0)


alphabet = {
    'A': 1959, # 4015,
    'B': 4051, # 3922,
    'C': 3993,
    'D': 3990,
    'E': 4057, # 4061,
    'F': 4008, # 4010,
    'G': 3995,
    'H': 3951,
    'I': 2553,
    'J':  542, #  670,
    'K': 3945,
    'L': 3857,
    'M': 3919,
    'N': 3975, # 3983,
    'O': 1686,
    'P': 4004,
    'Q': 1687,
    'R': 4005,
    'S': 1466,
    'T': 2296,
    'U': 3871, # 3615,
    'V': 3614,
    'W': 3887,
    'X': 2891,
    'Y': 3132,
    'Z': 3033, # 2493,
    '0': 3999,
    '1': 1521,
    '2': 2485,
    '3': 2527,
    '4': 3631,
    '5': 3546,
    '6': 4027, # 1989,
    '7': 2191, # 2235,
    '8': 4031,
    '9': 3551,
    ' ':    0,
    '.':   16,
    ',':  288,
    '!':  208,
    '?':  180,
    ':':  144,
    ';': 2464, #  416,
    '\'': 192,
    '"':  200, #  196,
    '/':  300,
    '\\':3105,
    '<':  592, #  597,
    '>': 1312, # 1352,
    '+':  626,
    '-':  546,
    '*': 3264, # 1252,
    '^': 1156,
    '_':  273,
    '=': 1365,
    '(': 1680,
    ')': 2400,
    '[': 3984,
    ']': 2544,
    '{': 1273,
    '}': 2548,
    '#': 1782, # 1791,
    '%': 2349,
    '&': 1021,
    '|':  240,
    '$': 1266,
    '@': 1791, # 3831,
    '~': 612,
    '`': 2112,
}

def get_letter(c):
    c = c.upper()
    if c not in alphabet:
        return None
    b = alphabet[c]
    return set((2 - i // 4, 3 - i % 4) for i in range(12) if b & (1 << i))

def get_message(m):
    s = set()
    for i, c in enumerate(m):
        s ^= set((p[0] + 4 * i, p[1]) for p in get_letter(c))
    return s



all_btns = set((i % 8, i // 8) for i in range(32))
down_prev = frozenset()
down_curr = frozenset()

def btns_update():
    global down_prev, down_curr
    down_prev = down_curr
    down_curr = frozenset(trellis.pressed_keys)
    #if len(down_curr) > 0: print(trellis.pressed_keys)

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


pixels_on = get_message('hi')
for p in pixels_on:
    trellis.pixels[p] = on_col


message = 'Hello, World!!'
dots = get_message(message)
scroll = 0

while True:
    btns_update()
    
    for p in btns_pressed():
        pass
    
    trellis.pixels.fill((0,0,0))
    for dot in dots:
        if (0 <= dot[0] - scroll + 8 < 8 and 0 <= dot[1] < 4):
            trellis.pixels[dot[0] - scroll + 8, dot[1]] = on_col
    trellis.pixels.show()
    
    scroll += 1
    scroll %= len(message) * 4 + 8
    
    time.sleep(0.25)
