from src.pylejandria.gui import FramelessWindow
import tkinter as tk
from inspect import signature
from threading import Thread
from pylejandria.tools import pair

class Plot(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.grid_mode = None
        self.scale = 20
        self.plots = []
        self.updating = False

        for key, value in kwargs.items():
            self[key] = value

        self.bind('<Configure>', self.update_canvas)
    
    def set_scale(self, value):
        self.scale = value
    
    def update_canvas(self, *e):
        if self.updating: return
        self.updating = True
        self.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.delete('all')

        if self.grid_mode[0] == '-':
            self.draw_line_grid(**self.grid_mode[1])
        elif self.grid_mode[0] == '+':
            self.draw_cross_grid(**self.grid_mode[1])
        elif isinstance(self.grid_mode[0], tuple):
            self.draw_line_grid(**(self.grid_mode[1] | {'dash': self.grid_mode[0]}))

        for data, kwargs in self.plots:
            if callable(data):
                parameters = len(signature(data).parameters)
                if parameters == 1:
                    thread = Thread(target=self.function, args=(data, ), kwargs=kwargs)
                    thread.start()
                elif parameters == 2:
                    thread = Thread(target=self.implicit, args=(data, ), kwargs=kwargs)
                    thread.start()
        
        self.updating = False
    
    def function(self, func, **kwargs):
        color = kwargs.get('color', '#00ffff')
        width = kwargs.get('width', 1)
        x_values = map(lambda x: (x - self.width//2) / self.scale, range(self.width))
        y_values = []
        for x_value in x_values:
            try: y_values.append(func(x_value))
            except ZeroDivisionError: y_values.append(0j)
        y_screen = map(lambda y: self.height//2 - y * self.scale, y_values)
        x_screen = range(self.width)
        points = list(zip(x_screen, y_screen))
        for (x1, y1), (x2, y2) in pair(points, 2):
            try: self.create_line(x1, y1, x2, y2, fill=color, width=width)
            except tk.TclError: continue
    
    def implicit(self, func, **kwargs):
        color = kwargs.get('color', '#00ffff')
        width = kwargs.get('width', 1)
        fill = kwargs.get('fill', None)
        alpha = kwargs.get('alpha', 0)
        state = False
        points = []

        for y in range(self.height):
            for x in range(self.width):
                x_value = (x - self.width//2) / self.scale
                y_value = (self.height//2 - y) / self.scale
                value = func(x_value, y_value)
                if alpha != 0 and len(points) == 2:
                    if y % int(2/alpha) == 0:
                        (x1, y1), (x2, y2) = points
                        self.create_line(x1, y1, x2, y2, fill=fill, width=1)
                    points = []
                if value not in (state, None):
                    state = not state
                    points.append((x, y))
                    self.create_oval(x - width//2, y - width//2, x + width//2, y + width//2, fill=color, outline=color)
    
    def set_grid(self, **kwargs):
        self.grid_mode = (kwargs.get('style', None), kwargs)

    def draw_cross(self, x, y, size=1, color='#404040', width=1):
        kwargs = {
            'fill': color,
            'width': width
        }
        self.create_line(x - size, y, x + size, y, **kwargs)
        self.create_line(x, y - size, x, y + size, **kwargs)
    
    def draw_cross_grid(self, **kwargs):
        color = kwargs.get('color', '#404040')
        size = kwargs.get('size', 1)
        width = kwargs.get('width', 1)
        axis = kwargs.get('axis', '#ffffff')
        axis_width = kwargs.get('axis_width', 3)
        for i in range(self.height//self.scale):
            y1 = self.height//2 - i * self.scale
            y2 = self.height//2 + i * self.scale
            for j in range(self.width//self.scale):
                x1 = self.width//2 - j * self.scale
                x2 = self.width//2 + j * self.scale
                self.draw_cross(x1, y1, size, color=color, width=width)
                self.draw_cross(x2, y1, size, color=color, width=width)
                self.draw_cross(x1, y2, size, color=color, width=width)
                self.draw_cross(x2, y2, size, color=color, width=width)

        self.create_line(self.width//2, 0, self.width//2, self.height, fill=axis, width=axis_width)
        self.create_line(0, self.height//2, self.width, self.height//2, fill=axis, width=axis_width)

    def draw_line_grid(self, **kwargs):
        color = kwargs.get('color', '#404040')
        width = kwargs.get('width', 1)
        axis = kwargs.get('axis', '#ffffff')
        axis_width = kwargs.get('axis_width', 3)
        dash = kwargs.get('dash', None)
        for i in range(self.width//self.scale):
            x1 = self.width // 2 - i * self.scale
            x2 = self.width // 2 + i * self.scale
            if dash is None:
                self.create_line(x1, 0, x1, self.height, fill=color, width=width)
                self.create_line(x2, 0, x2, self.height, fill=color, width=width)
            else:
                self.create_line(x1, 0, x1, self.height, fill=color, width=width, dash=dash)
                self.create_line(x2, 0, x2, self.height, fill=color, width=width, dash=dash)
        for i in range(self.height//self.scale):
            y1 = self.height // 2 - i * self.scale
            y2 = self.height // 2 + i * self.scale
            if dash is None:
                self.create_line(0, y1, self.width, y1, fill=color)
                self.create_line(0, y2, self.width, y2, fill=color)
            else:
                self.create_line(0, y1, self.width, y1, fill=color, dash=dash)
                self.create_line(0, y2, self.width, y2, fill=color, dash=dash)

        self.create_line(self.width//2, 0, self.width//2, self.height, fill=axis, width=axis_width)
        self.create_line(0, self.height//2, self.width, self.height//2, fill=axis, width=axis_width)

    def plot(self, value, color='#00ffff', width=1, fill=None, alpha=0):
        kwargs = {
            'color': color,
            'width': width,
            'fill': fill,
            'alpha': alpha
        }
        self.plots.append([value, kwargs])

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

window = FramelessWindow(title='TkSystem Plot', titlebg='#323232', fg='#ffffff', bg='#202020')
window.minsize(800, 500)
window.geometry('1200x800')

print(window.winfo_screenwidth(), window.winfo_screenheight())

plot = Plot(window, bg='#202030', bd=0)
plot.pack(expand=True, fill='both', padx=50, pady=50)

plot.set_scale(200)
plot.set_grid(style='-', axis='#808080', size=5)
plot.plot(lambda x, y: (x**2 + y**2-1)**3 - x**2*y**3 <= 0, width=1, color='#ff0080', fill='#400020', alpha=1)

window.mainloop()