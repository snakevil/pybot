# encoding: utf-8

import pybot.bot as bot

__all__ = ['Collapsed']

class Collapsed(bot.Fingerprint):
    def __init__(self):
        region = ((740, 377), (774, 411))
        super().__init__(
            region,
            '5e3f0f0f8120e0e0',
            88,
            ok = (region, 4)
        )

    def __str__(self):
        return '展开卷轴'
