# encoding: utf-8

from .action import Base as Action
from .expect import Base as Expect

class Spell(object):
    def __init__(self, how, when = None):
        assert isinstance(how, Action)
        assert not when or isinstance(when, Expect)
        self.action = how
        self.expect = when

    def chant(self, player, context = {}):
        tick = context.get('tick') or 250
        if self.expect:
            while not self.expect.test(player, context):
                player.idle(tick)
        self.action.apply(player, context)
        if self.expect:
            player.idle(tick)
            while self.expect.test(player, context):
                self.action.apply(player, context)
                player.idle(tick)
        return context
