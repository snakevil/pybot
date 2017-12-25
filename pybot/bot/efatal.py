# encoding: utf-8

from .. import core

class EFatal(core.Error):
    def __init__(self):
        super(EFatal, self).__init__(
            0x3002,
            ''
        )
