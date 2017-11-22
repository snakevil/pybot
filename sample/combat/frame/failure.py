# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Failure(Fingerprint):
    def __init__(self):
        super(Failure, self).__init__(
            ((240, 79), (300, 109)),
            '515151717131353a',
            102,
            ok = (((600, 225), (800, 450)), 5)
        )

    def __str__(self):
        return '战斗失败'
