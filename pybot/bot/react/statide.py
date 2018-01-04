# encoding: utf-8

from ... import player
from .react import React
from .espread import ESpread
from .eregion import ERegion

class Statide(React):
    def __init__(self, src, dest):
        super(Statide, self).__init__(1)
        self._from = src
        self._to = dest

    def __repr__(self):
        return 'Statide(%r, %r)' % (self._from, self._to)

    def do(self, event, trace):
        src = event.get('__state_spot_%s__' % self._from)
        dest = event.get('__state_spot_%s__' % self._to)
        if src and dest:
            trace.append('= %r -> %r' % (src, dest))
            event.drag(src, dest)
        else:
            trace.append('= None -> None')
            event['__fatal__'] = True
