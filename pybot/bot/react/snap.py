# encoding: utf-8

import time
from .react import React

class Snap(React):
    def do(self, event, trace):
        event.screen.save(
            '%s-snap-%d.png' % (
                event.target[1:],
                time.strftime(
                    '%y%m%d%H%M%S',
                    time.localtime(event.screen.timestamp)
                )
            )
        )
