# encoding: utf-8

from .react import React

class Log(React):
    def __init__(self, message):
        super(Log, self).__init__()
        self._msg = message

    def __repr__(self):
        return 'Log(%r)' % self._msg

    def do(self, event, trace):
        event.log('%s logged %r' % (event.target, self._msg), 3)
