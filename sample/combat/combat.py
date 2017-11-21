# encoding: utf-8

from pybot import bot
from .frame import *

class Combat(bot.Competence):
    def __init__(self):
        super(Combat, self).__init__([
            bot.Reflex(
                Begin(),
                bot.react.OK()
            ),
            bot.Reflex(
                Success(),
                bot.react.OK()
            ),
            bot.Reflex(
                Reward(),
                bot.react.OK().then(
                    bot.react.Wait(500, 1000)
                )
            ),
            bot.Reflex(
                End(),
                bot.react.OK().then(
                    bot.react.Wait(500, 1000)
                )
            ),
            bot.Reflex(
                Manual(),
                bot.react.OK()
            )
        ])
