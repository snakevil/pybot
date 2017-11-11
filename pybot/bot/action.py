# encoding: utf-8

import random
import time
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

class Action(Base):
    def then(self, action):
        return Thenable().then(self).then(action)

class Noop(Action):
    def __init__(self, desc):
        super(Noop, self).__init__()
        self.desc = desc

    def apply(self, player, context = {}):
        super(Noop, self).apply(player, context)
        self.log(self.desc)
        return context

class Grab(Action):
    def apply(self, player, context = {}):
        super(Grab, self).apply(player, context)
        image = player.snap()
        if image:
            filepath = '%s-%d.png' % (player, int(time.time()))
            image.save(filepath)
            self.log(filepath)
        return context

class Wait(Action):
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

class Fire(Action):
    def __init__(self, point, spread = 0):
        super(Fire, self).__init__()
        if isinstance(point, tuple):
            if isinstance(point[0], tuple):
                self.target = window.Rect(point)
            elif isinstance(spread, tuple):
                self.target = window.Rect(point, spread)
                spread = 0
            else:
                self.target = window.Point(point)
        else:
            self.target = window.Point(point, spread)
            spread = 0
        assert isinstance(spread, int) and 0 <= spread
        self.spread = spread

    def apply(self, player, context = {}):
        super(Fire, self).apply(player, context)
        if isinstance(self.target, window.Rect):
            if self.spread:
                point = self.target.random(self.spread)
            else:
                point = self.target.center
        elif self.spread:
            point = self.target.spread(self.spread)
        else:
            point = self.target
        self.log(point)
        player.click(point)
        return context

__all__ = [
    'Action',
    'Noop',
    'Wait', 'Fire'
]
