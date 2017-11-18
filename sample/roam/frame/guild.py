# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Guild(Fingerprint):
    def __init__(self):
        super(Guild, self).__init__(
            ((654, 347), (722, 415)),
            'fec800087f3e0c14',
            75
        )

    def __str__(self):
        return '阴阳寮'
