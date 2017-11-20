# encoding: utf-8

from .react import React

class Log(React):
    def __init__(self, message):
        super(Log, self).__init__()
        self._msg = message

    def do(self, event):
        event.log(self._msg, 1)
