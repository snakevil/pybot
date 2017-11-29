# encoding: utf-8

from ... import core

class EWin32(core.Error):
    def __init__(self, api):
        super(EWin32, self).__init__(
            0x2003,
            "Win32 API '%s' failure." % api,
            api = api
        )
