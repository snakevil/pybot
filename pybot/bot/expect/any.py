# encoding: utf-8

from .base import Base

class Any(Base):
    def __init__(self, *expects, **spots):
        super(Any, self).__init__(**spots)
        self._spots = self.spots.copy()
        self._expects = []
        for expect in expects:
            if isinstance(expect, Any):
                self._expects.extend(expect._expects)
            else:
                self._expects.append(expect)

    def __repr__(self):
        return 'Any(%s)' % repr(self._expects)[1:-1]

    def __and__(self, another):
        return All(self, another)

    def __or__(self, another):
        return type(self)(self, another)

    def __ior__(self, another):
        self._expects.append(another)
        return self

    def _test(self, event, trace):
        self.spots = self._spots.copy()
        for expect in self._expects:
            trace2 = []
            matched = expect.test(event)
            trace.append('%r %r' % (expect, matched))
            trace.append(trace2)
            if matched:
                self.spots.update(expect.spots)
                return True
        return False
