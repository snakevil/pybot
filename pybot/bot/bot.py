# encoding: utf-8

import threading
import time
from .event import Event

class Bot(threading.Thread):
    def __init__(self, player, context, **config):
        super(Bot, self).__init__()
        self._player = player
        self._ = config
        self.context = context
        self._enabled = threading.Event()
        self._exited = False
        self._activity = time.time()
        self._reflexes = {}
        self.enable()

    def stop(self):
        self._['log']('%s cleaning...' % self._player, 1)
        self._exited = True

    def inject(self, *reflexes):
        for reflex in reflexes:
            exist = self._reflexes.get(reflex.expect)
            if exist:
                exist += reflex
            else:
                self._reflexes[reflex.expect] = reflex

    def enable(self):
        self._enabled.set()

    def disable(self):
        self._enabled.clear()

    def run(self):
        self._['log']('%s activated' % self._player, 2)
        wrapper = {
            'target': str(self._player),
            'idle': self._player.idle,
            'click': self._player.click,
            'stop': self.stop,
            'enable': self.enable,
            'disable': self.disable,
            'log': self._['log']
        }
        reflexes = self._reflexes.values()
        while not self._exited:
            self._enabled.wait()
            self._player.idle(self._['tick'])
            try:
                wrapper['screen'] = self._player.snap()
                now = time.time()
                if not wrapper['screen']:
                    wrapper['log'](
                        '%s had no screen input' % (wrapper['target']),
                        3
                    )
                    continue
                event = Event(wrapper, self.context)
                for reflex in reflexes:
                    if reflex.do(event):
                        self._activity = now
                        break
                if self._activity + self._['timeout'] < now:
                    event.log('%s timeout' % event.target, 3)
                    snappath = '%s-timeout-%d.png' % (
                        event.target[1:],
                        int(now)
                    )
                    event.screen.save(snappath)
                    event.log(
                        '%s screenshot to %r' % (
                            event.target,
                            snappath
                        ),
                        1
                    )
                    self._activity = now
                self.context.update(event)
            except Exception as e:
                self._['log']('%s %s' % (self._player, e), 3)
        self._['log']('%s clear' % self._player, 2)
