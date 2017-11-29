# encoding: utf-8

from ... import core

class EChunkMissing(core.Error):
    def __init__(self, chunk):
        super(EChunkMissing, self).__init__(
            0x1002,
            'Chunk %r missing.' % chunk,
            chunk = chunk
        )
