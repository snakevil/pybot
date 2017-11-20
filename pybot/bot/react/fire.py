# encoding: utf-8

from ...player import Point, Rect
from .react import React

class Fire(React):
    def __init__(self, point, spread = 0):
        super(Fire, self).__init__(1)
        if isinstance(point, tuple):
            if isinstance(point[0], tuple):
                self._target = Rect(point)
            elif isinstance(spread, tuple):
                self._target = Rect(point, spread)
                spread = 0
            else:
                self._target = Point(point)
        else:
            self._target = Point(point, spread)
            spread = 0
        assert isinstance(spread, int) and 0 <= spread
        self._spread = spread

    def do(self, event):
        if isinstance(self._target, Rect):
            if self._spread:
                point = self._target.random(self._spread)
            else:
                point = self._target.center
        elif self._spread:
            point = self._target.spread(self._spread)
        else:
            point = self._target
        event.click(point)
