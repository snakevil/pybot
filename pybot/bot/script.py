# encoding: utf-8

import sys
from ..player import Window as Player
from .expect import Base as Expect
from .action import Base as Action
from .trigger import Trigger
from .bot import Bot

class Script(object):
    def __init__(self, *roles):
        self.roles = roles or ['']
        self._target = roles[0]
        self._triggers = {role: [] for role in self.roles}

    def role(self, role = ''):
        assert role in self.roles
        self._target = role

    def on(self, expect, action):
        assert isinstance(expect, Expect)
        assert isinstance(action, Action)
        self._triggers[self._target].append(Trigger(expect, action))

    def perform(self, players, **context):
        if isinstance(players, Player):
            players = {'': players}
        bots = {}
        for role in self.roles:
            assert isinstance(players.get(role), Player)
            players[role].aka(role or 'player')
            context2 = {}
            context2.update(context)
            bots[role] = Bot(players[role], context2)
            for trigger in self._triggers[role]:
                bots[role].handle(trigger)
            bots[role].start()
