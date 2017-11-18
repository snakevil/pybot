# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Begin(Fingerprint):
    def __init__(self):
        super(Begin, self).__init__(
            ((684, 400), (778, 434)),
            '0102c1f33e9fcfef',
            143,
            ok = ((730, 345), 48),
            cancel = ((23, 21), 12)
        )

    def __str__(self):
        return '战斗准备'
