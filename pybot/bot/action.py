# encoding: utf-8

import random
from .. import player as window

class Base(object):
    def log(self, player, message):
        print '%s <%s> %s' % (player.title, type(self).__name__, message)

    def apply(self, player, state = {}):
        return state

class Locate(Base):
    def __init__(self, *refs):
        self.pixels = refs

    def apply(self, player, state = {}):
        found = False
        while not found:
            screenshot = player.screen()
            found = True
            for expected in self.pixels:
                pixel = screenshot.pixel(*expected[0])
                if pixel != expected:
                    found = False
                    self.log(player, 'failed for %s' % pixel)
                    break
            if not found:
                player.idle(100)
        self.log(player, 'succeed')
        return state

class Wait(Base):
    def __init__(self, msecs, extra = 0):
        self.msecs = msecs
        self.extra = extra

    def apply(self, player, state = {}):
        msecs = self.msecs + random.randint(0, self.extra)
        self.log(player, '%d ms' % msecs)
        player.idle(msecs)
        return state

class Fire(Base):
    def __init__(self, pos, spread = 0):
        self.pos = pos
        self.spread = spread

    def apply(self, player, state = {}):
        point = window.Point(self.pos)
        if self.spread:
            point = point.spread(self.spread)
        self.log(player, point)
        player.click(point)
        return state
