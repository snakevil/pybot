# encoding: utf-8

from .. import core

__all__ = ['ELicenseBlob']

class ELicenseBlob(core.Error):
    def __init__(self):
        super(ELicenseBlob, self).__init__(
            0x4005,
            'LICENSE Illegal blob.'
        )
