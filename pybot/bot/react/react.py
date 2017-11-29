# encoding: utf-8

from ... import core
from .base import Base
from .thenable import Thenable

class React(Base):
    def __add__(self, other):
        return self.then(other)

    def __radd__(self, other):
        raise core.EType(other, type(self))

    def then(self, next):
        if not isinstance(next, Base):
            raise core.EType(next, type(self))
        return Thenable().then(self).then(next)
