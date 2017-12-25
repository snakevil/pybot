# encoding: utf-8

from ... import player
from .react import React

class Halt(React):
    def __init__(self):
        super(Halt, self).__init__(.1)

    def __repr__(self):
        return 'Halt()'

    def do(self, event):
        event['__fatal__'] = True
