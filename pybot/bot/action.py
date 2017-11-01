# encoding: utf-8

import random
from .. import player as window

class Base(object):
    def log(self, player, message):
        msg = '%s <%s> %s' % (player.title, type(self).__name__, message)
        if self._context['serial']:
            msg = '#%s %s' % (self._context['serial'], msg)
        logger = self._context.get('log')
        if hasattr(logger, '__call__'):
            logger(msg)
        else:
            print msg

    def apply(self, player, context = {}):
        context.setdefault('serial', 0)
        self._context = context
        return context

class Locate(Base):
    def __init__(self, *refs):
        self.pixels = refs

    def apply(self, player, context = {}):
        context = Base.apply(player, context)
        found = False
        times = 0
        dismatched_pixel = None
        dismatched_times = 0
        while not found:
            screenshot = player.screen()
            found = True
            times += 1
            for expected in self.pixels:
                pixel = screenshot.pixel(*expected[0])
                if 10 < pixel - expected:
                    found = False
                    if dismatched_pixel != pixel:
                        dismatched_pixel = pixel
                        dismatched_times = 1
                        self.log(
                            player,
                            '(%d, %d, %d) failed for %s' % (
                                expected[1][0],
                                expected[1][1],
                                expected[1][2],
                                pixel
                            )
                        )
                    else:
                        dismatched_times += 1
                        if __debug__ and 10 == dismatched_times:
                            screenshot.save(
                                '%d,%d-%d_%d_%d.png' % (
                                    pixel.x, pixel.y,
                                    pixel.r, pixel.g, pixel.b
                                )
                            )
                    break
            if not found:
                player.idle(100)
        self.log(player, 'succeed in %d retries' % times)
        return context

class Wait(Base):
    def __init__(self, msecs, extra = 0):
        self.msecs = msecs
        self.extra = extra

    def apply(self, player, context = {}):
        context = Base.apply(player, context)
        msecs = self.msecs + random.randint(0, self.extra)
        self.log(player, '%d ms' % msecs)
        player.idle(msecs)
        return context

class Fire(Base):
    def __init__(self, pos, spread = 0):
        self.pos = pos
        self.spread = spread

    def apply(self, player, context = {}):
        context = Base.apply(player, context)
        point = window.Point(self.pos)
        if self.spread:
            point = point.spread(self.spread)
        self.log(player, point)
        player.click(point)
        return context
