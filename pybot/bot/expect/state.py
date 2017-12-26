# encoding: utf-8

from .expect import Expect


class State(Expect):
    """docstring for State"""
    def __init__(self, field, value):
        super(State, self).__init__()
        self._field = field
        self._value = value

    def __repr__(self):
        return 'State(%r, %r)' % (self._field, self._value)

    def _test(self, event, trace):
        value = event.get('__state_%s__' % self._field)
        trace.append('= %r' % value)
        return value == self._value
