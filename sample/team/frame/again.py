# encoding: utf-8

from pybot.bot import expect

class Again(expect.Fingerprint):
    def __init__(self):
        super(Again, self).__init__(
            ((339, 213), (381, 237)),
            'ff8707050406078f',
            118,
            ok = (((418, 250), (530, 292)), 5),
            check = (((339, 213), (363, 237)), 4),
            cancel = (((270, 250), (382, 292)), 5)
        )

    def __str__(self):
        return '继续组队'
