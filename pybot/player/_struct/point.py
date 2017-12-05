# encoding: utf-8

import random
import math

class Point(object):
    def __init__(self, x, y = None):
        if type(x) == tuple:
            y = x[1]
            x = x[0]
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point(%d, %d)' % (self.x, self.y)

    def __eq__(self, another):
        x = y = -1
        another_type = type(another)
        if another_type == tuple or another_type == list:
            x = another[0]
            y = another[1]
        else:
            try:
                x = another.x
                x = another.y
            except: pass
        return self.x == x and self.y == y

    def spread(self, radius):
        degree = random.uniform(0, math.pi)
        radius = random.uniform(0, radius)
        return type(self)(
            int(round(self.x + radius * math.cos(degree))),
            int(round(self.y - radius * math.sin(degree)))
        )

    def skew(self, x, y):
        return type(self)(self.x + x, self.y + y)
