import pyglet
from pyglet.window import Window
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(1400, 600, "Merge sort")
        self.batch = Batch()
        self.n = [random.randint(1, 150) for _ in range(200)]
        self.bars = self.create_bars()
        self.sort_generator = self.merge_sort_animation(0, len(self.n) - 1)
        self.sort_complete = False
        self.deltatime = 0.005
        pyglet.clock.schedule_interval(self.update, self.deltatime)
        self.event_handler = pyglet.window.event.WindowEventLogger()
        self.push_handlers(self.event_handler)

    def create_bars(self):
        bars = []
        bar_width = 5
        bar_spacing = 2
        for i, value in enumerate(self.n):
            bar_height = value * 3
            bar_color = (255, 255, 255, 255)
            bar = Rectangle(i * (bar_width + bar_spacing), 0, bar_width, bar_height, color=bar_color, batch=self.batch)
            bars.append(bar)
        return bars

    def merge_sort_animation(self, l, r):
        if l < r:
            mid = (l + r) // 2
            yield from self.merge_sort_animation(l, mid)
            yield from self.merge_sort_animation(mid + 1, r)
            yield from self.merge_animation(l, mid, r)

    def merge_animation(self, l, mid, r):
        left = self.n[l:mid + 1]
        right = self.n[mid + 1:r + 1]

        i = j = 0
        k = l

        while i < len(left) and j < len(right):
            yield l + i, mid + 1 + j

            if left[i] <= right[j]:
                self.n[k] = left[i]
                i += 1
            else:
                self.n[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            self.n[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            self.n[k] = right[j]
            j += 1
            k += 1

        self.update_bars_positions()

    def update(self, dt):
        try:
            i, j = next(self.sort_generator)
            self.update_bars_positions(i, j)
        except StopIteration:
            if not self.sort_complete:
                self.change_bars_color((0, 255, 0, 255)) 
                self.sort_complete = True


    def update_bars_positions(self, current_i=None, current_j=None):
        for i, bar in enumerate(self.bars):
            if (current_i is not None and i == current_i) or (current_j is not None and i == current_j + 1):
                bar.color = (255, 0, 0, 255)  
            else:
                bar.color = (255, 255, 255, 255) 
            bar.height = self.n[i] * 3 

    def change_bars_color(self, color):
        for bar in self.bars:
            bar.color = color

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_close(self):
        print("Window closed")
        pyglet.app.exit()

renderer = Renderer()
pyglet.app.run()