# encoding: utf-8

from pybot import bot
from ..team import Ready
from . import frame

class DualRush(bot.Script):
    def __init__(self):
        super(DualRush, self).__init__('leader', 'member')
        self.role('leader').on(
            Ready(),
            bot.action.OK()
        ).on(
            frame.Begin(),
            bot.action.OK()
        ).on(
            frame.Success(),
            bot.action.OK()
        ).on(
            frame.Reward(),
            bot.action.OK().then(
                bot.action.Wait(1000, 2000)
            )
        ).on(
            frame.End(),
            bot.action.OK().then(
                bot.action.Wait(1000, 2000)
            )
        ).role('member').on(
            frame.Success(),
            bot.action.OK()
        ).on(
            frame.Reward(),
            bot.action.OK().then(
                bot.action.Wait(1000, 2000)
            )
        ).on(
            frame.End(),
            bot.action.OK().then(
                bot.action.Wait(1000, 2000)
            )
        )
