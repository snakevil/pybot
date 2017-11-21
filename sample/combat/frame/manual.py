# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Manual(Fingerprint):
    def __init__(self):
        super(Manual, self).__init__(
            ((18, 403), (56, 423)),
            'c0a0a4a360a7a3a1',
            95,
            ok = ((38, 414), 25)
        )

    def __str__(self):
        return '手动操作'
