# encoding: utf-8

import signal
from ..player import get_euid, su, Window as Player
from .expect import Base as Expect
from .react import Base as React
from .reflex import Reflex
from .bot import Bot

class Mission(object):
    def __init__(self, *companies):
        self._companies = companies or ['']
        self._co = self._companies[0]
        self._reflexes = {company: [] for company in self._companies}
        self._log = self._logger
        self._bots = {}

    def company(self, company = ''):
        assert company in self._companies
        self._co = company
        return self

    def co(self, company = ''):
        return self.company(company)

    def on(self, expect, react, title = ''):
        assert isinstance(expect, Expect)
        assert isinstance(react, React)
        self._reflexes[self._co].append(
            Reflex(
                expect,
                react,
                title = title
            )
        )
        return self

    def inject(self, reflex):
        assert isinstance(reflex, Reflex)
        self._reflexes[self._co].append(Reflex)
        return self

    def clone(self, competence):
        assert isinstance(competence, Competence)
        self._reflexes[self._co].extend(competence)
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
        self._log('aborting for %s received...' % sigid, 0)
        for company in self._companies:
            self._bots[company].stop()

    def exec(self, players, **context):
        if get_euid():
            su()

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


        if isinstance(players, Player):
            players = {'': players}
        tick = 1000 / fps
        self._bots = {}
        for company in self._companies:
            assert isinstance(players.get(company), Player)
            players[company].aka(company or 'Adam')
            self._bots[company] = Bot(
                players[company],
                context.copy(),
                tick,
                self._log
            )
            for reflex in self._reflexes[company]:
                self._bots[company].inject(reflex)
            self._bots[company].start()
        self._log('started', 1)

        tick /= 1000
        while True:
            running = True
            for company in self._companies:
                running = running and self._bots[company].is_alive()
            if running:
                self._bots[self._companies[0]].join(tick)
            else:
                break
        self._log('completed :)', 1)
