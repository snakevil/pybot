# encoding: utf-8

import signal

from .. import core, player

from .expect import Base as Expect
from .react import Base as React
from .reflex import Reflex
from .competence import Competence
from .bot import Bot
from .ecompany import ECompany

class Mission(core.Firable):
    def __init__(self, *companies):
        super(Mission, self).__init__()
        self._companies = companies or ['']
        self._company = self._companies[0]
        self._reflexes = {company: [] for company in self._companies}
        self._logq = []
        self._level = 1
        self._bots = {}

        def on_log(self, message, level = 0):
            if level < self._level:
                return
            desc = '[debg] ' if not level \
                else '[info] ' if 1 == level \
                else '[warn] ' if 2 == level \
                else '[errr] ' if 3 == level \
                else '[crit] ' if 4 == level \
                else ''
            print('%s%s' % (desc, message))
            return False
        self.on('log', on_log)

    def company(self, company = ''):
        if company not in self._companies:
            raise ECompany(company, self._companies)
        self._company = company
        return self

    def co(self, company = ''):
        return self.company(company)

    def reflex(self, expect, react, title = ''):
        if not isinstance(expect, Expect):
            raise core.EType(expect, Expect)
        if not isinstance(react, React):
            raise core.EType(react, React)
        reflex = Reflex(expect, react, title = title)
        self._logq.append(('@%s injected %s' % (self._company, reflex), 1))
        self._reflexes[self._company].append(reflex)
        return self

    def inject(self, reflex):
        if not isinstance(reflex, Reflex):
            raise core.EType(reflex, Reflex)
        self._logq.append(('@%s injected %s' % (self._company, reflex), 1))
        self._reflexes[self._company].append(reflex)
        return self

    def clone(self, competence):
        if not isinstance(competence, Competence):
            raise core.EType(competence, Competence)
        self._logq.append(('@%s cloned %s' % (self._company, competence), 1))
        self._reflexes[self._company].extend(competence)
        return self

    def halt(self, signum, frame):
        sigid = 'SIGINT' if 2 == signum \
            else 'SIGTERM' if 15 == signum \
            else ''
        if sigid:
            self.fire('log', 'aborting for %s...' % sigid, 0)
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
        level = context.get('log')
        if level:
            del context['log']
            if isinstance(level, int):
                self._level = 255 if 0 > level else min(255, level)
            else:
                level = str(level).lower()
                self._level = 0 if 'debug' == level or 'debg' == level \
                    else 1 if 'info' == level \
                    else 2 if 'warn' == level or 'warning' == level \
                    else 3 if 'errr' == level or 'error' == level \
                    else 4 if 'crit' == level or 'critical' == level \
                        or 'fatal' == level \
                    else 255

        fps = context.get('fps')
        if fps:
            del context['fps']
        if not isinstance(fps, int) or 0 > fps or 60 < fps:
            fps = 10
        self.fire('log', 'FPS: %d' % fps, 2)

        timeout = context.get('timeout')
        if timeout:
            del context['timeout']
        if not isinstance(timeout, int) or 0 > timeout:
            timeout = 60
        self.fire('log', 'Timeout: %d' % timeout, 2)

        signal.signal(signal.SIGINT, self.halt)
        signal.signal(signal.SIGTERM, self.halt)

        for log in self._logq:
            self.fire('log', *log)
        self._logq = []

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
                timeout = timeout
            ).on(
                'log',
                lambda *args: self.fire('log', *args)
            ).on(
                'error',
                self._on_bot_error
            )
            self._bots[company].inject(*self._reflexes[company])
            self._bots[company].start()

    def complete(self):
        for bot in self._bots.values():
            self.fire('log', '%s quit' % bot.player, 4)
            bot.player.quit()

    def _on_bot_error(self, bot):
        self.halt(0, None)
        others = [other for other in self._bots.values() if other != bot]
        if others:
            while self.running:
                others[0].join(.1)
            try:
                bot.player.quit()
            except:
                pass
            for bot in others:
                self.fire('log', '%s quit' % bot.player, 4)
                bot.player.quit()
        self.fire('error')
