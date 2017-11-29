# encoding: utf-8

from ... import player
from .expect import Expect
from .ehistogram import EHistogram
from .ethreshold import EThreshold

class Colors(Expect):
    def __init__(self, region, histogram, threshold = 10, **spots):
        if not isinstance(histogram, tuple) or 8 != len(histogram):
            raise EHistogram(histogram)
        if not isinstance(threshold, int) or 0 > threshold:
            raise EThreshold(threshold)
        super(Colors, self).__init__(**spots)
        self._region = region if isinstance(region, player.Rect) \
            else player.Rect(*region)
        self._histogram = histogram
        self._threshold = threshold

    def __repr__(self):
        return 'Colors(%r, %r%s)' % (
            self._region,
            self._histogram,
            '' if 10 == self._threshold \
                else ', %d' % self._threshold
        )

    def test(self, event):
        if not event.screen:
            return False
        histo = event.screen.crop(
            (self._region.left, self._region.top),
            (self._region.right, self._region.bottom)
        ).histogram(1)
        distance = self._measure(self._histogram, histo)
        return distance <= self._threshold

    def _measure(self, a, b):
        distance = 0
        for ai, bi in zip(a, b):
            distance += (ai - bi) ** 2
        return 100 * distance ** .5 / (
            self._region.width * self._region.height
        )
