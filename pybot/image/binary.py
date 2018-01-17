# encoding: utf-8

import struct
import base64

from .base import Base
from ._codec import PNG

class Binary(Base):
    def __init__(self, size, raw, threshold = 0):
        super(Binary, self).__init__(size, raw)
        self.threshold = threshold
        self._projectX = None
        self._projectY = None
        self._digest = ''

    def __str__(self):
        width = 64
        blob = b''.join([
            struct.pack('>2HB', self.width, self.height, self.threshold),
            bytes.fromhex(self.digest)
        ])
        clob = base64.b64encode(blob).decode('utf-8')
        return '\n'.join(
            clob[i:i + width] for i in range(0, len(clob), width)
        )

    def _png(self):
        png = PNG(self.width, self.height, type = PNG.GREYSCALE_ALPHA)
        return png.encode(self.raw)

    def crop(self, top_left, bottom_right):
        cropped = super().crop(top_left, bottom_right)
        cropped.threshold = self.threshold
        return cropped

    def resize(self, width, height):
        resized = super().resize(width, height)
        resized.threshold = self.threshold
        return resized

    @classmethod
    def parse(cls, template):
        clob = template.strip().replace('\n', '')
        blob = base64.b64decode(clob.encode('utf-8'))
        width, height, threshold = struct.unpack('>2HB', blob[0:5])
        length = width * height * 4
        raw = bytearray(length)
        bize = range(8)
        for i in range(5, len(blob)):
            j = (i - 5) << 5
            bits = bin(blob[i])[2:].zfill(8)
            for k in bize:
                l = k << 2
                if j + l < length:
                    raw[j + l] = 255 if int(bits[k]) else 0
        return cls((width, height), raw, threshold)

    @staticmethod
    def otsu(raw):
        ''' http://www.isnowfy.com/similar-image-search/
            http://www.ruanyifeng.com/blog/2013/03/similar_image_search_part_ii.html

            len(grayb) / len(grays) * \
            len(grayf) / len(grays) * \
            pow(sum(grayb) / len(grayb) - sum(grayf) / len(grayf), 2)

            len(grayb) * \
            len(grayf) * \
            pow(sum(grayb) * len(grayf) - sum(grayf) * len(grayb), 2)
        '''
        threshold = 0
        grays = bytearray(raw[0::4])
        peak = 0
        for choice in range(1 + min(grays), max(grays)):
            grayf = []
            grayb = []
            for gray in grays:
                if gray < choice:
                    grayb.append(gray)
                else:
                    grayf.append(gray)
            grayf_len = len(grayf)
            grayb_len = len(grayb)
            value = grayf_len * grayb_len * (
                sum(grayb) * grayf_len - sum(grayf) * grayb_len
            ) ** 2
            if value > peak:
                peak = value
                threshold = choice
        return threshold

    @property
    def digest(self):
        if not self._digest:
            length = self.width * self.height
            size = length + 7 >> 3
            bits = bytearray(size << 3)
            bits[0:length] = self.raw[0::4]
            alob = bytearray(size)
            for cursor in range(size):
                index = cursor << 3
                alob[cursor] = ((bits[index] & 1) << 7) \
                    + ((bits[index + 1] & 1) << 6) \
                    + ((bits[index + 2] & 1) << 5) \
                    + ((bits[index + 3] & 1) << 4) \
                    + ((bits[index + 4] & 1) << 3) \
                    + ((bits[index + 5] & 1) << 2) \
                    + ((bits[index + 6] & 1) << 1) \
                    + (bits[index + 7] & 1)
            self._digest = bytes(alob).hex()
        return self._digest
