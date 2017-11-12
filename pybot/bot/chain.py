# encoding: utf-8

from .spell import Spell
from .rite import Rite
from .action import Wait

class Chain(object):
    def __init__(self, rite, role = ''):
        assert isinstance(rite, Rite)
        self.spells = []
        self.rite = rite
        self.caster = role

    def cast(self, spell):
        assert isinstance(spell, Spell)
        self.spells.append(spell)
        return self

    def until(self, expect, action):
        return self.cast(Spell(action, expect))

    def do(self, action):
        return self.cast(Spell(action))

    def idle(self, nmsecs, xmsecs = 0):
        return self.do(Wait(nmsecs, xmsecs))

    def chant(self, player, context = {}):
        for spell in self.spells:
            spell.cast(player, context)
        return context

    def role(self, role = ''):
        return self.rite.role(role)

    def perform(self, players, **context):
        return self.rite.perform(players, **context)
