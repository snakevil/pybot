# encoding: utf-8

from ... import core
from .etimeout import ETimeout

class Base(object):
    def __init__(self, timeout = .1):
        if not isinstance(timeout, float) \
                and not isinstance(timeout, int) \
                or 0 >= timeout:
            raise ETimeout(timeout)
        self.timeout = timeout

    def __repr__(self):
        return '%s()' % type(self).__name__

    def do(self, event, trace):
        raise core.ETodo('bot.react.base.do')
