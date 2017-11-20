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
        self._level = 2
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
        if level < self._level:
            return
        desc = '[debg] ' if not level \
            else '[info] ' if 1 == level \
            else '[warn] ' if 2 == level \
            else '[errr] ' if 3 == level \
            else '[crit] ' if 4 == level \
            else ''
        print('%s%s' % (desc, message))

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
        del context['log']
        if not callable(self._log):
            if isinstance(self._log, int):
                self._level = 255 if 0 > self._log \
                    else min(255, self._log)
            else:
                level = str(self._log).lower()
                self._level = 0 if 'debug' == level or 'debg' == level \
                    else 1 if 'info' == level \
                    else 2 if 'warn' == level or 'warning' == level \
                    else 3 if 'errr' == level or 'error' == level \
                    else 4 if 'crit' == level or 'critical' == level \
                        or 'fatal' == level \
                    else 255
            self._log = self._logger

        fps = context.get('fps')
        del context['fps']
        if not isinstance(fps, int) or 0 > fps or 60 < fps:
            fps = 10
        self._log('FPS: %d' % fps, 1)

        timeout = context.get('timeout')
        del context['timeout']
        if not isinstance(timeout, int) or 0 > timeout:
            timeout = 60
        self._log('Timeout: %d' % timeout, 1)

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
                tick = tick,
                log = self._log,
                timeout = timeout
            )
            for reflex in self._reflexes[company]:
                self._bots[company].inject(reflex)
            self._bots[company].start()
        self._log('started', 255)

        tick /= 1000
        while True:
            running = True
            for company in self._companies:
                running = running and self._bots[company].is_alive()
            if running:
                self._bots[self._companies[0]].join(tick)
            else:
                break
        self._log('completed :)', 255)
