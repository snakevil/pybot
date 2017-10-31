# encoding: utf-8

import random
from .. import player as window

class Base(object):
    def log(self, player, message, serial = 0):
        msg = '%s <%s> %s' % (player.title, type(self).__name__, message)
        if serial:
            msg = '#%s %s' % (serial, msg)
        print msg

    def apply(self, player, serial = 0, state = {}):
        return state

class Locate(Base):
    def __init__(self, *refs):
        self.pixels = refs

    def apply(self, player, serial = 0, state = {}):
        found = False
        while not found:
            screenshot = player.screen()
            found = True
            for expected in self.pixels:
                pixel = screenshot.pixel(*expected[0])
                if 10 < pixel - expected:
                    found = False
                    self.log(
                        player,
                        '(%d, %d, %d) failed for %s' % (
                            expected[1][0],
                            expected[1][1],
                            expected[1][2],
                            pixel
                        ),
                        serial
                    )
                    break
            if not found:
                player.idle(100)
        self.log(player, 'succeed', serial)
        return state

class Wait(Base):
    def __init__(self, msecs, extra = 0):
        self.msecs = msecs
        self.extra = extra

    def apply(self, player, serial = 0, state = {}):
        msecs = self.msecs + random.randint(0, self.extra)
        self.log(player, '%d ms' % msecs, serial)
        player.idle(msecs)
        return state

class Fire(Base):
    def __init__(self, pos, spread = 0):
        self.pos = pos
        self.spread = spread

    def apply(self, player, serial = 0, state = {}):
        point = window.Point(self.pos)
        if self.spread:
            point = point.spread(self.spread)
        self.log(player, point, serial)
        player.click(point)
        return state
