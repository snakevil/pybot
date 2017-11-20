# encoding: utf-8

from pybot import bot
from .frame import *

class Leader(bot.Competence):
    def __init__(self):
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
                Ready(),
                bot.react.OK()
            )
        ])
