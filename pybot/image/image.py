# encoding: utf-8

from .base import Base
from .grayscaled import Grayscaled

class Image(Base):
    def grayscale(self, bit = 8):
        return Grayscaled(self, self.bgrr, bit)
