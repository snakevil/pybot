# encoding: utf-8

from ... import core

class EGray(core.Error):
    def __init__(self, gray):
        super(EGray, self).__init__(
            0x3105,
            'Illegal gray %r.' % gray,
            gray = gray
        )
