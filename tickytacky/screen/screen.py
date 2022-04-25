import pyglet
from pyglet import shapes


class Screen(pyglet.window.Window):
    def __init__(self, width=240, height=160,
                 factor=6, title="NoName", fixed=False):
        super().__init__(width*factor, height*factor, title)
        self.time = 0
        self.batch = pyglet.graphics.Batch()
        self.height = height
        self.width = width
        self.factor = factor
        self.title = title
        self.pixel = []
        self.background = pyglet.graphics.OrderedGroup(0)
        self.sprites = [pyglet.graphics.OrderedGroup(1),
                        pyglet.graphics.OrderedGroup(2),
                        pyglet.graphics.OrderedGroup(3),
                        pyglet.graphics.OrderedGroup(4)]

        if fixed:
            super().set_maximum_size(width*factor, height*factor)
            super().set_minimum_size(width*factor, height*factor)

    def pixel_system(self, x, y):
        _width = self.width - 1
        _height = self.height - 1
        _x = x * self.factor
        _y = ((y*-1 + 159) * self.factor)
        f = self.factor
        return [(_width * f) - _width * f + _x,
                (_height * f) - _height * f + _y]

    def set_pixel(self, pixel, color, group=None):
        if not group:
            group = self.background
        pixel = self.pixel_system(pixel[0], pixel[1])
        if not color:
            return None
        else:
            self.pixel.append(shapes.Rectangle(
                              pixel[0],
                              pixel[1],
                              self.factor, self.factor,
                              color=color, batch=self.batch,
                              group=group))

    def add_sprite(self, data, group):
        palette = data.get("palette")
        shape = data.get("shape", [])
        location = data.get("location", [])
        for r in range(0, len(shape)):
            for c in range(0, len(shape[r])):
                self.set_pixel(pixel=(location[0] + c, location[1] + r),
                               color=palette.get(shape[r][c]),
                               group=self.sprites[group])

    def update(self, delta_time):
        self.time += delta_time
        self.clear()
        self.batch.draw()

    def on_draw(self):
        """Clear the screen and draw shapes"""
        self.clear()
        self.batch.draw()