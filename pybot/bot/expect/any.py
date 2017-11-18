# encoding: utf-8

from .base import Base

class Any(Base):
    def __init__(self, *expects):
        self.expects = []
        for expect in expects:
            if isinstance(expect, All):
                self.expects.extend(expect.expects)
            else:
                self.expects.append(expect)

    def __and__(self, another):
        return All(self, another)

    def __or__(self, another):
        return type(self)(self, another)

    def __ior__(self, another):
        self.expects.append(another)
        return self

    def test(self, event):
        for expect in self.expects:
            if expect.test(event):
                return True
        return False
