# encoding: utf-8

from ...player import Rect
from .expect import Expect

class Colors(Expect):
    def __init__(self, region, histogram, threshold = 10):
        assert isinstance(histogram, tuple) \
            and isinstance(histogram[0], tuple) \
            and isinstance(histogram[0][0], tuple)
        assert isinstance(threshold, int) and 0 <= threshold
        self.region = region if isinstance(region, Rect) \
            else Rect(*region)
        self.histogram = histogram
        self.threshold = threshold

    def test(self, event):
        if not event.screen:
            return False
        histo = event.screen.crop(
            (self.region.left, self.region.top),
            (self.region.right, self.region.bottom)
        ).histogram(1)
        distance = self._measure(self.histogram, histo)
        return distance <= self.threshold

    def _measure(self, a, b):
        a_flat = [k for i in a for j in i for k in j]
        b_flat = [k for i in b for j in i for k in j]
        distance = 0
        for ai, bi in zip(a_flat, b_flat):
            distance += (ai - bi) ** 2
        return 100 * distance ** .5 / (self.region.width * self.region.height)
