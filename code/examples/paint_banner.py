import math
import time
import random
import adafruit_trellism4

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels[0, 0] = (0,0,0)

intensity = 100

board = [[None] * 4 for _ in range(8)]

MODE_EDIT = 0  # Pick a pixel to edit
MODE_SCOL = 1  # Set the color
MODE_VIEW = 2  # View the result
MODE_SAVE = 3  # Load or save

mode = MODE_VIEW
t = 0

all_btns = set((i % 8, i // 8) for i in range(32))
down_prev = frozenset()
down_curr = frozenset()

def btns_update():
    global down_prev, down_curr
    down_prev = down_curr
    down_curr = frozenset(trellis.pressed_keys)

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


coord = 0
ocord = [0, 0]
col = [0, 0, 0]
timer = time.monotonic()
while True:
    btns_update()
    
    for p in btns_pressed():
        if (p == (7, 3)):
            if (mode == MODE_VIEW):
                coord = 0
                t = 0
                mode = MODE_EDIT
                continue
            elif (mode == MODE_EDIT):
                coord = 0
                t = 0
                mode = MODE_VIEW
                continue
            elif (mode == MODE_SCOL):
                board[ocord[0]][ocord[1]] = tuple(col) if col != (0, 0, 0) else None
                while (len(board) > 0 and board[-1] == [None, None, None, None]):
                        board.pop()
                t = 0
                mode = MODE_EDIT
                continue
        
        elif (mode == MODE_VIEW):
            pass
        elif (mode == MODE_EDIT):
            if (p[0] == 7):
                if (p[1] == 0 or p[1] == 1):
                    if (mode == MODE_EDIT):
                        if (coord > 0 or p[1] == 1):
                            coord += 7 * (2 * p[1] - 1)
                elif (p[1] == 2):
                    continue
                    coord = 0
                    t = 0
                    mode = MODE_SAVE
                    continue
            else:
                ocord = [coord + p[0], p[1]]
                while (len(board) <= ocord[0]):
                    board.append([None] * 4)
                col = list(board[ocord[0]][ocord[1]] or (0, 0, 0))
                t = 0
                mode = MODE_SCOL
            continue
        elif (mode == MODE_SCOL):
            if (p[1] < 3):
                row = p[1]
                col[row] = int((p[0] / 7.0) ** 2 * intensity)
    
    
    for x in range(8):
        for y in range(4):
            if (mode == MODE_VIEW):
                trellis.pixels[x, y] = coord + x < len(board) and board[coord + x][y] or (0, 0, 0)
            elif (mode == MODE_EDIT):
                if (x == 7):
                    trellis.pixels[x, y] = (intensity,)*3 if t // 5 % 2 > 0 else (0, 0, 0)
                else:
                    trellis.pixels[x, y] = coord + x < len(board) and board[coord + x][y] or (0, 0, 0)
            elif (mode == MODE_SCOL):
                if (y == 3):
                    trellis.pixels[x, y] = tuple(col)
                else:
                    c = [0, 0, 0]
                    if int((x / 7.0) ** 2 * intensity) <= col[y]:
                        c[y] = intensity
                    trellis.pixels[x, y] = tuple(c)
    
    if (mode == MODE_VIEW):
        if ((t + 1) % 10 == 0):
            coord += 1
            if (coord >= len(board)):
                coord = 0
    
    
    
    
    t += 1
    time.sleep(max(0, timer - time.monotonic()))
    timer += 0.1