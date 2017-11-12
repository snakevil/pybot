# encoding: utf-8

import random
from .action import Action

class Wait(Action):
    def __init__(self, nmsecs, xmsecs = 0):
        assert isinstance(nmsecs, int) and 0 < nmsecs
        assert isinstance(xmsecs, int) and 0 <= xmsecs
        super(Wait, self).__init__()
        if not xmsecs:
            xmsecs = nmsecs
        self.nmsecs = min(nmsecs, xmsecs)
        self.xmsecs = max(nmsecs, xmsecs)

    def apply(self, player, context = {}):
        super(Wait, self).apply(player, context)
        msecs = random.randint(self.nmsecs, self.xmsecs)
        self.log('%d ms' % msecs)
        player.idle(msecs)
        return context
