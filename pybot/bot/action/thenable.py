# encoding: utf-8

from .base import Base

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self.actions = []

    def apply(self, player, context = {}):
        super(Thenable, self).apply(player, context)
        for action in self.actions:
            context = action.apply(player, context)
        return context

    def then(self, action):
        assert isinstance(action, Base)
        self.actions.append(action)
        return self
