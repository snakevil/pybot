# encoding: utf-8

from ... import player
from .react import React
from .espread import ESpread

class Spot(React):
    def __init__(self, id):
        super(Spot, self).__init__(1)
        self._id = id

    def __repr__(self):
        return 'Spot(%r)' % self._id

    def do(self, event, trace):
        spot = event['__spots__'].get(self._id)
        if spot:
            if not isinstance(spot[1], int) or 0 > spot[1]:
                raise ESpread(spot[1])
            trace.append('Fire%r' % (spot,))
            if isinstance(spot[0], player.Rect):
                if spot[1]:
                    point = spot[0].random(spot[1])
                else:
                    point = spot[0].center
            elif spot[1]:
                point = spot[0].spread(spot[1])
            else:
                point = spot[0]
            trace.append(['= %r' % point])
            event.click(point)
        else:
            trace.append('None')
            event['__fatal__'] = True
