# encoding: utf-8

import time
from .. import player

class Base(object):
    def apply(self, player):
        pass

class Locate(Base):
    def __init__(self, *refs):
        self.pixels = refs

    def apply(self, player):
        found = False
        while not found:
            screenshot = player.screen()
            found = True
            for pixel in pixels:
                found &= pixel == screenshot.pixel(*pixel[0])
            if not found:
                time.sleep(.1)

class Hold(Base):
    def __init__(self, msecs):
        self.msecs = msecs

    def apply(self, player):
        time.sleep(self.msecs / 1000)

class Fire(Base):
    def __init__(self, pos, spread = 0):
        self.pos = pos
        self.spread = spread

    def apply(self, player):
        point = player.Point(self.pos)
        if self.spread:
            point = point.spread(self.spread)
        player.click(point)
