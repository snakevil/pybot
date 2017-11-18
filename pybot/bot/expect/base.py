# encoding: utf-8

from ...player import Point, Rect

class Base(object):
    def __init__(self, **spots):
        self.spots = {}
        for id in spots:
            self.spot(spot, *spots[id])

    def __repr__(self):
        return '%s()' % type(self).__name__

    def __and__(self, another):
        assert False

    def __iand__(self, another):
        return self.__and__(another)

    def __or__(self, another):
        assert False

    def __ior__(self, another):
        return self.__or__(another)

    def spot(self, id, point, spread = 0):
        if isinstance(point, tuple):
            if isinstance(point[0], tuple):
                region = Rect(point)
            elif isinstance(spread, tuple):
                region = Rect(point, spread)
                spread = 0
            else:
                region = Point(point)
        else:
            region = Point(point, spread)
            spread = 0
        assert isinstance(spread, int) and 0 <= spread
        self._spots[id] = (region, spread)
        return self

    def test(self, event):
        return False
