# encoding: utf-8

import sys
from .chain import Chain
from ..player import Window

class Rite(object):
    def __init__(self, *roles):
        self.roles = roles or ['']
        self.chains = []

    def role(self, role = ''):
        assert role in self.roles
        chain = Chain(self, role)
        self.chains.append(chain)
        return chain

    def perform(self, players, **context):
        if isinstance(players, Window):
            players = {'': players}
        for role in self.roles:
            assert isinstance(players.get(role), Window)
            players[role].aka(role or 'master')
        context = dict({
            'tick': 250,
            'loop': 1,
            'log': print,
            'dbg': lambda message: print(message, file = sys.stderr)
        }, **context)
        context['log']('# $tick = %d' % context['tick'])
        for index in range(context['loop']) :
            for chain in self.chains:
                chain.chant(players[chain.caster], context)
        for role in self.roles:
            players[role].aka('')
