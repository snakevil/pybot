# encoding: utf-8

from pybot.player import Window

class PC(Window):
    __pattern = '^阴阳师-网易游戏$'

    @classmethod
    def first(cls):
        return super(PC, cls).first(cls.__pattern)

    @classmethod
    def all(cls):
        return super(PC, cls).all(cls.__pattern)
