# encoding: utf-8

from pybot import bot
from .frame import *

class Bounty(bot.Competence):
    def __init__(self):
        super(Bounty, self).__init__([
            bot.Reflex(
                Coin3(),
                bot.react.OK()
            ),
            bot.Reflex(
                Coin2(),
                bot.react.Cancel()
            ),
            bot.Reflex(
                Sushi(),
                bot.react.OK()
            ),
            bot.Reflex(
                Magatama(),
                bot.react.OK()
            ),
            bot.Reflex(
                Orochi(),
                bot.react.OK()
            )
        ])
