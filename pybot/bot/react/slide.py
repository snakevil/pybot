# encoding: utf-8

from ... import player
from .react import React
from .espread import ESpread
from .eregion import ERegion

class Slide(React):
    """docstring for Slide"""
    def __init__(self, point, vector, spread = 0):
        super(Slide, self).__init__(1)
        if not isinstance(point, tuple):
            raise ERegion(point)
        if isinstance(point[0], tuple):
            self._target = player.Rect(point)
        else:
            self._target = player.Point(point)
        if not isinstance(vector, tuple) or isinstance(vector[0], tuple):
            raise ERegion(vector)
        self._vector = player.Point(vector)
        if not isinstance(spread, int) or 0 > spread:
            raise ESpread(spread)
        self._spread = spread

    def __repr__(self):
        return 'Slide(%r, %r%s)' % (
            self._target,
            self._vector,
            '' if not self._spread else ', %d' % self._spread
        )

    def do(self, event, trace):
        if isinstance(self._target, player.Rect):
            if self._spread:
                point = self._target.random(self._spread)
            else:
                point = self._target.center
        elif self._spread:
            point = self._target.spread(self._spread)
        else:
            point = self._target
        point2 = player.Point(
            point.x + self._vector.x,
            point.y + self._vector.y
        )
        trace.append('= %r -> %r' % (point, point2))
        event.drag(point, point2)
