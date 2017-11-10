# encoding: utf-8

from . import expect
from . import action
from .. import player as window

class Spell(object):
    def __init__(self, how, when = None):
        assert isinstance(action, action.Base)
        assert not when or isinstance(when, expect.Base)
        self.action = how
        self.expect = when

    def cast(self, player, context = {}):
        tick = 100
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
    def __init__(self, script, player = ''):
        assert isinstance(script, Script)
        self.spells = []
        self.script = script
        self.player = player

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
        player = self.script.identify(self.player)
        for spell in self.spells:
            spell.cast(player, context)
        return context

    def player(self, codename = ''):
        return self.script.player(codename)

    def play(self, chars):
        return self.script.play(chars)

class Script(object):
    def __init__(self, *codenames):
        self.codenames = codenames or ['']
        self.chains = []

    def player(self, codename = ''):
        assert codename in self.chars
        chain = Chain(self, codename)
        self.chains.append(chain)
        return chain

    def play(self, chars, **context):
        if isinstance(chars, window.Window):
            chars = {'': chars}
        for codename in self.codenames:
            assert isinstance(chars.get(codename), window.Window)
        self.players = chars
        for chain in self.chains:
            chain.perform(context)
        self.players = None

    def identify(self, codename):
        return self.players[codename]
