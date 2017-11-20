# encoding: utf-8

from pybot.bot.expect import Fingerprint
from .bounty import Bounty

class Sushi(Bounty):
    def __init__(self):
        super(Sushi, self).__init__(
            Fingerprint(
                ((405, 284), (450, 329)),
                '3e1c3ab9cf09631c',
                93
            )
        )
