# encoding: utf-8

from pybot.bot import expect

class Invite(expect.Fingerprint):
    def __init__(self):
        super(Invite, self).__init__(
            ((65, 137), (111, 183)),
            'ffc180a69088c1c3',
            136,
            ok = ((88, 160), 20),
            cancel = ((28, 160), 20)
        )

    def __str__(self):
        return '收到邀请'
