# encoding: utf-8

import platform
system = platform.system()
if 'Windows' == system:
    from ._win32 import *
elif 'Darwin' == system:
    from ._macos import *
else:
    from ._linux import *
