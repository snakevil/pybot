# encoding: utf-8

from os import path

from .. import core
from .base import Base
from .greyscale import Greyscale
from .binary import Binary
from ._codec import PNG

class Image(Base):
    @classmethod
    def load(cls, filepath):
        rpos = filepath.rfind('.')
        if -1 < rpos:
            ext = filepath[rpos:]
        else:
            ext = '.png'
            filepath += ext
        blob = ''
        with open(filepath, 'rb') as hfile:
            blob = hfile.read()
        if '.png' != ext:
            raise core.ETodo('image.image.load.jpeg')
        png = PNG.decode(blob)
        image = cls((png.width, png.height), png.data)
        image.timestamp = path.getmtime(filepath)
        return image

    @staticmethod
    def binary(blob):
        return Binary.parse(blob)

    @staticmethod
    def greyscale(blob):
        return Greyscale.parse(blob)

    def grayscale(self, depth = 8):
        ''' http://blog.csdn.net/u013467442/article/details/47616661
        '''
        if not isinstance(depth, int) or depth not in [1, 2, 4, 8]:
            raise EDepth(depth)
        raw = bytearray(self.raw)
        length = len(self.raw)
        bits = 8 - depth
        for cursor in range(0, length, 4):
            raw[cursor] = (
                raw[cursor] + (raw[cursor + 1] << 1) + raw[cursor + 2]
            ) << bits >> 2 + bits
        raw[1::4] = raw[0::4]
        raw[2::4] = raw[0::4]
        raw[3::4] = [255] * (length >> 2)
        return Greyscale(self, raw, depth)
