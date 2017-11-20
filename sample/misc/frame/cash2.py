# encoding: utf-8

from pybot.bot.expect import Fingerprint
from .bounty import Bounty

class Cash2(Bounty):
    def __init__(self):
        super(Cash2, self).__init__(
            Fingerprint(
                ((405, 284), (450, 329)),
                '00003c3e3e3e1b2c',
                74
            )
        )
