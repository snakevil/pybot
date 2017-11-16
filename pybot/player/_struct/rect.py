# encoding: utf-8

import random
from .point import Point

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
        return 'Rect((%d, %d), (%d, %d))' % (self.left, self.top, self.right, self.bottom)

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

    @property
    def center(self):
        return Point(
            self.left + (self.width >> 1),
            self.top + (self.height >> 1)
        )

    def random(self, padding = 0):
        padding = int(padding)
        assert 0 <= padding and 2 * padding <= min(self.width, self.height)
        return Point(
            random.randint(self.left + padding, self.right - padding),
            random.randint(self.top + padding, self.bottom - padding)
        )
