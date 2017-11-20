# encoding: utf-8

from .spot import Spot

class Cancel(Spot):
    def __init__(self):
        super(Cancel, self).__init__('cancel')
