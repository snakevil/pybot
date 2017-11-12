# encoding: utf-8

from ...image import Pixel
from .expect import Expect

class Pixels(Expect):
    def __init__(self, *pixels, **params):
        assert 0 < len(pixels)
        super(Pixels, self).__init__()
        threshold = params.get('threshold') or 10
        if isinstance(pixels[-1], int):
            threshold = pixels[-1]
            del pixels[-1]
        assert isinstance(threshold, int) and 0 <= threshold
        self.pixels = [
            pixel if isinstance(pixel, Pixel) \
                else Pixel(*pixel) \
                for pixel in pixels
        ]
        self.threshold = threshold

    def test(self, player, context = {}):
        super(Pixels, self).test(player, context)
        image = player.snap()
        if not image:
            return False
        dismatched = 0
        for expected in self.pixels:
            pixel = image.pixel(expected.x, expected.y)
            distance = pixel - expected
            if self.threshold < distance:
                dismatched += 1
                self.log('%s in D%.2f' % (pixel, distance))
        return 1 > dismatched
