import os
import math
import time
import random
import adafruit_trellism4
import deinit_trellis
import buttons

def main():
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
        'N': 3983, # 3975,
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


    btns = buttons.Buttons(trellis)


    pixels_on = get_message('hi')
    for p in pixels_on:
        trellis.pixels[p] = on_col


    fnames = [fname[:-3] for fname in os.listdir('.') if not fname.startswith('.') and fname.endswith('.py') and fname != 'code.py']

    index = 0
    length = len(fnames[index]) * 4 - 4
    dots = get_message(fnames[index])
    scroll = 0

    while True:
        btns.update()
        
        p = (0, 0)
        for p in btns.pressed():
            if (p[0] == 0 or p[0] == 7):
                if (p[0] == 0 and scroll - 2 >= 0):
                    scroll -= 2
                elif (p[0] == 7 and scroll + 2 <= length):
                    scroll += 2
            elif (p[1] == 0 or p[1] == 3):
                if (p[1] == 0 and index > 0):
                    index -= 1
                elif (p[1] == 3 and index < len(fnames)):
                    index += 1
                length = len(fnames[index]) * 4 - 4
                dots = get_message(fnames[index])
                scroll = 0
            else:
                break
        if (0 < p[0] < 7 and 0 < p[1] < 3):
            break
        
        trellis.pixels.fill((0,0,0))
        for dot in dots:
            if (0 <= dot[0] - scroll < 8 and 0 <= dot[1] < 4):
                trellis.pixels[dot[0] - scroll, dot[1]] = on_col
        trellis.pixels.show()
        
        time.sleep(0.05)


    deinit_trellis.deinit(trellis)
    mod = fnames[index]
    print('import ' + mod)
    mod = __import__(mod)
    if 'main' in dir(mod):
        print(mod.__name__ + '.main')
        mod.main()


if __name__ == '__main__':
    main()