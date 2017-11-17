# encoding: utf-8

import threading
from ..player import Window as Player
from .event import Event
from .trigger import Trigger

class Bot(threading.Thread):
    def __init__(self, player, context):
        assert isinstance(player, Player)
        assert isinstance(context, dict)
        self.player = player
        self.context = context
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
        prototype = {
            'idle': self.player.idle,
            'click': self.player.click,
            'stop': self.stop,
            'enable': self.enable,
            'disable': self.disable
        }
        while not self.exited:
            self.active.wait()
            self.player.idle(100)
            prototype['screen'] = self.player.snap()
            event = Event(prototype, self.context)
            for trigger in self.triggers:
                if trigger.fire(event):
                    break
            self.context.update(event)
