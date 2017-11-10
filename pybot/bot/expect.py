# encoding: utf-8

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
                self.log('%s in D%.2f' % (pixel, distance))
        return 1 > dismatched

class Otsu(Base):
    def __init__(self, region, otsu, gray = 0, threshold = 10):
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
        super(Otsu, self).test(player, context)
        otsu = player.snap().crop(
            (self.region.left, self.region.top),
            (self.region.right, self.region.bottom)
        ).resize(8, 8).grayscale().otsu(self.gray)
        distance = self._measure(self.otsu, otsu)
        if distance > self.threshold:
            self.log('%s in D%.2f' % (self.region, distance))
            return False
        return True

    def _measure(self, a, b):
        a_len = len(a)
        b_len = len(b)
        distance = 4 * abs(a_len - b_len)
        for i in range(min(a_len, b_len)):
            if a[i] != b[i]:
                a_bin = bin(int(a[i], 16))[2:].zfill(4)
                b_bin = bin(int(b[i], 16))[2:].zfill(4)
                for j in range(4):
                    if a_bin[j] != b_bin[j]:
                        distance += 1
        return 25 * distance / max(a_len, b_len)


__all__ = [
    'All', 'Any',
    'Until',
    'Pixels', 'Otsu'
]
