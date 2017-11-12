# encoding: utf-8

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
        return 'Color(%d, %d, %d)' % (self.r, self.g, self.b)

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

    def __sub__(self, another):
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
        return (
            (self.r - r) ** 2 + (self.g - g) ** 2 + (self.b - b) ** 2
        ) ** .5
