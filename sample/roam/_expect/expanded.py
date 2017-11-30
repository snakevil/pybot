# encoding: utf-8

import pybot.bot as bot

__all__ = ['Expanded']

class Expanded(Fingerprint):
    def __init__(self):
        region = ((126, 361), (202, 437))
        super().__init__(
            region,
            '001c3e3e3e7c3814',
            103,
            ok = (((740, 377), (774, 411)), 4),
            gallery = (((38, 361), (114, 437)), 4),
            team = (region, 4),
            guild = (((214, 361), (290, 437)), 4),
            store = (((302, 361), (378, 437)), 4),
            goals = (((390, 361), (466, 437)), 4),
            contact = (((478, 361), (554, 437)), 4),
            master = (((566, 361), (642, 437)), 4),
            cards = (((654, 361), (730, 437)), 4)
        )

    def __str__(self):
        return '选择功能'
