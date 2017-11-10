# encoding: utf-8

import sys
from .. import image
from .. import player as window

class Base(object):
    def __init__(self):
        self.context = {}

    def log(self, message):
        message = '%s /%s/ %s' % (
            self.player,
            type(self).__name__,
            message
        )
        log = self.context.get('dbg')
        if hasattr(log, '__call__'):
            log(message)
        else:
            print >> sys.stderr, message

    def test(self, player, context = {}):
        assert isinstance(player, window.Window)
        self.player = player
        assert isinstance(context, dict)
        self.context = context
        return False

class All(Base):
    def __init__(self, *expects):
        super(All, self).__init__()
        self.expects = expects

    def test(self, player, context = {}):
        super(All, self).test(player, context)
        for expect in self.expects:
            if not expect.test(player, context):
                return False
        return True

class Any(Base):
    def __init__(self, *expects):
        super(Any, self).__init__()
        self.expects = expects

    def test(self, player, context = {}):
        super(Any, self).test(player, context)
        for expect in self.expects:
            if expect.test(player, context):
                return True
        return False

class Pixels(Base):
    def __init__(self, *pixels, **params):
        assert 0 < len(pixels)
        super(Pixels, self).__init__()
        threshold = params.get('threshold') or 10
        if isinstance(pixels[-1], int):
            threshold = pixels[-1]
            del pixels[-1]
        assert isinstance(threshold, int) and 0 <= threshold
        self.pixels = [
            pixel if isinstance(pixel, image.Pixel) \
                else image.Pixel(*pixel) \
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
                self.log('%s in D%.1f' % (pixel, distance))
        return 1 > dismatched

class Otsu(Base):
    def __init__(self, region, otsu, threshold = 0, gray = 0):
        assert isinstance(otsu, str)
        assert isinstance(threshold, int) and 0 <= threshold
        assert isinstance(gray, int) and 0 <= gray and gray < 255
        super(Otsu, self).__init__()
        self.region = region if isinstance(region, window.Rect) \
            else window.Rect(*region)
        self.otsu = otsu
        self.threshold = threshold
        self.gray = gray

    def test(self, player, context = {}):
        super(Otsu, self).apply(player, context)
        otsu = player.snap().crop(
            (self.region.left, self.region.top),
            (self.region.right, self.region.bottom)
        ).resize(8, 8).grayscale().otsu(self.gray)
        expected_bin = bin(int(self.otsu, 16))
        otsu_bin = bin(int(otsu, 16))
        expected_len = len(expected_bin)
        otsu_len = len(otsu_bin)
        distance = abs(expected_len - otsu_len)
        for i in range(2, min(expected_len, otsu_len)):
            if expected_bin[i] != otsu_bin[i]:
                distance += 1
        if 100 * distance > self.threshold * max(expected_len, otsu_len):
            self.log('D%d' % distance)
            return False
        return True

__all__ = [
    'All', 'Any',
    'Until',
    'Pixels', 'Otsu'
]
