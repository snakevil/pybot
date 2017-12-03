# encoding: utf-8

import time as t

from .. import core

__all__ = ['ELicenseExpired']

class ELicenseExpired(core.Error):
    def __init__(self, time):
        super(ELicenseExpired, self).__init__(
            0x4002,
            'LICENSE Expired due %s.' % t.strftime('%c', t.localtime(time)),
            time = time
        )
