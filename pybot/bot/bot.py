# encoding: utf-8

import threading
import time

from .. import core

from .event import Event

class Bot(threading.Thread, core.Firable):
    def __init__(self, player, context, **config):
        super(Bot, self).__init__()
        core.Firable.__init__(self)
        self.player = player
        self._ = config
        self.context = context
        self._enabled = threading.Event()
        self._exited = False
        self._activity = time.time()
        self._reflexes = {}
        self.enable()

    def stop(self):
        if not self._exited:
            self.fire('log', '%s cleaning...' % self.player, 1)
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
        self.fire('log', '%s activated' % self.player, 2)
        wrapper = {
            'target': str(self.player),
            'idle': self.player.idle,
            'click': self.player.click,
            'drag': self.player.drag,
            'stop': self.stop,
            'enable': self.enable,
            'disable': self.disable,
            'log': lambda *args: self.fire('log', *args)
        }
        reflexes = self._reflexes.values()
        while not self._exited:
            self._enabled.wait()
            self.player.idle(self._['tick'])
            try:
                wrapper['screen'] = self.player.snap()
                now = wrapper['time'] = time.time()
                if not wrapper['screen']:
                    self.fire(
                        'log',
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
                    self.fire('log', '%s timeout' % event.target, 3)
                    snappath = '%s-timeout-%d.png' % (
                        event.target[1:],
                        int(now)
                    )
                    event.screen.save(snappath)
                    self.fire(
                        'log',
                        '%s screenshot to %r' % (event.target, snappath),
                        1
                    )
                    self._activity = now
                self.context.update(event)
            except Exception as e:
                self._exited = True
                self.fire('log', '%s broken' % self.player, 4)
                self.fire('error', self)
                return
        self.fire('log', '%s clear' % self.player, 2)
