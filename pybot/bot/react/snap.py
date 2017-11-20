# encoding: utf-8

import time
from .react import React

class Snap(React):
    def do(self, event):
        event.screen.save('%s-%d.png' % (event.target[1:], int(time.time())))
