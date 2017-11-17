# encoding: utf-8

import time
from .action import Action

class Grab(Action):
    def do(self, event):
        assert event.screen
        filepath = '%s-%d.png' % (player, int(time.time()))
        event.screen.save(filepath)
