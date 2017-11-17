# encoding: utf-8

from .base import Base

class Thenable(Base):
    def __init__(self):
        super(Thenable, self).__init__()
        self.actions = []

    def do(self, event):
        for action in self.actions:
            action.do(event)

    def then(self, action):
        assert isinstance(action, Base)
        self.actions.append(action)
        self.timeout += action.timeout
        return self
