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
        self._projectX = None
        self._projectY = None
        self._threshold = 0

    def __str__(self):
        width = 64
        blob = b''.join([
            struct.pack('>2H', self.width, self.height),
            self.raw[0::4]
        ])
        clob = base64.b64encode(blob).decode('utf-8')
        return '\n'.join(
            clob[i:i + width] for i in range(0, len(clob), width)
        )

    def _png(self):
        png = PNG(self.width, self.height, self.depth, PNG.GREYSCALE_ALPHA)
        return png.encode(self.raw)

    def crop(self, top_left, bottom_right):
        cropped = super().crop(top_left, bottom_right)
        cropped.depth = self.depth
        return cropped

    def resize(self, width, height):
        resized = super().resize(width, height)
        resized.depth = self.depth
        return resized

    @classmethod
    def parse(cls, clob):
        blob = base64.b64decode(clob.strip().replace('\n', '').encode('utf-8'))
        width, height = struct.unpack('>2H', blob[0:4])
        length = width * height
        raw = bytearray(length << 2)
        raw[0::4] = blob[4:]
        raw[1::4] = blob[4:]
        raw[2::4] = blob[4:]
        raw[3::4] = bytearray([255]) * length
        return cls((width, height), raw)

    @property
    def projectX(self):
        if not self._projectX:
            size = self.width << 2
            self._projectX = [
                sum(self.raw[x * 4::size]) \
                    for x in range(self.width)
            ]
        return self._projectX

    @property
    def projectY(self):
        if not self._projectY:
            size = self.width << 2
            self._projectY = [
                sum(self.raw[i:i + size:4]) \
                    for i in range(0, len(self.raw), size)
            ]
        return self._projectY

    @property
    def threshold(self):
        if not self._threshold:
            self._threshold = Binary.otsu(self.raw)
        return self._threshold

    def binary(self, threshold = 0):
        threshold = threshold or self.threshold
        length = len(self.raw)
        raw = bytearray(length)
        for cursor in range(0, length, 4):
            raw[cursor] = 0 if self.raw[cursor] < threshold else 255
        raw[1::4] = raw[0::4]
        raw[2::4] = raw[0::4]
        raw[3::4] = [255] * (length >> 2)
        return Binary(self, raw, threshold)
