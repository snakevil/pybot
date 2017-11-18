# encoding: utf-8

from pybot.bot import expect

class Ready(expect.All):
    def __init__(self):
        region = ((596, 355), (708, 397))
        super(Ready, self).__init__([
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

    def __str__(self):
        return '组队就绪'
