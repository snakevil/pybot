# encoding: utf-8

from .spot import Spot

class OK(Spot):
    def __init__(self):
        super(OK, self).__init__('ok')
