# encoding: utf-8

from .base import Base
from .greyscale import Greyscale
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
            assert False
        png = PNG.decode(blob)
        return cls((png.width, png.height), png.data)

    def grayscale(self, bit = 8):
        return Greyscale(self, self.rgba, bit)
