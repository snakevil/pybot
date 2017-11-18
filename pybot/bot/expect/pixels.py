# encoding: utf-8

from ...image import Pixel
from .expect import Expect

class Pixels(Expect):
    def __init__(self, *pixels, **params):
        assert 0 < len(pixels)
        threshold = params.get('threshold') or 10
        if isinstance(pixels[-1], int):
            threshold = pixels[-1]
            del pixels[-1]
        assert isinstance(threshold, int) and 0 <= threshold
        super(Pixels, self).__init__(**spots)
        self._pixels = [
            pixel if isinstance(pixel, Pixel) \
                else Pixel(*pixel) \
                for pixel in pixels
        ]
        self._threshold = threshold

    def __repr__(self):
        return 'Pixels(%s%s)' % (
            repr(self._pixels)[1:-1],
            '' if 10 == self._threshold \
                else ', %d' % self._threshold
        )

    def test(self, event):
        if not event.screen:
            return False
        for expected in self._pixels:
            pixel = event.screen.pixel(expected.x, expected.y)
            if self._threshold < pixel - expected:
                return False
        return True
