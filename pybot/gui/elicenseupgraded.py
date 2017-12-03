# encoding: utf-8

from .. import core

__all__ = ['ELicenseUpgraded']

class ELicenseUpgraded(core.Error):
    def __init__(self, version):
        super(ELicenseUpgraded, self).__init__(
            0x4003,
            'LICENSE Major version restricted to %d.' % version,
            version = version
        )
