# encoding: utf-8

from .. import core

class ECompany(core.Error):
    def __init__(self, name, all):
        super(ECompany, self).__init__(
            0x3001,
            'Company %r not in %r.' % (name, all),
            name = name,
            all = all
        )
