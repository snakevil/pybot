# encoding: utf-8

import struct
import zlib

class Color(object):
    def __init__(self, r, g = None, b = None):
        if type(r) == tuple:
            g = r[1]
            b = r[2]
            r = r[0]
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return '(%d %d %d)' % (self.r, self.g, self.b)

    def __eq__(self, another):
        r = g = b = -1
        another_type = type(another)
        if another_type == tuple or another_type == list:
            r = another[0]
            g = another[1]
            b = another[2]
        else:
            try:
                r = another.r
                g = another.g
                b = another.b
            except: pass
        return self.r == r and self.g == g and self.b == b

    def __ne__(self, another):
        return not self.__eq__(another)

class Pixel(Color):
    def __init__(self, pos, rgb):
        self.x = pos[0]
        self.y = pos[1]
        super(Pixel, self).__init__(*rgb)

    def __str__(self):
        return '%d,%d %s' % (self.x, self.y, super(Pixel, self).__str__())

    def __eq__(self, another):
        x = y = r = g = b = -1
        another_type = type(another)
        try:
            if another_type == tuple or another_type == list:
                x = another[0][0]
                y = another[0][1]
                r = another[1][0]
                g = another[1][1]
                b = another[1][2]
            else:
                x = another.x
                y = another.y
                r = another.r
                g = another.g
                b = another.b
        except: pass
        return self.x == x and \
            self.y == y and \
            self.r == r and \
            self.g == g and \
            self.b == b

    def __ne__(self, another):
        return not self.__eq__(another)

class Screenshot(object):
    def __init__(self, raw, size):
        self.__pixels = None
        self.bgra = raw
        size_type = type(size)
        if size_type == tuple or size_type == list:
            self.width = size[0]
            self.height = size[1]
        else:
            self.width = size.width
            self.height = size.height

    def pixel(self, x, y):
        if not self.__pixels:
            rgbs = zip(self.bgra[2::4], self.bgra[1::4], self.bgra[0::4])
            self.__pixels = tuple(zip(*[iter(rgbs)] * self.width))
        return Pixel((x, y), self.__pixels[y][x])

    def save(self, filepath):
        rgb = bytearray(self.width * self.height * 3)
        rgb[0::3] = self.bgra[2::4]
        rgb[1::3] = self.bgra[1::4]
        rgb[2::3] = self.bgra[0::4]
        rgb = bytes(rgb)
        width = 3 * self.width
        nul = struct.pack('>B', 0)
        scanlines = b''.join(
            [nul + rgb[y * width:(1 + y) * width] for y in range(self.height)]
        )
        ihdr = [b'', b'IHDR', b'', b'']
        ihdr[2] = struct.pack('>2I5B', self.width, self.height, 8, 2, 0, 0, 0)
        ihdr[3] = struct.pack('>I', zlib.crc32(b''.join(ihdr[1:3])) & 0xffffffff)
        ihdr[0] = struct.pack('>I', len(ihdr[2]))
        idat = [b'', b'IDAT', zlib.compress(scanlines), b'']
        idat[3] = struct.pack('>I', zlib.crc32(b''.join(idat[1:3])) & 0xffffffff)
        idat[0] = struct.pack('>I', len(idat[2]))
        iend = [b'', b'IEND', b'', b'']
        iend[3] = struct.pack('>I', zlib.crc32(iend[1]) & 0xffffffff)
        iend[0] = struct.pack('>I', len(iend[2]))
        with open(filepath, 'wb') as hfile:
            hfile.write(struct.pack('>8B', 137, 80, 78, 71, 13, 10, 26, 10))
            hfile.write(b''.join(ihdr))
            hfile.write(b''.join(idat))
            hfile.write(b''.join(iend))

    def dump(self, filepath):
        with open(filepath, 'wb') as hfile:
            hfile.write(struct.pack('>2H', self.width, self.height))
            hfile.write(bytes(self.bgra))

    @classmethod
    def parse(cls, filepath):
        hfile = open(filepath, 'rb')
        size = struct.unpack('>2H', hfile.read(4))
        raw = bytearray(hfile.read())
        hfile.close()
        return cls(raw, size)
