# encoding: utf-8

from ... import core

class EPadding(core.Error):
    def __init__(self, padding):
        super(EPadding, self).__init__(
            0x2001,
            "Illegal padding '%s'." % padding,
            padding = padding
        )
