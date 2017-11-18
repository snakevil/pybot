# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Success(Fingerprint):
    def __init__(self):
        super(Success, self).__init__(
            ((257, 84), (413, 137)),
            'a28282aade767464',
            104
        )

    def __str__(self):
        return '战斗胜利'
