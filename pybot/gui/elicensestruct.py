# encoding: utf-8

from .. import core

__all__ = ['ELicenseStruct']

class ELicenseStruct(core.Error):
    def __init__(self):
        super(ELicenseStruct, self).__init__(
            0x4005,
            'LICENSE bad structure.'
        )
