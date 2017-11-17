# encoding: utf-8

from .base import Base

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self.actions = []

    def invoke(self, player, context):
        for action in self.actions:
            action.invoke(player, context)

    def then(self, action):
        assert isinstance(action, Base)
        self.actions.append(action)
        self.timeout += action.timeout
        return self
