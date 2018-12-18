class Buttons:
    def __init__(self, trellis):
        self.trellis = trellis
        
        self.down_prev = frozenset()
        self.down_curr = frozenset()
        
        w, h = trellis.pixels.width, trellis.pixels.height
        self.all_btns = frozenset((i % w, i // w) for i in range(w * h))

    def update(self):
        self.down_prev = self.down_curr
        self.down_curr = frozenset(self.trellis.pressed_keys)

    def down(self):
        return self.down_curr

    def up(self):
        return self.all_btns - self.down_curr

    def pressed(self):
        return self.down_curr - self.down_prev

    def released(self):
        return self.down_prev - self.down_curr