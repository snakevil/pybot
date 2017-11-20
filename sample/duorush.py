# encoding: utf-8

from pybot import bot
from . import team
from . import combat

class DuoRush(bot.Mission):
    def __init__(self):
        super(DuoRush, self).__init__('Aalto', 'Bella')
        self.co('Aalto').on(
            team.Ready(),
            bot.react.OK()
        ).clone(
            combat.Combat()
        ).co('Bella').clone(
            combat.Combat()
        )
