# encoding: utf-8

from pybot.bot import expect

class Orochi(expect.Fingerprint):
    def __init__(self):
        super(Orochi, self).__init__(
            ((219, 132), (281, 192)),
            'c36de1cfc1e1a08a',
            95,
            ok = ((25, 163), 18)
        )

    def __str__(self):
        return '发现真蛇'
