# encoding: utf-8

from ... import core

class EDepth(core.Error):
    def __init__(self, depth):
        super(EDepth, self).__init__(
            0x1001,
            'Illegal depth %r.' % depth,
            depth = depth
        )
