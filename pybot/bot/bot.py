# encoding: utf-8

import threading
from .event import Event

class Bot(threading.Thread):
    def __init__(self, player, context, tick, log):
        super(Bot, self).__init__()
        self._ = {
            'player': player,
            'tick': tick,
            'log': log
        }
        self.context = context
        self._active = threading.Event()
        self._exited = False
        self._triggers = []
        self.enable()

    def stop(self):
        self._['log']('%s cleaning...' % self._['player'], 0)
        self._exited = True

    def handle(self, trigger):
        self._triggers.append(trigger)

    def enable(self):
        self._active.set()

    def disable(self):
        self._active.clear()

    def run(self):
        self._['log']('%s ready' % self._['player'], 0)
        wrapper = {
            'idle': self._['player'].idle,
            'click': self._['player'].click,
            'stop': self.stop,
            'enable': self.enable,
            'disable': self.disable,
            'log': self._['log']
        }
        while not self._exited:
            self._active.wait()
            self._['player'].idle(self._['tick'])
            wrapper['screen'] = self._['player'].snap()
            event = Event(wrapper, self.context)
            for trigger in self._triggers:
                if trigger.fire(event):
                    break
            self.context.update(event)
        self._['log']('%s gone' % self._['player'], 0)
