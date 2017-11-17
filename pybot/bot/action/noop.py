# encoding: utf-8

from .action import Action

class Noop(Action):
    def __init__(self, desc):
        super(Noop, self).__init__()
        self.desc = desc

    def do(self, event):
        pass
