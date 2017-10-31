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

    def hold(self, msecs, extra = 0):
        self.steps.append(action.Wait(msecs, extra))
        return self

    def fire(self, pos, spread = 0):
        if type(pos) == int:
            pos = (pos, spread)
            spread = 0
        self.steps.append(action.Fire(pos, spread))
        return self

    def plan(self):
        pass

    def apply(self, player, state = {}):
        if not self._plan:
            self._plan = True
            if 1 > len(self.steps):
                self.plan()
        self.log(player, self.title)
        for step in self.steps:
            state = step.apply(player, state)
        self.log(player, 'COMPLETED')
        return state

__all__ = ['Operation']
