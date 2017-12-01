# encoding: utf-8

import signal
from .. import core, player
from .expect import Base as Expect
from .react import Base as React
from .reflex import Reflex
from .competence import Competence
from .bot import Bot
from .ecompany import ECompany

class Mission(object):
    def __init__(self, *companies):
        self._companies = companies or ['']
        self._company = self._companies[0]
        self._reflexes = {company: [] for company in self._companies}
        self._log = self._logger
        self._qlog = []
        self._level = 1
        self._bots = {}

    def company(self, company = ''):
        if company not in self._companies:
            raise ECompany(company, self._companies)
        self._company = company
        return self

    def co(self, company = ''):
        return self.company(company)

    def on(self, expect, react, title = ''):
        if not isinstance(expect, Expect):
            raise core.EType(expect, Expect)
        if not isinstance(react, React):
            raise core.EType(react, React)
        reflex = Reflex(expect, react, title = title)
        self._qlog.append(('@%s injected %s' % (self._company, reflex), 1))
        self._reflexes[self._company].append(reflex)
        return self

    def inject(self, reflex):
        if not isinstance(reflex, Reflex):
            raise core.EType(reflex, Reflex)
        self._qlog.append(('@%s injected %s' % (self._company, reflex), 1))
        self._reflexes[self._company].append(reflex)
        return self

    def clone(self, competence):
        if not isinstance(competence, Competence):
            raise core.EType(competence, Competence)
        self._qlog.append(('@%s cloned %s' % (self._company, competence), 1))
        self._reflexes[self._company].extend(competence)
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
        self._log('aborting for %s...' % sigid, 0)
        for company in self._companies:
            self._bots[company].stop()

    @property
    def running(self):
        if not self._bots:
            return False
        running = True
        for company in self._companies:
            running = running and self._bots[company].is_alive()
        return running

    def await(self, tick = 1000):
        tick /= 1000
        while self.running:
            self._bots[self._companies[0]].join(tick)

    def exec(self, players, **context):
        self._log = context.get('log')
        if self._log:
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
        else:
            self._log = self._logger

        fps = context.get('fps')
        if fps:
            del context['fps']
        if not isinstance(fps, int) or 0 > fps or 60 < fps:
            fps = 10
        self._log('FPS: %d' % fps, 2)

        timeout = context.get('timeout')
        if timeout:
            del context['timeout']
        if not isinstance(timeout, int) or 0 > timeout:
            timeout = 60
        self._log('Timeout: %d' % timeout, 2)

        signal.signal(signal.SIGINT, self.halt)
        signal.signal(signal.SIGTERM, self.halt)

        for log in self._qlog:
            self._log(*log)
        self._qlog = []

        if isinstance(players, player.Window):
            players = {'': players}
        tick = 1000 / fps
        self._bots = {}
        for company in self._companies:
            if not isinstance(players.get(company), player.Window):
                raise core.EType(players.get(company), player.Window)
            players[company].aka(company or 'Adam')
            self._bots[company] = Bot(
                players[company],
                context.copy(),
                tick = tick,
                log = self._log,
                timeout = timeout
            )
            self._bots[company].inject(*self._reflexes[company])
            self._bots[company].start()
