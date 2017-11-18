# encoding: utf-8

from pybot import bot
from . import expect

class DualRush(bot.Script):
    def __init__(self):
        super(DualRush, self).__init__('leader', 'member')
        self.role('leader').on(
            expect.TeamReady(),
            bot.action.Fire(
                ((596, 355), (708, 397)),
                4
            )
        ).on(
            expect.Prepare(),
            bot.action.Fire(
                (730, 346),
                48
            )
        ).on(
            expect.Success(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            expect.Reward(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            expect.End(),
            bot.action.Fire(
                ((672, 32), (800, 450)),
                10
            )
        ).role('member').on(
            expect.Success(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            expect.Reward(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            expect.End(),
            bot.action.Fire(
                ((672, 32), (800, 450)),
                10
            )
        )
