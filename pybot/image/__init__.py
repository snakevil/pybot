# encoding: utf-8

from ._struct import *
from .image import Image
from .screenshot import Screenshot

load = Image.load
template = Image.binary
greyscale = Image.greyscale
