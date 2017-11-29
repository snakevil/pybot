# encoding: utf-8

from ... import core
from .base import Base

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self._reacts = []

    def __add__(self, other):
        if not isinstance(other, Base):
            raise core.EType(other, type(self))
        ret = Thenable()
        for react in self._reacts:
            ret.then(react)
        return ret.then(other)

    def __radd__(self, other):
        raise core.EType(other, type(self))

    def __iadd__(self, other):
        if not isinstance(other, Base):
            raise core.EType(other, Base)
        self._reacts.append(other)
        self.timeout += other.timeout

    def do(self, event):
        for react in self._reacts:
            react.do(event)

    def then(self, react):
        self += react
        return self
