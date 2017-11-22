# encoding: utf-8

from pybot.bot import expect

class Ally2(expect.Fingerprint):
    def __init__(self):
        super(Ally2, self).__init__(
            ((306, 173), (368, 189)),
            'ffeeaa2a2a130a3b',
            139,
            ok = (((418, 250), (530, 292)), 5),
            cancel = (((270, 250), (382, 292)), 5)
        )

    def __str__(self):
        return '确认自动'
