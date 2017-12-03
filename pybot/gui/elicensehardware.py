# encoding: utf-8

from .. import core

__all__ = ['ELicenseHardware']

class ELicenseHardware(core.Error):
    def __init__(self, hwaddr):
        super(ELicenseHardware, self).__init__(
            0x4004,
            'LICENSE Hardware dismatched for %s.' % hwaddr.hex().upper(),
            hwaddr = hwaddr
        )
