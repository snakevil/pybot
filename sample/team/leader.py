# encoding: utf-8

from pybot import bot
from .frame import *

class Leader(bot.Competence):
    def __init__(self, total):
        assert total in range(1, 4)
        if 2 == total:
            ready = Ready()
        else:
            ready = Ready3()
        super(Leader, self).__init__([
            bot.Reflex(
                Repeat(),
                bot.react.OK()
            ),
            bot.Reflex(
                Again(),
                bot.react.Spot('check')
            ),
            bot.Reflex(
                ready,
                bot.react.OK()
            )
        ])
