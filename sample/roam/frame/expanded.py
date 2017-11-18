# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Normal(Fingerprint):
    def __init__(self):
        super(Normal, self).__init__(
            ((126, 361), (202, 437)),
            '001c3e3e3e7c3814',
            103
        )

    def __str__(self):
        return '展开的菜单'
