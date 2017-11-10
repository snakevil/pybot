# encoding: utf-8

import random
from .. import player as window

class Base(object):
    def __init__(self):
        self.context = {}

    def log(self, message):
        message = '%s <%s> %s' % (
            self.player,
            type(self).__name__,
            message
        )
        log = self.context.get('log')
        if hasattr(log, '__call__'):
            log(message)

    def apply(self, player, context = {}):
        assert isinstance(player, window.Window)
        assert isinstance(context, dict)
        self.player = player
        self.context = context
        return context

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self.actions = []

    def apply(self, player, context = {}):
        super(Thenable, self).apply(player, context)
        for action in self.actions:
            context = action.apply(player, context)
        return context

    def then(self, action):
        assert isinstance(action, Base)
        self.actions.append(action)
        return self

class Base1(Base):
    def then(self, action):
        return Thenable().then(self).then(action)

class Noop(Base1):
    def __init__(self, desc):
        super(Noop, self).__init__()
        self.desc = desc

    def apply(self, player, context = {}):
        super(Noop, self).apply(player, context)
        self.log(self.desc)
        return context

class Wait(Base1):
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
        return context

class Fire(Base1):
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
        return context

__all__ = [
    'Noop',
    'Wait', 'Fire'
]
