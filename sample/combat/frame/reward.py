# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Reward(Fingerprint):
    def __init__(self):
        super(Reward, self).__init__(
            ((336, 222), (466, 304)),
            '8ebdff3f40410000',
            54,
            ok = (((600, 225), (800, 450)), 5)
        )

    def __str__(self):
        return '战斗奖励'
