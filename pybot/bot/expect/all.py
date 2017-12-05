# encoding: utf-8

from .base import Base

class All(Base):
    def __init__(self, *expects, **spots):
        super(All, self).__init__(**spots)
        self._expects = []
        for expect in expects:
            if isinstance(expect, All):
                self._expects.extend(expect._expects)
            else:
                self._expects.append(expect)
            self.spots.update(expect.spots)

    def __repr__(self):
        return 'All(%s)' % repr(self._expects)[1:-1]

    def __and__(self, another):
        return type(self)(self, another)

    def __iand__(self, another):
        self._expects.append(another)
        self.spots.update(another.spots)
        return self

    def __or__(self, another):
        return Any(self, another)

    def test(self, event):
        for expect in self._expects:
            if not expect.test(event):
                return False
            self.spots.update(expect.spots)
        return True
