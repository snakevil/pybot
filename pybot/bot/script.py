# encoding: utf-8

import signal
from ..player import Window as Player
from .expect import Base as Expect
from .action import Base as Action
from .trigger import Trigger
from .bot import Bot

class Script(object):
    def __init__(self, *roles):
        self.roles = roles or ['']
        self._target = self.roles[0]
        self._triggers = {role: [] for role in self.roles}

    def role(self, role = ''):
        assert role in self.roles
        self._target = role
        return self

    def on(self, expect, action):
        assert isinstance(expect, Expect)
        assert isinstance(action, Action)
        self._triggers[self._target].append(Trigger(expect, action))
        return self

    def halt(self, signum, frame):
        for role in self.roles:
            self._bots[role].stop()

    def perform(self, players, **context):
        if isinstance(players, Player):
            players = {'': players}
        self._bots = {}
        signal.signal(signal.SIGINT, self.halt)
        signal.signal(signal.SIGTERM, self.halt)
        for role in self.roles:
            assert isinstance(players.get(role), Player)
            players[role].aka(role or 'player')
            self._bots[role] = Bot(players[role], context.copy())
            for trigger in self._triggers[role]:
                self._bots[role].handle(trigger)
            self._bots[role].start()
        while True:
            running = True
            for role in self.roles:
                running = running and self._bots[role].is_alive()
            if running:
                self._bots[self.roles[0]].join(.1)
            else:
                break
