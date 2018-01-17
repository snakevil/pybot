# encoding: utf-8

import time
import struct
import base64

from .. import core
from ._struct import Pixel
from ._codec import PNG
from ._codec.edepth import EDepth
from .ecoordinate import ECoordinate

class Base(object):
    def __init__(self, size, raw):
        if isinstance(size, tuple) or isinstance(size, list):
            self.width = size[0]
            self.height = size[1]
        else:
            self.width = size.width
            self.height = size.height
        self.raw = raw
        self.timestamp = time.time()

    def __str__(self):
        width = 64
        blob = b''.join([
            struct.pack('>2H', self.width, self.height),
            self.raw
        ])
        clob = base64.b64encode(blob).decode('utf-8')
        return '\n'.join(
            clob[i:i + width] for i in range(0, len(clob), width)
        )

    def pixel(self, x, y):
        if 1 > x or x >= self.width or 1 > y or y >= self.height:
            raise ECoordinate(x, y)
        offset = self.width * y + x << 2
        return Pixel(
            (x, y),
            tuple(self.raw[offset:offset + 4])
        )

    def save(self, filepath):
        rpos = filepath.rfind('.')
        if -1 < rpos:
            ext = filepath[rpos:]
        else:
            ext = '.png'
            filepath += ext
        if '.png' != ext:
            raise core.ETodo('image.base.save.jpeg')
        with open(filepath, 'wb') as hfile:
            hfile.write(self._png())

    def _png(self):
        png = PNG(self.width, self.height, type = PNG.TRUECOLOR_ALPHA)
        return png.encode(self.raw)

    def crop(self, top_left, bottom_right):
        top = min(top_left[1], bottom_right[1])
        right = max(top_left[0], bottom_right[0])
        bottom = max(top_left[1], bottom_right[1])
        left = min(top_left[0], bottom_right[0])
        if 0 > left or left >= self.width or 0 > top or top >= self.height:
            raise ECoordinate(left, top)
        if 1 > right or right > self.width or 1 > bottom or bottom > self.height:
            raise ECoordinate(right, bottom)
        width = max(1, right - left)
        height = max(1, bottom - top)
        size = width << 2
        raw = bytearray(size * height)
        for y in range(height):
            offset = self.width * (top + y) + left << 2
            raw[size * y:size * (y + 1)] = self.raw[offset:offset + size]
        return type(self)((width, height), raw)

    def resize(self, width, height):
        ''' http://blog.csdn.net/liyuan02/article/details/6765442
        '''
        width = max(1, width)
        height = max(1, height)
        size = width << 2
        raw = bytearray(size * height)
        ratio_x = (self.width << 16) / width + 1
        ratio_y = (self.height << 16) / height + 1
        size0 = self.width << 2
        for y in range(height):
            y0 = int(y * ratio_y) >> 16
            offset = y * size
            offset0 = y0 * size0
            for x in range(width):
                x0 = int(x * ratio_x) >> 16
                raw[offset + (x << 2):offset + (x << 2) + 4] = \
                    self.raw[offset0 + (x0 << 2):offset0 + (x0 << 2) + 4]
        return type(self)((width, height), raw)

    def histogram(self, depth = 2):
        ''' http://www.ruanyifeng.com/blog/2013/03/similar_image_search_part_ii.html
        '''
        if not isinstance(depth, int) or depth not in [1, 2, 4, 8]:
            raise EDepth(depth)
        values = range(1 << depth)
        depth = 8 - depth
        space = [
            [
                [0 for i in values] for j in values
            ] for k in values
        ]
        for i in range(0, len(self.raw), 4):
            a = self.raw[i + 3]
            if not a:
                space[0][0][0] += 1
                continue
            r = self.raw[i]
            g = self.raw[i + 1]
            b = self.raw[i + 2]
            if 255 == a:
                r >>= depth
                g >>= depth
                b >>= depth
            else:
                a = (a << 8) // 255
                r >>= depth + 8
                g >>= depth + 8
                b >>= depth + 8
            space[r][g][b] += 1
        return (b for r in space for g in r for b in g)
