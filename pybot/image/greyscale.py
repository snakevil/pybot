# encoding: utf-8

from .base import Base
from .binary import Binary
from ._codec import PNG

class Greyscale(Base):
    def __init__(self, size, raw, depth = 8):
        ''' http://blog.csdn.net/u013467442/article/details/47616661
        '''
        assert isinstance(depth, int) and 0 < depth and depth < 9
        super(Greyscale, self).__init__(size, raw)
        self.depth = depth
        length = self.width * self.height
        gray = bytearray(length)
        depth = 8 - depth
        cursor = 0
        while cursor < length:
            pos = cursor << 2
            gray[cursor] = (
                raw[pos] + (raw[pos + 1] << 1) + raw[pos + 2]
            ) >> 2 + depth << depth
            cursor += 1
        self.rgba[0::4] = gray[:]
        self.rgba[1::4] = gray[:]
        self.rgba[2::4] = gray[:]
        self._threshold = 0

    def _png(self):
        png = PNG(self.width, self.height, self.depth, PNG.GREYSCALE_ALPHA)
        return png.encode(self.rgba)

    @property
    def threshold(self):
        if not self._threshold:
            self._threshold = Binary.otsu(self.rgba)
        return self._threshold

    def binary(self, threshold = 0):
        return Binary(self, self.rgba, threshold or self.threshold)
        for pixel in self.rgba[0::4]:
            if pixel > gray:
                raw += [255, 255, 255, 0]
            else:
                raw += [0, 0, 0, 0]
        return type(self)(self, bytearray(raw))
