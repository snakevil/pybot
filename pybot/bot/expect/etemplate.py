# encoding: utf-8

from ... import core

class ETemplate(core.Error):
    def __init__(self, template):
        super(ETemplate, self).__init__(
            0x3106,
            'Illegal template %r.' % template,
            template = template
        )
