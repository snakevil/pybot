# encoding: utf-8

from pybot import bot
from . import team
from . import combat
from . import misc

class TriRush(bot.Mission):
    def __init__(self):
        super(TriRush, self).__init__('Aby', 'Baal', 'Cain')
        self.co('Aby').clone(
            team.Leader3()
        ).clone(
            combat.Combat()
        ).clone(
            misc.Bounty()
        ).co('Baal').clone(
            team.Member()
        ).clone(
            combat.Combat()
        ).clone(
            misc.Bounty()
        ).co('Cain').clone(
            team.Member()
        ).clone(
            combat.Combat()
        ).clone(
            misc.Bounty()
        )
