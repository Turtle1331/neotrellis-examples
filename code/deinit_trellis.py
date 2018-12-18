'''
A simple utility to deinitialize the digital IO pins used by the trellis.
'''

def deinit(trs):
    trs.pixels.fill((0, 0, 0))
    trs.pixels.show()

    npxl = trs.pixels._neopixel
    mtrx = trs._matrix
    
    npxl.deinit()
    for pin in mtrx.row_pins:
        pin.deinit()
    for pin in mtrx.col_pins:
        pin.deinit()