# encoding: utf-8

from ... import player
from .react import React
from .espread import ESpread

class Fire(React):
    def __init__(self, point, spread = 0):
        super(Fire, self).__init__(1)
        if isinstance(point, tuple):
            if isinstance(point[0], tuple):
                self._target = player.Rect(point)
            elif isinstance(spread, tuple):
                self._target = player.Rect(point, spread)
                spread = 0
            else:
                self._target = player.Point(point)
        else:
            self._target = player.Point(point, spread)
            spread = 0
        if not isinstance(spread, int) or 0 > spread:
            raise ESpread(spread)
        self._spread = spread

    def __repr__(self):
        return 'Fire(%r%s)' % (
            self._target,
            '' if not self._spread else ', %d' % self._spread
        )

    def do(self, event):
        if isinstance(self._target, player.Rect):
            if self._spread:
                point = self._target.random(self._spread)
            else:
                point = self._target.center
        elif self._spread:
            point = self._target.spread(self._spread)
        else:
            point = self._target
        event.click(point)
