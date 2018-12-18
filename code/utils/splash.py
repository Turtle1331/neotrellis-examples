import os
import math
import time
import random
import board
import audioio
import adafruit_trellism4
import deinit_trellis

def main():
    trellis = adafruit_trellism4.TrellisM4Express()
    trellis.pixels.fill((0,0,0))
    trellis.pixels.auto_write = False
    
    while len(trellis.pressed_keys) > 0:
        time.sleep(0.01)

    timer = time.monotonic()
    t = 0
    while len(trellis.pressed_keys) == 0:
        i = int(100 * (-math.cos(2 * math.pi * t) * 0.5 + 0.5) ** 2)
        c = (i, i, i)
        
        trellis.pixels[0, 0] = c
        trellis.pixels[7, 0] = c
        trellis.pixels[0, 3] = c
        trellis.pixels[7, 3] = c
        trellis.pixels.show()
        
        time.sleep(0.01)
        t = time.monotonic() - timer



    audio = audioio.AudioOut(board.A1, right_channel=board.A0)
    f = open('tuba_fanfare.wav', 'rb')
    wav = audioio.WaveFile(f)
    audio.play(wav)

    timer = time.monotonic()
    t = 0
    m = 0.25
    while t < 2:
        p = t / 2.0 + 0.1
        for x in range(8):
            for y in range(4):
                d = 1 - (abs(x - 3.5) + abs(y - 1.5)) / 5
                v = p + m * (p - d)
                v = max(0, min(2, 2 * v))
                v = 1 - abs(1 - v)
                i = int(100 * v ** 3)
                trellis.pixels[x, y] = (i, i, i)
        trellis.pixels.show()
        
        
        time.sleep(0.01)
        t = time.monotonic() - timer

    audio.deinit()
    deinit_trellis.deinit(trellis)
    __import__('start').main()


if __name__ == '__main__':
    main()