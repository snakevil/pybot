# encoding: utf-8

from ... import core, player

class Base(object):
    def __init__(self, **spots):
        self.spots = {}
        for id in spots:
            self.spot(id, *spots[id])

    def __repr__(self):
        return '%s()' % type(self).__name__

    def __and__(self, another):
        raise core.ETodo('bot.expect.base.__and__')

    def __iand__(self, another):
        return self.__and__(another)

    def __or__(self, another):
        raise core.ETodo('bot.expect.base.__or__')

    def __ior__(self, another):
        return self.__or__(another)

    def spot(self, id, point, spread = 0):
        if isinstance(point, tuple):
            if isinstance(point[0], tuple):
                region = player.Rect(point)
            elif isinstance(spread, tuple):
                region = player.Rect(point, spread)
                spread = 0
            else:
                region = player.Point(point)
        else:
            region = player.Point(point, spread)
            spread = 0
        self.spots[id] = (region, spread)
        return self

    def test(self, event):
        return False
