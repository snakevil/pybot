# encoding: utf-8

from ... import core

class EChunkDuplicated(core.Error):
    def __init__(self, chunk):
        super(EChunkDuplicated, self).__init__(
            0x1003,
            'Chunk %r duplicated.' % chunk,
            chunk = chunk
        )
