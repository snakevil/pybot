# encoding: utf-8

from ... import core
from .base import Base

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self._reacts = []

    def do(self, event):
        for react in self._reacts:
            react.do(event)

    def then(self, react):
        if not isinstance(react, Base):
            raise core.EType(react, Base)
        self._reacts.append(react)
        self.timeout += react.timeout
        return self
