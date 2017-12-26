# encoding: utf-8

from .react import React

class Cast(React):
    def __init__(self, spell):
        super(Cast, self).__init__(1)
        self._spell = spell

    def __repr__(self):
        return 'Cast(%r)' % self._spell

    def do(self, event, trace):
        self._spell(event)
