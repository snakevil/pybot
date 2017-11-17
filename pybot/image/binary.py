# encoding: utf-8

from .base import Base
from ._codec import PNG

class Binary(Base):
    def __init__(self, size, raw, threshold = 0):
        threshold = threshold or self.otsu(raw)
        length = len(raw)
        cursor = 0
        while cursor < length:
            raw[cursor] = 0 if raw[cursor] < threshold else 255
            cursor += 4
        raw[1::4] = raw[0::4]
        raw[2::4] = raw[0::4]
        super(Binary, self).__init__(size, raw)
        self._digest = ''

    def _png(self):
        png = PNG(self.width, self.height, type = PNG.GREYSCALE_ALPHA)
        return png.encode(self.rgba)

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
            bits[0:length] = self.rgba[0::4]
            alob = bytearray(size)
            index = 0
            cursor = 0
            while cursor < size:
                alob[cursor] = ((bits[index] & 1) << 7) \
                    + ((bits[index + 1] & 1) << 6) \
                    + ((bits[index + 2] & 1) << 5) \
                    + ((bits[index + 3] & 1) << 4) \
                    + ((bits[index + 4] & 1) << 3) \
                    + ((bits[index + 5] & 1) << 2) \
                    + ((bits[index + 6] & 1) << 1) \
                    + (bits[index + 7] & 1)
                index += 8
                cursor += 1
            self._digest = bytes(alob).hex()
        return self._digest
