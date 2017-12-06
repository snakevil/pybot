# encoding: utf-8

from ... import core

class ERegion(core.Error):
    def __init__(self, region):
        super(ERegion, self).__init__(
            0x3204,
            'Illegal region %r.' % region,
            region = region
        )
