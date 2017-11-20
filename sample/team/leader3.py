# encoding: utf-8

from pybot import bot
from .frame import *

class Leader3(bot.Competence):
    def __init__(self):
        super(Leader3, self).__init__([
            bot.Reflex(
                Repeat(),
                bot.react.OK()
            ),
            bot.Reflex(
                Again(),
                bot.react.Spot('check')
            ),
            bot.Reflex(
                Ready3(),
                bot.react.OK()
            )
        ])
