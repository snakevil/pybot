# encoding: utf-8

from pybot import bot
from ..team import Ready
from . import frame

class DualRush(bot.Script):
    def __init__(self):
        super(DualRush, self).__init__('leader', 'member')
        self.role('leader').on(
            Ready(),
            bot.action.Fire(
                ((596, 355), (708, 397)),
                4
            )
        ).on(
            frame.Begin(),
            bot.action.Fire(
                (730, 346),
                48
            )
        ).on(
            frame.Success(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            frame.Reward(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            frame.End(),
            bot.action.Fire(
                ((672, 32), (800, 450)),
                10
            )
        ).role('member').on(
            frame.Success(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            frame.Reward(),
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            )
        ).on(
            frame.End(),
            bot.action.Fire(
                ((672, 32), (800, 450)),
                10
            )
        )
