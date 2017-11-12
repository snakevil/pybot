# encoding: utf-8

import struct
import zlib
from ._struct import Pixel

class Base(object):
    def __init__(self, size, raw):
        self.bgrr = raw
        size_type = type(size)
        if size_type == tuple or size_type == list:
            self.width = size[0]
            self.height = size[1]
        else:
            self.width = size.width
            self.height = size.height

    def pixel(self, x, y):
        assert 0 <= x and x < self.width
        assert 0 <= y and y < self.height
        pos = self.width * x + y
        return Pixel(
            (x, y),
            (self.bgrr[pos + 2], self.bgrr[pos + 1], self.bgrr[pos])
        )

    def save(self, filepath):
        rpos = filepath.rfind('.')
        if -1 < rpos:
            ext = filepath[rpos:]
        else:
            ext = '.png'
            filepath += ext
        if '.png' == ext:
            return self._2png(filepath)

    def _2png(self, filepath):
        rgb = bytearray(self.width * self.height * 3)
        rgb[0::3] = self.bgrr[2::4]
        rgb[1::3] = self.bgrr[1::4]
        rgb[2::3] = self.bgrr[0::4]
        rgb = bytes(rgb)
        width = 3 * self.width
        nul = struct.pack('>B', 0)
        scanlines = b''.join(
            [nul + rgb[y * width:(1 + y) * width] for y in range(self.height)]
        )
        ihdr = [
            b'',
            b'IHDR',
            struct.pack('>2I5B', self.width, self.height, 8, 2, 0, 0, 0),
            b''
        ]
        ihdr[3] = struct.pack(
            '>I',
            zlib.crc32(b''.join(ihdr[1:3])) & 0xffffffff
        )
        ihdr[0] = struct.pack('>I', len(ihdr[2]))
        idat = [
            b'',
            b'IDAT',
            zlib.compress(scanlines),
            b''
        ]
        idat[3] = struct.pack(
            '>I',
            zlib.crc32(b''.join(idat[1:3])) & 0xffffffff
        )
        idat[0] = struct.pack('>I', len(idat[2]))
        iend = [b'', b'IEND', b'', b'']
        iend[3] = struct.pack('>I', zlib.crc32(iend[1]) & 0xffffffff)
        iend[0] = struct.pack('>I', len(iend[2]))
        with open(filepath, 'wb') as hfile:
            hfile.write(struct.pack('>8B', 137, 80, 78, 71, 13, 10, 26, 10))
            hfile.write(b''.join(ihdr))
            hfile.write(b''.join(idat))
            hfile.write(b''.join(iend))

    def crop(self, top_left, bottom_right):
        top = min(top_left[1], bottom_right[1])
        right = max(top_left[0], bottom_right[0])
        bottom = max(top_left[1], bottom_right[1])
        left = min(top_left[0], bottom_right[0])
        assert 0 <= left and left < self.width
        assert 0 <= top and top < self.height
        width = right - left
        height = bottom - top
        assert 0 < width and width <= self.width
        assert 0 < height and height <= self.height
        line = 4 * width
        raw = bytearray(line * height)
        for y in range(height):
            offset = 4 * (self.width * (top + y) + left)
            raw[line * y:line * (y + 1)] = self.bgrr[offset:offset + line]
        return type(self)((width, height), raw)

    def resize(self, width, height):
        ''' http://blog.csdn.net/liyuan02/article/details/6765442
        '''
        assert 0 < width
        assert 0 < height
        line = 4 * width
        raw = bytearray(line * height)
        ratio_x = (self.width << 16) / width
        ratio_y = (self.height << 16) / height
        line0 = 4 * self.width
        for y in range(height):
            y0 = int(y * ratio_y) >> 16
            offset = y * line
            offset0 = y0 * line0
            for x in range(width):
                x0 = int(x * ratio_x) >> 16
                raw[offset + 4 * x:offset + 4 * x + 4] = \
                    self.bgrr[offset0 + 4 * x0:offset0 + 4 * x0 + 4]
        return type(self)((width, height), raw)

    def histogram(self, bit = 2):
        ''' http://www.ruanyifeng.com/blog/2013/03/similar_image_search_part_ii.html
        '''
        assert isinstance(bit, int) and 0 < bit and bit < 9
        values = range(1 << bit)
        bit = 8 - bit
        space = [
            [
                [0 for i in values] for j in values
            ] for k in values
        ]
        for i in range(0, len(self.bgrr), 4):
            r = self.bgrr[2 + i] >> bit
            g = self.bgrr[1 + i] >> bit
            b = self.bgrr[i] >> bit
            space[r][g][b] += 1
        return tuple(tuple(tuple(b) for b in r) for r in space)

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
        if '.png' == ext:
            return cls._png(blob)

    @classmethod
    def _png(cls, blob):
        width, height = struct.unpack('>2I', blob[16:24])
        idat_size, = struct.unpack('>I', blob[33:37])
        blob = zlib.decompress(blob[41:41 + idat_size])
        rgbs = b''
        for y in range(height):
            rgbs += blob[1 + (1 + 3 * width) * y:(1 + 3 * width) * (1 + y)]
        rgbs = bytearray(rgbs)
        raw = bytearray(4 * width * height)
        raw[0::4], raw[1::4], raw[2::4] = rgbs[2::3], rgbs[1::3], rgbs[0::3]
        return cls((width, height), raw)
