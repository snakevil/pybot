# encoding: utf-8

import struct
import base64

from .base import Base
from .binary import Binary
from ._codec import PNG
from ._codec.edepth import EDepth

class Greyscale(Base):
    def __init__(self, size, raw, depth = 8):
        super(Greyscale, self).__init__(size, raw)
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

    def dump(self):
        width = 64
        blob = b''.join([
            struct.pack('>2H', self.width, self.height),
            self.rgba[0::4]
        ])
        clob = base64.b64encode(blob).decode('utf-8')
        return '\n'.join(
            clob[i:i + width] for i in range(0, len(clob), width)
        )

    @classmethod
    def parse(cls, template):
        clob = template.strip().replace('\n', '')
        blob = base64.b64decode(clob.encode('utf-8'))
        width, height = struct.unpack('>2H', blob[0:4])
        length = width * height * 4
        raw = bytearray(length)
        raw[0::4] = blob[4:]
        raw[1::4] = blob[4:]
        raw[2::4] = blob[4:]
        return cls((width, height), raw)
