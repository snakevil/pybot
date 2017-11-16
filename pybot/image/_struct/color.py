# encoding: utf-8

class Color(object):
    def __init__(self, r, g = None, b = None, a = None):
        if type(r) == tuple:
            g = r[0]
            b = r[1]
            r = r[2]
            a = r[3]
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return 'Color(%d, %d, %d, %d)' % (self.r, self.g, self.b, self.a)

    def __eq__(self, another):
        r = g = b = a = -1
        another_type = type(another)
        if another_type == tuple or another_type == list:
            r = another[0]
            g = another[1]
            b = another[2]
            a = another[3]
        else:
            try:
                r = another.r
                g = another.g
                b = another.b
                a = another.a
            except: pass
        return self.r == r and self.g == g and self.b == b and self.a == a

    def __ne__(self, another):
        return not self.__eq__(another)

    def __sub__(self, another):
        r1 = g1 = b1 = -1
        a1 = 255
        another_type = type(another)
        if another_type == tuple or another_type == list:
            r1 = another[0]
            g1 = another[1]
            b1 = another[2]
            a1 = another[3]
        else:
            try:
                r1 = another.r
                g1 = another.g
                b1 = another.b
                a1 = another.a
            except: pass
        r0 = self.r * self.a // 255
        g0 = self.g * self.a // 255
        b0 = self.b * self.a // 255
        r1 = r1 * a1 // 255
        g1 = g1 * a1 // 255
        b1 = b1 * a1 // 255
        return ((r0 - r1) ** 2 + (g0 - g1) ** 2 + (b0 - b1) ** 2) ** .5
