# encoding: utf-8

from ...player import Rect
from .expect import Expect

class Colors(Expect):
    def __init__(self, region, histogram, threshold = 10):
        assert isinstance(histogram, tuple) \
            and isinstance(histogram[0], tuple) \
            and isinstance(histogram[0][0], tuple)
        assert isinstance(threshold, int) and 0 <= threshold
        self._region = region if isinstance(region, Rect) \
            else Rect(*region)
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
        a_flat = [k for i in a for j in i for k in j]
        b_flat = [k for i in b for j in i for k in j]
        distance = 0
        for ai, bi in zip(a_flat, b_flat):
            distance += (ai - bi) ** 2
        return 100 * distance ** .5 / (
            self._region.width * self._region.height
        )
