# encoding: utf-8

import random
from .. import image
from .. import player as window

class Base(object):
    def __init__(self, context = {}):
        assert isinstance(context, dict)
        self.context = context

    def log(self, message):
        message = '%s <%s> %s' % (
            self.player,
            type(self).__name__,
            message
        )
        log = self.context.get('log')
        if hasattr(log, '__call__'):
            log(message)
        else:
            print message

    def apply(self, player, context = {}):
        assert isinstance(player, window.Window)
        self.player = player
        assert isinstance(context, dict)
        if context:
            self.context = dict(self.context, **context)
        return self

    def then(self, action):
        assert isinstance(action, type(self))
        return action.apply(self.player, self.context)

class Wait(Base):
    def __init__(self, nmsecs, xmsecs = 0):
        assert isinstance(nmsecs, int) and 0 < nmsecs
        assert isinstance(xmsecs, int) and 0 <= xmsecs
        super(Wait, self).__init__()
        if not xmsecs:
            xmsecs = nmsecs
        self.nmsecs = min(nmsecs, xmsecs)
        self.xmsecs = max(nmsecs, xmsecs)

    def apply(self, player, context = {}):
        super(Wait, self).apply(player, context)
        msecs = random.randint(self.nmsecs, self.xmsecs)
        self.log('%d ms' % msecs)
        player.idle(msecs)
        return self

class Fire(Base):
    def __init__(self, point, spread = 0):
        assert isinstance(spread, int) and 0 <= spread
        super(Fire, self).__init__()
        self.point = point if isinstance(point, window.Point) \
            else window.Point(point)
        self.spread = spread

    def apply(self, player, context = {}):
        super(Fire, self).apply(player, context)
        point = self.point if not self.spread \
            else point.spread(self.spread)
        self.log(point)
        player.click(point)
        return self

class PixelMatch(Base):
    def __init__(self, *pixels):
        assert 0 < len(pixels)
        super(PixelMatch, self).__init__()
        threshold = 10
        if isinstance(pixels[-1], int):
            threshold = pixels[-1]
            del pixels[-1]
            assert 0 <= threshold
        self.pixels = [
            pixel if isinstance(pixel, image.Pixel) \
                else image.Pixel(*pixel) \
                for pixel in pixels
        ]
        self.threshold = threshold

    def apply(self, player, context = {}):
        super(PixelMatch, self).apply(player, context)
        bingo = True
        image = player.snap()
        if image:
            for expected in self.pixels:
                pixel = image.pixel(expected.x, expected.y)
                if self.threshold < pixel - expected:
                    bingo = False
                    self.log('%s dismatched' % pixel)
            self.log('succeed' if bingo else 'failed')
        else:
            bingo = False
            self.log('failed for %s minimized' % player)
        self.context['PixelMatch'] = bingo
        return self

class UntilPixelMatch(PixelMatch):
    def apply(self, player, context = {}):
        while True:
            super(UntilPixelMatch, self).apply(player, context)
            if self.context.get('PixelMatch'):
                del self.context['PixelMatch']
                break
            player.idle(100)
            self.log('retry in 100 msecs')
        return self
