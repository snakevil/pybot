# encoding: utf-8

from pybot.bot.expect import Fingerprint

class End(Fingerprint):
    def __init__(self):
        super(End, self).__init__(
            ((297, 370), (477, 394)),
            'cbb3b6f4e86060e0',
            28,
            ok = (((700, 225), (800, 450)), 5)
        )

    def __str__(self):
        return '战斗结束'
