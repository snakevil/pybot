# encoding: utf-8

from .image import Image

class Screenshot(Image):
    def __init__(self, size, raw):
        length = len(raw)
        alob = bytearray(length)
        alob[0::4] = raw[2::4]
        alob[1::4] = raw[1::4]
        alob[2::4] = raw[0::4]
        alob[3::4] = [255] * (length >> 2)
        super(Screenshot, self).__init__(self, size, alob)
