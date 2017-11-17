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

    def test(self, player, context):
        image = player.snap()
        if not image:
            return False
        for expected in self.pixels:
            pixel = image.pixel(expected.x, expected.y)
            if self.threshold < pixel - expected:
                return False
        return True