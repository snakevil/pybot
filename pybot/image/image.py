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
    def template(blob):
        return Binary.parse(blob)

    def grayscale(self, depth = 8):
        return Greyscale(self, self.rgba, depth)
