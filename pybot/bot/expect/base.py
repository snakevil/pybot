# encoding: utf-8

from ... import core, player

class Base(object):
    def __init__(self, **spots):
        self._time = 0
        self._result = False
        self.spots = {}
        for id in spots:
            self.spot(id, *spots[id])

    def __repr__(self):
        return '%s()' % type(self).__name__

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __and__(self, other):
        raise core.ETodo('bot.expect.base.__and__')

    def __iand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        raise core.ETodo('bot.expect.base.__or__')

    def __ior__(self, other):
        return self.__or__(other)

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
        if event.time != self._time:
            self._result = self._test(event)
        return self._result

    def _test(self, event):
        return False
