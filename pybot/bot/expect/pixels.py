# encoding: utf-8

from ... import image
from .expect import Expect
from .epixels import EPixels
from .ethreshold import EThreshold

class Pixels(Expect):
    def __init__(self, *pixels, **spots):
        if not len(pixels):
            raise EPixels()
        threshold = spots.get('threshold') or 10
        del spots['threshold']
        if isinstance(pixels[-1], int):
            threshold = pixels[-1]
            del pixels[-1]
        if not isinstance(threshold, int) or 0 > threshold:
            raise EThreshold(threshold)
        super(Pixels, self).__init__(**spots)
        self._pixels = [
            pixel if isinstance(pixel, image.Pixel) \
                else image.Pixel(*pixel) \
                for pixel in pixels
        ]
        self._threshold = threshold

    def __repr__(self):
        return 'Pixels(%s%s)' % (
            repr(self._pixels)[1:-1],
            '' if 10 == self._threshold \
                else ', %d' % self._threshold
        )

    def _test(self, event):
        if not event.screen:
            return False
        for expected in self._pixels:
            pixel = event.screen.pixel(expected.x, expected.y)
            if self._threshold < pixel - expected:
                return False
        return True
