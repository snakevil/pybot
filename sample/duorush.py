# encoding: utf-8

from pybot import bot
from . import team
from . import combat
from . import misc

class DuoRush(bot.Mission):
    def __init__(self):
        super(DuoRush, self).__init__('Aalto', 'Bella')
        self.co('Aalto').clone(
            team.Leader()
        ).clone(
            combat.Combat()
        ).clone(
            misc.Bounty()
        ).co('Bella').clone(
            team.Member()
        ).clone(
            combat.Combat()
        ).clone(
            misc.Bounty()
        )
