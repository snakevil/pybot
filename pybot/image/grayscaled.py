# encoding: utf-8

from .base import Base

class Grayscaled(Base):
    def __init__(self, size, raw, bit = 8):
        ''' http://blog.csdn.net/u013467442/article/details/47616661
        '''
        assert isinstance(bit, int) and 0 < bit and bit < 9
        self.bit = bit
        bgrr = bytearray(len(raw))
        bit = 8 - bit
        for i in range(0, len(raw), 4):
            gray = (
                raw[2 + i] + (raw[1 + i] << 1) + raw[i]
            ) >> 2 + bit << bit
            bgrr[i] = bgrr[1 + i] = bgrr[2 + i] = gray
        super(Grayscaled, self).__init__(size, bgrr)

    @property
    def otsugray(self):
        ''' http://www.isnowfy.com/similar-image-search/
            http://www.ruanyifeng.com/blog/2013/03/similar_image_search_part_ii.html

            len(grayb) / len(grays) * \
            len(grayf) / len(grays) * \
            pow(sum(grayb) / len(grayb) - sum(grayf) / len(grayf), 2)

            len(grayb) * \
            len(grayf) * \
            pow(sum(grayb) * len(grayf) - sum(grayf) * len(grayb), 2)
        '''
        if not hasattr(self, '_otsugray'):
            self._otsugray = 0
            size = self.width * self.height
            grays = list(self.bgrr[0::4])
            ref = 0
            for guess in range(1 + min(grays), max(grays)):
                grayf = []
                grayb = []
                for gray in grays:
                    if gray < guess:
                        grayb.append(gray)
                    else:
                        grayf.append(gray)
                grayf_len = len(grayf)
                grayb_len = len(grayb)
                digest = grayf_len * grayb_len * (
                    sum(grayb) * grayf_len - sum(grayf) * grayb_len
                ) ** 2
                if digest > ref:
                    ref = digest
                    self._otsugray = guess
        return self._otsugray

    def otsu(self, gray = 0):
        if not gray:
            gray = self.otsugray
        buff = ''
        for pixel in self.bgrr[0::4]:
            buff += '1' if pixel > gray \
                else '0'
        pad = 4 - len(buff) % 4
        if 4 > pad:
            buff = '0' * pad + buff
        ret = ''
        for i in range(0, len(buff), 4):
            ret += hex(int(buff[i:4 + i], 2))[2]
        return ret

    def otsuscale(self, gray = 0):
        if not gray:
            gray = self.otsugray
        raw = []
        for pixel in self.bgrr[0::4]:
            if pixel > gray:
                raw += [255, 255, 255, 0]
            else:
                raw += [0, 0, 0, 0]
        return type(self)(self, bytearray(raw))
