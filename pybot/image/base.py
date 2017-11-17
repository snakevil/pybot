# encoding: utf-8

import struct
import zlib
from ._struct import Pixel
from ._codec import PNG

class Base(object):
    def __init__(self, size, raw):
        if isinstance(size, tuple) or isinstance(size, list):
            self.width = size[0]
            self.height = size[1]
        else:
            self.width = size.width
            self.height = size.height
        self.rgba = raw

    def pixel(self, x, y):
        assert 0 <= x and x < self.width
        assert 0 <= y and y < self.height
        pos = (self.width * y + x) * 4
        return Pixel(
            (x, y),
            tuple(self.rgba[pos:pos + 4])
        )

    def save(self, filepath):
        rpos = filepath.rfind('.')
        if -1 < rpos:
            ext = filepath[rpos:]
        else:
            ext = '.png'
            filepath += ext
        if '.png' != ext:
            assert False
        with open(filepath, 'wb') as hfile:
            hfile.write(self._png())

    def _png(self):
        png = PNG(self.width, self.height, type = PNG.TRUECOLOR_ALPHA)
        return png.encode(self.rgba)

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
            raw[line * y:line * (y + 1)] = self.rgba[offset:offset + line]
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
                    self.rgba[offset0 + 4 * x0:offset0 + 4 * x0 + 4]
        return type(self)((width, height), raw)

    def histogram(self, depth = 2):
        ''' http://www.ruanyifeng.com/blog/2013/03/similar_image_search_part_ii.html
        '''
        assert isinstance(depth, int) and 0 < depth and depth < 9
        values = range(1 << depth)
        depth = 8 - depth
        space = [
            [
                [0 for i in values] for j in values
            ] for k in values
        ]
        for i in range(0, len(self.rgba), 4):
            a = self.rgba[i + 3]
            if not a:
                space[0][0][0] += 1
                continue
            r = self.rgba[i]
            g = self.rgba[i + 1]
            b = self.rgba[i + 2]
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
        return tuple(tuple(tuple(b) for b in r) for r in space)