# encoding: utf-8

from .. import core

__all__ = ['ELicenseUpgraded']

class ELicenseUpgraded(core.Error):
    def __init__(self):
        super(ELicenseUpgraded, self, version).__init__(
            0x4003,
            'Major version restricted to %d.' % version,
            version = version
        )
