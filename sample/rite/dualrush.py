# encoding: utf-8

from pybot import bot
from ..spell import combat

class DualRush(bot.Rite):
    def __init__(self, duration = 30000):
        super(DualRush, self).__init__(
            'leader', 'member'
        )
        self.role('leader').cast(
            combat.Ready()
        ).idle(3000).cast(
            combat.Begin()
        ).idle(duration).cast(
            combat.Loot()
        ).role('member').cast(
            combat.MemberLoot()
        ).idle(2000).cast(
            combat.Over()
        ).role('leader').cast(
            combat.Over()
        )
