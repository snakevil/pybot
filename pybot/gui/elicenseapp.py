# encoding: utf-8

from .. import core

__all__ = ['ELicenseApp']

class ELicenseApp(core.Error):
    def __init__(self):
        super(ELicenseApp, self).__init__(
            0x4001,
            'App dismatched.'
        )
