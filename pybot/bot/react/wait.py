# encoding: utf-8

import random
from .react import React
from .ewait import EWait

class Wait(React):
    def __init__(self, nmsecs, xmsecs = 0):
        if not isinstance(nmsecs, int) or 0 >= nmsecs:
            raise EWait(nmsecs)
        if not isinstance(xmsecs, int) or 0 > xmsecs:
            raise EWait(xmsecs)
        super(Wait, self).__init__()
        if not xmsecs:
            xmsecs = nmsecs
        self._nmsecs = min(nmsecs, xmsecs)
        self._xmsecs = max(nmsecs, xmsecs)
        self.timeout = self._xmsecs / 1000

    def do(self, event):
        msecs = random.randint(self._nmsecs, self._xmsecs)
        event.idle(msecs)
