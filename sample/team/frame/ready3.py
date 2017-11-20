# encoding: utf-8

from pybot.bot import expect

class Ready3(expect.All):
    def __init__(self):
        region = ((596, 355), (708, 397))
        super(Ready3, self).__init__(
            expect.Fingerprint(
                region,
                '807f7f4d595b7f00',
                91
            ),
            expect.Colors(
                region,
                (645, 0, 0, 0, 904, 0, 3143, 12)
            ),
            expect.Negative(
                expect.Fingerprint(
                    ((628, 271), (688, 331)),
                    'ffa7b2a33880c1e7',
                    114
                )
            ),
            ok = (region, 5),
            cancel = (((89, 355), (201, 397)), 5)
        )

    def __str__(self):
        return '组队就绪'
