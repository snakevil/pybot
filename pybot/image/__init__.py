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
        return '(%d %d %d)' % (self.r, self.g, self.b)

    def __eq__(self, another):
        r = g = b = -1
        its_type = type(another)
        if its_type == tuple or its_type == list:
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

class Pixel(Color):
    def __init__(self, pos, rgb):
        self.x = pos[0]
        self.y = pos[1]
        super(Pixel, self).__init__(*rgb)

    def __str__(self):
        return '%d,%d %s' % (self.x, self.y, super(Pixel, self).__str__())

    def __eq__(self, another):
        x = y = r = g = b = -1
        its_type = type(another)
        try:
            if its_type == tuple or its_type == list:
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
