# encoding: utf-8

from pybot import bot
from .frame import *

class Member(bot.Competence):
    def __init__(self):
        super(Member, self).__init__([
            bot.Reflex(
                Ally2(),
                bot.react.OK()
            ),
            bot.Reflex(
                Ally(),
                bot.react.OK()
            ),
            bot.Reflex(
                Invite(),
                bot.react.OK()
            )
        ])
