# encoding: utf-8

from ... import core

class ETimeout(core.Error):
    def __init__(self, timeout):
        super(ETimeout, self).__init__(
            0x3201,
            'Illegal timeout %r.' % timeout,
            timeout = timeout
        )
