# encoding: utf-8

from ... import core

class EPixels(core.Error):
    def __init__(self):
        super(EPixels, self).__init__(0x3103, 'Pixels missing.')
