# encoding: utf-8

import sys
import time
import pybot

windows = pybot.player.Window.all(
    '' if 2 > len(sys.argv) else sys.argv[1]
)

now = int(time.time())
for i in range(len(windows)):
    pic = windows[i].snap()
    if pic:
        pic.save('%d-%d.png' % (now, i))
