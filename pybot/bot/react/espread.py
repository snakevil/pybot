# encoding: utf-8

from ... import core

class ESpread(core.Error):
    def __init__(self, spread):
        super(ESpread, self).__init__(
            0x3203,
            'Illegal spread %r.' % spread,
            spread = spread
        )
