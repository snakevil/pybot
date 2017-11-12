# encoding: utf-8

from .base import Base
from .all import All
from .any import Any

class Expect(Base):
    def __and__(self, another):
        return All(self, another)

    def __or__(self, another):
        return Any(self, another)
