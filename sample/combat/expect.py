# encoding: utf-8

from pybot.bot import expect

class TeamReady(expect.All):
    def __init__(self):
        region = ((596, 355), (708, 397))
        super(TeamReady, self).__init__([
            expect.Fingerprint(
                region,
                '807f7f4d595b7f00',
                91
            ),
            expect.Colors(
                region,
                (((645, 0), (0, 0)), ((904, 0), (3143, 12)))
            )
        ])

class Prepare(expect.Fingerprint):
    def __init__(self):
        super(Prepare, self).__init__(
            ((684, 400), (778, 434)),
            '0102c1f33e9fcfef',
            143
        )

class Success(expect.Fingerprint):
    def __init__(self):
        super(Success, self).__init__(
            ((257, 84), (413, 137)),
            'a28282aade767464',
            104
        )

class Reward(expect.Fingerprint):
    def __init__(self):
        super(Reward, self).__init__(
            ((336, 222), (466, 304)),
            '8ebdff3f40410000',
            54
        )

class End(expect.Fingerprint):
    def __init__(self):
        super(End, self).__init__(
            ((297, 370), (477, 394)),
            'cbb3b6f4e86060e0',
            28
        )
