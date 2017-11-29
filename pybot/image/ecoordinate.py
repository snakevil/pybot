# encoding: utf-8

from .. import core

class ECoordinate(core.Error):
    def __init__(self, x, y):
        super(ECoordinate, self).__init__(
            0x1101,
            'Illegal coordinate (%r, %r).' % (x, y),
            x = x,
            y = y
        )
