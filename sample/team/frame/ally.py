# encoding: utf-8

from pybot.bot import expect

class Ally(expect.Fingerprint):
    def __init__(self):
        super(Ally, self).__init__(
            ((125, 137), (171, 183)),
            'ffd19cba3e8080c1',
            159,
            ok = ((148, 160), 20),
            once = ((88, 160), 20),
            cancel = ((28, 160), 20)
        )

    def __str__(self):
        return '自动接受'
