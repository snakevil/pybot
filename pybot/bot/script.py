# encoding: utf-8

import signal
from ..player import Window as Player
from .expect import Base as Expect
from .action import Base as Action
from .trigger import Trigger
from .bot import Bot

class Script(object):
    def __init__(self, *roles):
        self._roles = roles or ['']
        self._target = self._roles[0]
        self._triggers = {role: [] for role in self._roles}
        self._log = self._logger

    def role(self, role = ''):
        assert role in self._roles
        self._target = role
        return self

    def on(self, expect, action, title = ''):
        assert isinstance(expect, Expect)
        assert isinstance(action, Action)
        self._triggers[self._target].append(
            Trigger(
                expect,
                action,
                title = title
            )
        )
        return self

    def _logger(self, message, level = 0):
        desc = 'debg' if not level \
            else 'info' if 1 == level \
            else 'warn' if 2 == level \
            else 'errr'
        print('[%s] %s' % (desc, message))

    def halt(self, signum, frame):
        sigid = 'SIGINT' if 2 == signum \
            else 'SIGTERM' if 15 == signum \
            else signum
        self._log('quitting for %s received...' % sigid, 0)
        for role in self._roles:
            self._bots[role].stop()

    def perform(self, players, **context):
        if isinstance(players, Player):
            players = {'': players}

        self._log = context.get('log')
        if self._log:
            del context['log']
        if not callable(self._log):
            self._log = self._logger

        fps = context.get('fps')
        if fps:
            del context['fps']
        if not isinstance(fps, int) or 0 > fps or 60 < fps:
            fps = 10
        self._log('FPS: %d' % fps, 2)

        signal.signal(signal.SIGINT, self.halt)
        signal.signal(signal.SIGTERM, self.halt)

        tick = 1000 / fps
        self._bots = {}
        for role in self._roles:
            assert isinstance(players.get(role), Player)
            players[role].aka(role or 'player')
            self._bots[role] = Bot(
                players[role],
                context.copy(),
                tick,
                self._log
            )
            for trigger in self._triggers[role]:
                self._bots[role].handle(trigger)
            self._bots[role].start()
        self._log('started', 1)

        tick /= 1000
        while True:
            running = True
            for role in self._roles:
                running = running and self._bots[role].is_alive()
            if running:
                self._bots[self._roles[0]].join(tick)
            else:
                break
        self._log('goodbye :)', 1)
