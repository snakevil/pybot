# encoding: utf-8

from .base import Base

class All(Base):
    def __init__(self, *expects):
        super(All, self).__init__()
        self.expects = []
        for expect in expects:
            if isinstance(expect, All):
                self.expects.extend(expect.expects)
            else:
                self.expects.append(expect)

    def __and__(self, another):
        return type(self)(self, another)

    def __iand__(self, another):
        self.expects.append(another)
        return self

    def __or__(self, another):
        return Any(self, another)

    def test(self, event):
        for expect in self.expects:
            if not expect.test(event):
                return False
        return True
