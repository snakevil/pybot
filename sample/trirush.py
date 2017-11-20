# encoding: utf-8

from pybot import bot
from . import team
from . import combat

class TriRush(bot.Mission):
    def __init__(self):
        super(TriRush, self).__init__('Aby', 'Baal', 'Cain')
        self.co('Aby').on(
            team.Ready3(),
            bot.react.OK()
        ).clone(
            combat.Combat()
        ).co('Baal').clone(
            combat.Combat()
        ).co('Cain').clone(
            combat.Combat()
        )
