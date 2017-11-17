# encoding: utf-8

import threading
from ..player import Window as Player
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
        while not self.exited:
            self.active.wait()
            self.player.idle(100)
            for trigger in self.triggers:
                if trigger.fire(self.player, self.context):
                    break
