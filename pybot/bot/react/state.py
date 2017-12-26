# encoding: utf-8

from .react import React

class State(React):
    def __init__(self, **fields):
        super(State, self).__init__()
        self._fields = fields

    def __repr__(self):
        return 'State(%s)' % ', '.join([
            '%s = %r' % (k, v) for k, v in self._fields.items()
        ])

    def do(self, event, trace):
        for k, v in self._fields.items():
            event['__state_%s__' % k] = v
