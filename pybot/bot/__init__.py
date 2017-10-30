# encoding: utf-8

from . import action

class Operation(action.Base):
    def __init__(self, title):
        self.title = title
        self.steps = []
        self._plan = False

    def locate(self, *references):
        self.steps.append(action.Locate(*references))
        return self

    def hold(self, msecs):
        self.steps.append(action.Hold(msecs))
        return self

    def fire(self, x, y, spread = 0):
        self.steps.append(action.Fire())
        return self

    def plan(self):
        pass

    def apply(self, player, state = {}):
        if not self._plan:
            self._plan = True
            if 1 > len(self.steps):
                self.plan()
        for step in self.steps:
            state = step.apply(player, state)
        return state

__all__ = ['Operation']
