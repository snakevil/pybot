# encoding: utf-8

from ...player import Point, Rect
from .action import Action

class Fire(Action):
    def __init__(self, point, spread = 0):
        super(Fire, self).__init__(1)
        if isinstance(point, tuple):
            if isinstance(point[0], tuple):
                self.target = Rect(point)
            elif isinstance(spread, tuple):
                self.target = Rect(point, spread)
                spread = 0
            else:
                self.target = Point(point)
        else:
            self.target = Point(point, spread)
            spread = 0
        assert isinstance(spread, int) and 0 <= spread
        self.spread = spread

    def do(self, event):
        if isinstance(self.target, Rect):
            if self.spread:
                point = self.target.random(self.spread)
            else:
                point = self.target.center
        elif self.spread:
            point = self.target.spread(self.spread)
        else:
            point = self.target
        event.click(point)
