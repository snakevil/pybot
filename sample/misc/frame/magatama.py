# encoding: utf-8

from pybot.bot.expect import Fingerprint
from .bounty import Bounty

class Magatama(Bounty):
    def __init__(self):
        super(Magatama, self).__init__(
            Fingerprint(
                ((405, 284), (450, 329)),
                '1c14303be7387b0c',
                103
            )
        )

    def __str__(self):
        return '协作邀请：勾玉'
