# encoding: utf-8

from pybot.bot import expect

class Bounty(expect.All):
    def __init__(self, icon):
        assert isinstance(icon, expect.Base)
        super(Bounty, self).__init__(
            expect.Fingerprint(
                ((351, 99), (477, 121)),
                'dfcccd8c2ca8ecbd',
                109
            ),
            icon,
            ok = (((510, 241), (634, 283)), 5),
            cancel = (((510, 304), (634, 346)), 5)
        )
