# encoding: utf-8

from pybot import bot
from . import team
from . import combat
from . import misc

class MultiRush(bot.Mission):
    def __init__(self, local, total):
        assert local in range(1, 4)
        if total < local:
            total = local
        self.codes = ['Andy']
        if 1 < local:
            self.codes.append('Baal')
        if 2 < local:
            self.codes.append('Cain')
        super(MultiRush, self).__init__(*self.codes)
        self.co(self.codes[0]).clone(
            team.Leader(total)
        ).clone(
            combat.Combat()
        ).clone(
            misc.Bounty()
        )
        for i in range(1, local):
            self.co(self.codes[i]).clone(
                team.Member()
            ).clone(
                combat.Combat()
            ).clone(
                misc.Bounty()
            )
