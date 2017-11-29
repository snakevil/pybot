# encoding: utf-8

from ... import core

class EChunkBroken(core.Error):
    def __init__(self, chunk):
        super(EChunkBroken, self).__init__(
            0x1004,
            'Chunk %r broken.' % chunk,
            chunk = chunk
        )
