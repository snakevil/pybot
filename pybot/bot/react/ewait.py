# encoding: utf-8

from ... import core

class EWait(core.Error):
    def __init__(self, msecs):
        super(EWait, self).__init__(
            0x3202,
            'Illegal micro-seconds %r.' % msecs,
            msecs = msecs
        )
