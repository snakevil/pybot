# encoding: utf-8

from ... import core

class EFingerprint(core.Error):
    def __init__(self, fingerprint):
        super(EFingerprint, self).__init__(
            0x3104,
            'Illegal fingerprint %r.' % fingerprint,
            fingerprint = fingerprint
        )
