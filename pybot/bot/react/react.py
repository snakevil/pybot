# encoding: utf-8

from .base import Base
from .thenable import Thenable

class React(Base):
    def then(self, next):
        return Thenable().then(self).then(next)
