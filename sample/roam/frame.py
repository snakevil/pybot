# encoding: utf-8

from pybot.bot import expect

class Collapsed(expect.Fingerprint):
    def __init__(self):
        super(Collapsed, self).__init__(
            ((740, 377), (774, 411)),
            '5e3f0f0f8120e0e0',
            88
        )

class Normal(expect.Fingerprint):
    def __init__(self):
        super(Normal, self).__init__(
            ((126, 361), (202, 437)),
            '001c3e3e3e7c3814',
            103
        )

class Guild(expect.Fingerprint):
    def __init__(self):
        super(Guild, self).__init__(
            ((654, 347), (722, 415)),
            'fec800087f3e0c14',
            75
        )
