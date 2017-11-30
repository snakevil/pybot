# encoding: utf-8

from ... import core
from .base import Base

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self._reacts = []

    def __repr__(self):
        length = len(self._reacts)
        if not length:
            return super(Thenable, self).__repr__()
        return repr(self._reacts[0]) \
            + ''.join([
                '.then(%r)' % self._reacts[i] for i in range(1, length)
            ])

    def __add__(self, other):
        ret = Thenable()
        ret._reacts.extend(self._reacts)
        ret.timeout = self.timeout
        return ret.then(other)

    def __radd__(self, other):
        raise core.EType(other, type(self))

    def __iadd__(self, other):
        return self.then(other)

    def do(self, event):
        for react in self._reacts:
            react.do(event)

    def then(self, next):
        if not isinstance(next, Base):
            raise core.EType(next, Base)
        if isinstance(next, Thenable):
            self._reacts.extend(next._reacts)
        else:
            self._reacts.append(next)
        self.timeout += next.timeout
        return self
