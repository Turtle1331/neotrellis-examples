import time
import array
import math
import os
import board
import audioio
import adafruit_trellism4

SRC_FOLDER = 'sounds/drums/'
sounds = {
    (0, 0): 'kick.wav',
    (1, 0): 'snare.wav',
    (2, 0): 'hihat_l.wav',
    (3, 0): 'hihat_s.wav',
    (0, 1): 'coin.wav',
    (1, 1): 'bass_wha_c.wav',
    (2, 1): 'blip_c.wav',
    (3, 1): 'clap.wav',
}

colors = {
    (0, 0): (100, 0, 0),
    (1, 0): (100, 100, 0),
    (2, 0): (0, 75, 50),
    (3, 0): (0, 0, 125),
    (0, 1): (100, 25, 0),
    (1, 1): (100, 0, 100),
    (2, 1): (50, 50, 50),
    (3, 1): (0, 100, 0),
}

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.auto_write = False
audio = audioio.AudioOut(board.A1, right_channel=board.A0)


def play_wav(fname, async=False):
    try:
        length = os.stat(fname)[6]
        f = open(fname, "rb")
        wav = audioio.WaveFile(f)
        duration = length / (wav.sample_rate * wav.channel_count * wav.bits_per_sample / 8)
        audio.play(wav)
        if async:
            return duration
        while audio.playing:
            time.sleep(0.01)
        audio.stop()
    except OSError:
        print('could not find ' + fname)


def play_sin():
    channels = 2
    length = 8000 // 400
    sine_wave = array.array("H", [0] * channels * length)
    for i in range(length):
        for j in range(channels):
            sine_wave[i * channels + j] = int(math.sin(math.pi * 2 * i / length) * (2 ** 13) + 2 ** 15)
    
    sample = audioio.RawSample(sine_wave, channel_count=2, sample_rate=8000)
    audio.play(sample, loop=True)
    time.sleep(1)
    audio.stop()

def draw_all():
    trellis.pixels.fill((0,0,0))
    for pos, col in colors.items():
        trellis.pixels[2 * pos[0], 2 * pos[1]] = col
        trellis.pixels[2 * pos[0] + 1, 2 * pos[1]] = col
        trellis.pixels[2 * pos[0], 2 * pos[1] + 1] = col
        trellis.pixels[2 * pos[0] + 1, 2 * pos[1] + 1] = col
    trellis.pixels.show()



#play_wav('/startrek/01.wav')
#play_sin()
duration = None
position = None
timer = None
playing = True
curr = set()
available = set(sounds.keys())
while True:
    prev = curr
    curr = set(trellis.pressed_keys)
    for btn in (curr - prev):
        btn = (btn[0] // 2, btn[1] // 2)
        if btn not in available:
            continue
        if audio.playing:
            audio.stop()
        trellis.pixels.fill((0,0,0))
        trellis.pixels[2 * btn[0], 2 * btn[1]] = colors[btn]
        trellis.pixels[2 * btn[0] + 1, 2 * btn[1]] = colors[btn]
        trellis.pixels[2 * btn[0], 2 * btn[1] + 1] = colors[btn]
        trellis.pixels[2 * btn[0] + 1, 2 * btn[1] + 1] = colors[btn]
        trellis.pixels.show()
        position = btn
        duration = play_wav(SRC_FOLDER + sounds[btn], async=True)
        timer = time.monotonic()
        break
    
    audio.playing  # This is needed to get the audio module to update playing status
    if (playing and not audio.playing):
        draw_all()
    
    if audio.playing:
        t = (time.monotonic() - timer) / duration
        #'height', 'show', 'width', 'fill', 'auto_write', 'brightness', '_neopixel', '_rotation', '_width', '_height'
        for i in range(8):
            for j in range(4):
                b = (int (t * 8) - 1.5 <= abs(2 * position[0] + 0.5 - i) / 2 + abs(2 * position[1] + 0.5 - j) / 2 <= int(t * 8) + 0.5)
                trellis.pixels[i, j] = b and colors[position] or (0, 0, 0)
        trellis.pixels[2 * btn[0], 2 * btn[1]] = colors[btn]
        trellis.pixels[2 * btn[0] + 1, 2 * btn[1]] = colors[btn]
        trellis.pixels[2 * btn[0], 2 * btn[1] + 1] = colors[btn]
        trellis.pixels[2 * btn[0] + 1, 2 * btn[1] + 1] = colors[btn]
        trellis.pixels.show()
    
    #print(playing, audio.playing, playing and not audio.playing)
    playing = audio.playing
    #time.sleep(0.01)
    
