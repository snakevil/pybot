# encoding: utf-8

import threading
from ..player import Window as Player
from .event import Event
from .trigger import Trigger

class Bot(threading.Thread):
    def __init__(self, player, context, tick):
        super(Bot, self).__init__()
        self.player = player
        self.context = context
        self.tick = tick
        self.active = threading.Event()
        self.exited = False
        self.triggers = []
        self.enable()

    def stop(self):
        self.exited = True

    def handle(self, trigger):
        assert isinstance(trigger, Trigger)
        self.triggers.append(trigger)

    def enable(self):
        self.active.set()

    def disable(self):
        self.active.clear()

    def run(self):
        wrapper = {
            'idle': self.player.idle,
            'click': self.player.click,
            'stop': self.stop,
            'enable': self.enable,
            'disable': self.disable
        }
        while not self.exited:
            self.active.wait()
            self.player.idle(self.tick)
            wrapper['screen'] = self.player.snap()
            event = Event(wrapper, self.context)
            for trigger in self.triggers:
                if trigger.fire(event):
                    break
            self.context.update(event)
