# encoding: utf-8

from pybot.bot import expect

class Repeat(expect.Fingerprint):
    def __init__(self):
        super(Repeat, self).__init__(
            ((339, 213), (381, 237)),
            '8f8767555426078f',
            121,
            ok = (((418, 250), (530, 292)), 5),
            uncheck = (((339, 213), (363, 237)), 4),
            cancel = (((270, 250), (382, 292)), 5)
        )
