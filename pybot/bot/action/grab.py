# encoding: utf-8

import time
from .action import Action

class Grab(Action):
    def apply(self, player, context = {}):
        super(Grab, self).apply(player, context)
        image = player.snap()
        if image:
            filepath = '%s-%d.png' % (player, int(time.time()))
            image.save(filepath)
            self.log(filepath)
        return context
