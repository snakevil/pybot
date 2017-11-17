# encoding: utf-8

import time
from .action import Action

class Grab(Action):
    def invoke(self, player, context):
        image = player.snap()
        assert image
        filepath = '%s-%d.png' % (player, int(time.time()))
        image.save(filepath)
