# encoding: utf-8

import time
from .react import React

class Snap(React):
    def do(self, event):
        assert event.screen
        event.screen.save('%s-%d.png' % (event.target, int(time.time())))
