# encoding: utf-8

from ... import core
from .base import Base
from .expect import Expect

class Negative(Expect):
    def __init__(self, positive, **spots):
        if not isinstance(positive, Base):
            raise core.EType(positive, Base)
        super(Negative, self).__init__(**spots)
        self._expect = positive
        self.spots.update(positive.spots)

    def __repr__(self):
        return 'Negative(%r)' % self._expect

    def _test(self, event, trace):
        trace2 = []
        matched = self._expect.test(event, trace2)
        trace.append('%r %r' % (self._expect, matched))
        trace.append(trace2)
        return not matched
