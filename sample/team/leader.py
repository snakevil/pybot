# encoding: utf-8

from pybot import bot
from .frame import *

class Leader(bot.Competence):
    def __init__(self, total):
        if 2 == total:
            self._total = '双'
            ready = Ready()
        else:
            self._total = '仨'
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

    def __str__(self):
        return '%s人队伍组织能力' % self._total
