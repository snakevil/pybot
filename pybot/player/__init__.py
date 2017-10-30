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

    def __str__(self):
        return '%d,%d' % (self.x, self.y)

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

class Rect(object):
    def __init__(self, top_left, bottom_right = None):
        left = top = right = bottom = 0
        try:
            if not bottom_right:
                bottom_right = top_left[1]
                top_left = top_left[0]
            left = top_left[0]
            top = top_left[1]
            right = bottom_right[0]
            bottom = bottom_right[1]
        except: pass
        self.left = min(left, right)
        self.right = max(left, right)
        self.top = min(top, bottom)
        self.bottom = max(top, bottom)
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    def __str__(self):
        return '%d,%d ~ %d,%d' % (self.left, self.top, self.right, self.bottom)

    def __eq__(self, another):
        top = right = bottom = left = -1
        another_type = type(another)
        try:
            if another_type == tuple or another_type == list:
                left = another[0][0]
                top = another[0][1]
                right = another[1][0]
                bottom = another[1][1]
            else:
                left = another.left
                top = another.top
                right = another.right
                bottom = another.bottom
        except: pass
        return self.left == left and \
            self.top == top and \
            self.right == right and \
            self.bottom == bottom

    def center(self):
        return Point(
            self.left + int(self.width / 2),
            self.top + int(self.height / 2)
        )

    def random(self, padding = 0):
        return Point(
            random.randint(self.left + padding, self.right - padding),
            random.randint(self.top + padding, self.bottom - padding)
        )
