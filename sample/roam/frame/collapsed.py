# encoding: utf-8

from pybot.bot.expect import Fingerprint

class Collapsed(Fingerprint):
    def __init__(self):
        super(Collapsed, self).__init__(
            ((740, 377), (774, 411)),
            '5e3f0f0f8120e0e0',
            88
        )

    def __str__(self):
        return '收起的菜单'
