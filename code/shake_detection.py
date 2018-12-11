import math
import time
import random
import busio
import adafruit_adxl34x
import board
import adafruit_trellism4

# https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/master/NeoTrellisM4_Dice/code.py

trellis = adafruit_trellism4.TrellisM4Express()

i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

previous_reading = [None, None, None]
time_interval = 0.05
bound = 40.0 * time_interval

progress = -1

def randomize(x):
   print("Reset colors")
   for y in range(4):
        c = tuple(random.randint(0, 1) * 100 for _ in range(3))
        if (0 <= x + 1 < 8):
            print(x + 1, y)
            trellis.pixels[x + 1, y] = (0,0,0)
        if (0 <= x < 8):
            print(x, y)
            trellis.pixels[x, y] = c

def shaken():
   """Detect when the Trellis is shaken.
   See http://www.profoundlogic.com/docs/display/PUI/Accelerometer+Test+for+Shaking
   TL;DR one or more axis experiences a significant (set by bound) change very quickly
   Returns whether a shake was detected.
   """
   global previous_reading
   result = False
   x, y, z = accelerometer.acceleration
   if previous_reading[0] is not None:
       result = (math.fabs(previous_reading[0] - x) > bound and
                 math.fabs(previous_reading[1] - y) > bound and
                 math.fabs(previous_reading[2] - z) > bound)
   previous_reading = (x, y, z)
   return result

for i in range(8):
    randomize(i)

while True:
    shook = shaken()
    if (progress > -1):
        print("progress is", progress)
        randomize(progress)
        progress += 1
        if (progress >= 8):
            progress = -1
    else:
        if shook:
            progress = 0
    time.sleep(time_interval)
