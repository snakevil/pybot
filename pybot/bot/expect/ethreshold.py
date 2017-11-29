# encoding: utf-8

from ... import core

class EThreshold(core.Error):
    def __init__(self, threshold):
        super(EThreshold, self).__init__(
            0x3101,
            'Illegal threshold %r.' % threshold,
            threshold = threshold
        )
