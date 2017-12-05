# encoding: utf-8

from .base import Base
from .binary import Binary
from ._codec import PNG
from ._codec.edepth import EDepth

class Greyscale(Base):
    def __init__(self, size, raw, depth = 8):
        ''' http://blog.csdn.net/u013467442/article/details/47616661
        '''
        if not isinstance(depth, int) or depth not in [1, 2, 4, 8]:
            raise EDepth(depth)
        rgba = bytearray(raw)
        bits = 8 - depth
        for cursor in range(0, len(rgba), 4):
            rgba[cursor] = (
                raw[cursor] + (raw[cursor + 1] << 1) + raw[cursor + 2]
            ) >> 2 + bits << bits
        rgba[1::4] = rgba[0::4]
        rgba[2::4] = rgba[0::4]
        super(Greyscale, self).__init__(size, rgba)
        self.depth = depth
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
