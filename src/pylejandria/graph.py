import pygame, argparse
from pylejandria.tools import pretty_dict

parser = argparse.ArgumentParser()
parser.add_argument('--width', type=int, required=False, default=1920)
parser.add_argument('--height', type=int, required=False, default=1080)
args = parser.parse_args()

pygame.init()
SCREEN = pygame.display.set_mode((args.width, args.height))
WIDTH, HEIGHT = SCREEN.get_size()
RUNNING = True

def lerp(a, b, c):
    if c <= 0: return lerp(a, b, -c)[::-1]
    return [a + (b - a) * t/c for t in range(c+1)]

def draw_text(surface, font, text, color, x, y, orientation='center', bg=None):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(**{orientation:(x, y)})
    if bg is not None:
        pygame.draw.rect(surface, bg, rect)
    surface.blit(rendered, rect)

DEFAULT_GRAPH_CONFIG = {
    'minx': -20,
    'maxx': 20,
    'miny': -20,
    'maxy': 20,
    'square': True
}

class GraphException(Exception):
    pass

class Graph:
    def __init__(self, master, **kwargs):
        if not kwargs: self.config = DEFAULT_GRAPH_CONFIG
        else: self.config = kwargs
        self.master = master

        self.maxx, self.minx = self.config.get('maxx'), self.config.get('minx')
        self.maxy, self.miny = self.config.get('maxy'), self.config.get('miny')
        self.x_width = self.maxx - self.minx
        self.y_width = self.maxy - self.miny
        self.width = self.config.get('width', self.master.get_size()[0])
        self.height = self.config.get('height', self.master.get_size()[1])
        if self.config.get('square', False):
            self.width = self.height = min(self.width, self.height)
        self.x_range = lerp(self.minx, self.maxx, self.x_width)
        self.y_range = lerp(self.miny, self.maxy, -self.y_width)
        try: self.x_center = self.x_range.index(0)
        except IndexError: self.x_center = -self.minx
        try: self.y_center = self.y_range.index(0)
        except IndexError: self.y_center = -self.miny
        self.cell_width = self.width / self.x_width
        self.cell_height = self.height / self.y_width
        self.x_line = self.x_center * self.cell_width
        self.y_line = self.y_center * self.cell_height

        self.surface = pygame.Surface((self.width, self.height))
        rect_config = {
                self.config.get('anchor', 'center'): (
                    self.config.get('x', self.width/2),
                    self.config.get('y', self.height/2)
                )
            }
        self.rect = self.surface.get_rect(**rect_config)

        self.font = pygame.font.SysFont(
            self.config.get('font', 'Robotica'),
            self.config.get('font_size', 16)
        )
        self.font_color = self.config.get('font_color', 'white')
        self.background = self.config.get('bg', 'black')
        self.axis_color = self.config.get('axis', '#505050')
        self.stroke_color = self.config.get('stroke', "#323232")
        self.stroke_weight = self.config.get('weight', 1)

        self.render()
    
    def draw_line(self, i, x, y):
        pygame.draw.line(
            self.surface,
            self.stroke_color if i != 0 else self.axis_color,
            (x[0], y[0]),
            (x[1], y[1]),
            self.stroke_weight if i != 0 else self.stroke_weight * 2
        )
    
    def draw_line_text(self, i, x, y, orientation):
        if i == 0: return
        draw_text(
            self.surface, self.font, str(i), 
            self.config.get('font_color', 'white'),
            x, y,
            orientation, self.background
        )
    
    def render(self):
        self.surface.fill(self.background)
        for i in self.x_range:
            x = (i + self.x_center) * self.cell_width
            self.draw_line(i, (x, x), (0, self.height))
            self.draw_line_text(i, x, self.y_line, 'topright')
        for i in self.y_range:
            y = (self.y_center - i) * self.cell_height
            self.draw_line(i, (0, self.width), (y, y))
            self.draw_line_text(i, self.x_line, y, 'bottomleft')

    def show(self):
        self.master.blit(self.surface, self.rect)

    def __repr__(self):
        return pretty_dict(self.config, _print=False)

graph = Graph(SCREEN)

while RUNNING:
    SCREEN.fill('black')
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: RUNNING = False
    
    graph.show()
    
    pygame.display.update()