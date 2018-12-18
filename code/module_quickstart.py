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
    btns = buttons.Buttons(trellis)
    
    config = {}
    try:
        with open('quickstart_config.csv', 'r') as f:
            lines = f.readlines()
        
        
        for line in lines:
            if len(line) <= 4:
                continue
            x, y, mod = line[0], line[2], line[4:]
            
            if not x.isdigit() or not y.isdigit():
                continue
            x = max(0, min(7, int(x)))
            y = max(0, min(3, int(y)))
            
            mod = ''.join(list(filter(str.isalpha, mod)))
            if (len(mod) == 0):
                continue
            
            config[(x, y)] = mod
    except OSError:
        with open('quickstart_config.csv', 'w') as f:
            pass
    
    if (len(config) == 0):
        config[(0, 0)] = 'module_list'
    
    
    for p, mod in config.items():
        random.seed(hash(mod))
        c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        print(p, c)
        trellis.pixels[p] = c
    trellis.pixels.show()
    
    available = set(config.keys())
    s = frozenset()
    while len(s) == 0:
        btns.update()
        s = btns.pressed() & available
        time.sleep(0.01)
    
    trellis.pixels.auto_write = True
    deinit_trellis.deinit(trellis)
    p = s.pop()
    
    mod = config[p]
    print('import ' + mod)
    mod = __import__(mod)
    if 'main' in dir(mod):
        print(mod.__name__ + '.main')
        mod.main()


if __name__ == '__main__':
    main()