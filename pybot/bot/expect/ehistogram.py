# encoding: utf-8

from ... import core

class EHistogram(core.Error):
    def __init__(self, histogram):
        super(EHistogram, self).__init__(
            0x3102,
            'Illegal histogram %r.' % histogram,
            histogram = histogram
        )
