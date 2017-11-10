# encoding: utf-8

import random
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
            else self.point.spread(self.spread)
        self.log(point)
        player.click(point)
        return self
