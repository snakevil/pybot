# encoding: utf-8

from ... import core

class EMinimized(core.Error):
    def __init__(self):
        super(EMinimized, self).__init__(0x2002, 'Window minimized.')
