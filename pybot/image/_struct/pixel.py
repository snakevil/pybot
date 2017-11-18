# encoding: utf-8

from .color import Color

class Pixel(Color):
    def __init__(self, pos, rgba):
        self.x = pos[0]
        self.y = pos[1]
        super(Pixel, self).__init__(*rgba)

    def __repr__(self):
        return 'Pixel((%d, %d), (%d, %d, %d, %d))' % (
            self.x,
            self.y,
            self.r,
            self.g,
            self.b,
            self.a
        )

    def __eq__(self, another):
        x = y = r = g = b = a = -1
        another_type = type(another)
        try:
            if another_type == tuple or another_type == list:
                x = another[0][0]
                y = another[0][1]
                r = another[1][0]
                g = another[1][1]
                b = another[1][2]
                a = another[1][3]
            else:
                x = another.x
                y = another.y
                r = another.r
                g = another.g
                b = another.b
                a = another.a
        except: pass
        return self.x == x and self.y == y \
            and self.r == r and self.g == g and self.b == b and self.a == a

    def __ne__(self, another):
        return not self.__eq__(another)

    def __sub__(self, another):
        r = g = b = -1
        a = 255
        another_type = type(another)
        try:
            if another_type == tuple or another_type == list:
                r = another[1][0]
                g = another[1][1]
                b = another[1][2]
                a = another[1][3]
            else:
                r = another.r
                g = another.g
                b = another.b
                a = another.a
        except: pass
        return super(Pixel, self).__sub__((r, g, b, a))
