import pyglet
from pyglet.window import Window
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(1400, 600, "Bubble sort") 
        self.batch = Batch()
        self.n = random.sample(range(1, 101), 100) 
        self.bars = self.create_bars()
        self.sort_generator = self.bubble_sort_animation()
        self.sort_complete = False  
        self.deltatime = 0.005

    def create_bars(self):
        bars = []
        bar_width = 5 # Set the width for each bar
        bar_spacing = 2  # Set the spacing for each bar
        for i, value in enumerate(self.n):
            bar_height = value * 3  
            bar_color = (255, 255, 255, 255) # White color for initial bars
            bar = Rectangle(i * (bar_width + bar_spacing), 0, bar_width, bar_height, color=bar_color, batch=self.batch)
            bars.append(bar)
        return bars

    def bubble_sort_animation(self):
        n = len(self.n)
        for i in range(n-1):
            for j in range(0, n-i-1):
                yield i, j

                if self.n[j] > self.n[j+1]:
                    self.n[j], self.n[j+1] = self.n[j+1], self.n[j]
        self.sort_complete = True 

    def on_update(self, dt):
        try:
            i, j = next(self.sort_generator)
            self.update_bars_positions(i, j)
        except StopIteration:
            if self.sort_complete:
                self.change_bars_color((0, 255, 0, 255)) # Change bars to green
            return

        clock.schedule_once(lambda dt: self.on_update(dt), self.deltatime)

    def update_bars_positions(self, current_i, current_j):
        for i, bar in enumerate(self.bars):
            if i == current_j or i == current_j + 1:
                bar.color = (255, 0, 0, 255)  # Use different shades of red for sorting bars
            else:
                bar.color = (255, 255, 255, 255) # Non-sorting bars will be in white color 
            bar.height = self.n[i] * 3  

    def change_bars_color(self, color):
        for bar in self.bars:
            bar.color = color

    def on_draw(self):
        self.clear()
        self.batch.draw()

# Create an instance of the Renderer class and run the Pyglet application
renderer = Renderer()
pyglet.clock.schedule_once(renderer.on_update, 1.0)
pyglet.app.run()
