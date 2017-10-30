# encoding: utf-8

import random
import math
import platform
import time
from .. import image

system = platform.system()
if 'Windows' == system:
    from ._decorate import win32 as _decorate
elif 'Darwin' == system:
    from ._decorate import macos as _decorate
else:
    from ._decorate import linux as _decorate

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

class Window(object):
    def __init__(self, handle):
        self._handle = handle
        self.pid = _decorate.get_pid(handle)

    @classmethod
    def first(cls, pattern):
        handles = _decorate.query(pattern)
        if 0 < len(handles):
            return cls(handles[0])

    @classmethod
    def all(cls, pattern):
        return [cls(handle) for handle in _decorate.query(pattern)]

    def idle(self, msecs):
        time.sleep(msecs / 1000)
        return self

    @property
    def minimized(self):
        return _decorate.is_minimized(self._handle)

    def minimize(self):
        if self.minimized:
            return self
        _decorate.minimize(self._handle)
        return self.idle(10)

    def restore(self):
        if not self.minimized:
            return self
        _decorate.restore(self._handle)
        return self.idle(10)

    def focus(self):
        self.restore()
        _decorate.foreground(self._handle)
        return self

    @property
    def window(self):
        self.restore()
        return Rect(*_decorate.get_rect(self._handle))

    @property
    def width(self):
        self.restore()
        return _decorate.get_size(self._handle)[0]

    @property
    def height(self):
        self.restore()
        return _decorate.get_size(self._handle)[1]

    def click(self, point):
        _decorate.click(self._handle, point.x, point.y)
        return self.idle(90)

    def screen(self):
        return image.Screenshot(_decorate.grab(self._handle), self)

__all__ = ['Point', 'Window']
