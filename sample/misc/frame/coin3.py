# encoding: utf-8

from pybot.bot.expect import Fingerprint
from .bounty import Bounty

class Coin3(Bounty):
    def __init__(self):
        super(Coin3, self).__init__(
            Fingerprint(
                ((405, 284), (450, 329)),
                '00003c3e3e3e1b0c',
                81
            )
        )

    def __str__(self):
        return '协作邀请：3W金'
