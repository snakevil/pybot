# encoding: utf-8

from ...player import Point, Rect
from .action import Action

class Spot(Action):
    def __init__(self, id):
        super(Spot, self).__init__(1)
        self._id = id

    def __repr__(self):
        return 'Spot(%r)' % self._id

    def do(self, event):
        spot = event['__spots__'].get(self._id)
        if spot:
            event.log('!%r represented as Fire%r' % (self, spot))
            if isinstance(spot[0], Rect):
                if spot[1]:
                    point = spot[0].random(spot[1])
                else:
                    point = spot[0].center
            elif spot[1]:
                point = spot[0].spread(spot[1])
            else:
                point = spot[0]
            event.click(point)
        else:
            event.log('!%r missing' % self, 3)
