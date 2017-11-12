# encoding: utf-8

from .base import Base
from .thenable import Thenable

class Action(Base):
    def then(self, action):
        return Thenable().then(self).then(action)
