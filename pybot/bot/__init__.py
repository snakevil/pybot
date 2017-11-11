# encoding: utf-8

import sys
from . import expect
from . import action
from .. import player as window

class Spell(object):
    def __init__(self, how, when = None):
        assert isinstance(how, action.Base)
        assert not when or isinstance(when, expect.Base)
        self.action = how
        self.expect = when

    def cast(self, player, context = {}):
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

class Chain(object):
    def __init__(self, script, role = ''):
        assert isinstance(script, Script)
        self.spells = []
        self.script = script
        self.role = role

    def cast(self, spell):
        assert isinstance(spell, Spell)
        self.spells.append(spell)
        return self

    def until(self, when, how):
        return self.cast(Spell(how, when))

    def do(self, what):
        return self.cast(Spell(what))

    def idle(self, nmsecs, xmsecs = 0):
        return self.do(action.Wait(nmsecs, xmsecs))

    def perform(self, context = {}):
        player = self.script.identify(self.role)
        for spell in self.spells:
            spell.cast(player, context)
        return context

    def player(self, role = ''):
        return self.script.player(role)

    def play(self, players, **context):
        return self.script.play(players, **context)

class Script(object):
    def __init__(self, *roles):
        self.roles = roles or ['']
        self.chains = []

    def player(self, role = ''):
        assert role in self.roles
        chain = Chain(self, role)
        self.chains.append(chain)
        return chain

    def play(self, players, **context):
        if isinstance(players, window.Window):
            players = {'': players}
        for role in self.roles:
            assert isinstance(players.get(role), window.Window)
            players[role].aka(role or 'player')
        context = dict({
            'tick': 250,
            'loop': 1,
            'log': print,
            'dbg': lambda message: print(message, file = sys.stderr)
        }, **context)
        context['log']('# $tick = %d' % context['tick'])
        self.players = players
        for index in range(context['loop']) :
            for chain in self.chains:
                chain.perform(context)
        self.players = None
        for role in self.roles:
            players[role].aka('')

    def identify(self, role):
        return self.players[role]

__all__ = [
    'Spell',
    'Chain',
    'Script'
]
