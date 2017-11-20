# encoding: utf-8

from .base import Base

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self._reacts = []

    def do(self, event):
        for react in self._reacts:
            react.do(event)

    def then(self, react):
        assert isinstance(react, Base)
        self._reacts.append(react)
        self.timeout += react.timeout
        return self
