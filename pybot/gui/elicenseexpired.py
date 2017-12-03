# encoding: utf-8

import time as t

from .. import core

__all__ = ['ELicenseExpired']

class ELicenseExpired(core.Error):
    def __init__(self):
        super(ELicenseExpired, self, time).__init__(
            0x4002,
            'Expired due %s.' % t.strftime('%c', time),
            time = time
        )
