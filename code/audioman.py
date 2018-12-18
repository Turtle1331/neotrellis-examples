import audioio

audio = audioio.AudioOut(board.A1, right_channel=board.A0)

def get_raw_obj():
    return audio

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
        return 0
    except OSError:
        return -1

def play_raw(data):
    duration = length / (wav.sample_rate * wav.channel_count * wav.bits_per_sample / 8)
    sample = audioio.RawSample(sine_wave, channel_count=2, sample_rate=8000)
    audio.play(sample, loop=True)
    time.sleep(1)
    audio.stop()