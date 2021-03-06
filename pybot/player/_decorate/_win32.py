# encoding: utf-8

import sys
import ctypes as c
import ctypes.wintypes as w
import re
import time
import random
import math
from .eminimized import EMinimized
from .ewin32 import EWin32

shell32 = c.windll.shell32
user32 = c.windll.user32
kernel32 = c.windll.kernel32
gdi32 = c.windll.gdi32

def get_euid():
    try:
        return 0 if shell32.IsUserAnAdmin() \
            else -1
    except:
        return -1

def su(*cmd):
    if 1 > len(cmd):
        exe = sys.executable
        opts = sys.argv
    elif '.py' == cmd[0][-3:]:
        exe = sys.executable
        opts = cmd
    else:
        exe = cmd[0]
        opts = cmd[1:]
    shell32.ShellExecuteW(
        None,
        'runas',
        '"%s"' % (exe),
        ' '.join(['"%s"' % i for i in opts]),
        None,
        1 # SW_SHOWNORMAL
    )
    sys.exit(0)

def _query_gtor():
    _proxy = c.WINFUNCTYPE(
        c.c_bool,
        c.POINTER(c.c_int),
        c.POINTER(c.c_int)
    )
    _stack = ['', []]
    def _every(hwnd, extra):
        size = 1 + user32.GetWindowTextLengthW(hwnd)
        title = c.create_unicode_buffer(size)
        user32.GetWindowTextW(hwnd, title, size)
        if re.search(_stack[0], title.value):
            _stack[1].append(hwnd)
        return True
    def query(pattern):
        _stack[0] = pattern
        _stack[1] = []
        result = user32.EnumWindows(_proxy(_every), 0)
        if not result:
            raise EWin32('user32.EnumWindows')
        return _stack[1]
    return query
query = _query_gtor()

def get_pid(hwnd):
    pid = c.c_int()
    result = user32.GetWindowThreadProcessId(hwnd, c.byref(pid))
    if not result:
        raise EWin32('user32.GetWindowThreadProcessId')
    return pid.value

def is_minimized(hwnd):
    return bool(user32.IsIconic(hwnd))

def _show_gtor(cmd):
    def show(hwnd):
        user32.ShowWindow(hwnd, cmd)
    return show
minimize = _show_gtor(6)
restore = _show_gtor(9)

def destroy(hwnd):
    WM_CLOSE = 0x10
    result = user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
    if not result:
        raise EWin32('user32.PostMessageW')

def foreground(hwnd):
    result = user32.SetForegroundWindow(hwnd)
    if not result:
        raise EWin32('user32.SetForegroundWindow')

def get_rect(hwnd):
    rect = w.RECT()
    result = user32.GetWindowRect(hwnd, c.byref(rect))
    if not result:
        raise EWin32('user32.GetWindowRect')
    return ((rect.left, rect.top), (rect.right, rect.bottom))

def get_size(hwnd):
    rect = w.RECT()
    result = user32.GetClientRect(hwnd, c.byref(rect))
    if not result:
        raise EWin32('user32.GetClientRect')
    return (rect.right - rect.left, rect.bottom - rect.top)

def resize(hwnd, width, height, top = 0, left = 0):
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_NOZORDER = 0x0004
    SWP_NOACTIVATE = 0x0010
    flag = SWP_NOZORDER + SWP_NOACTIVATE
    (ox0, oy0), (ox1, oy1) = get_rect(hwnd)
    if not top and not left:
        flag += SWP_NOMOVE
        left = ox0
        top = oy0
    iw, ih = get_size(hwnd)
    width += ox1 - ox0 - iw
    height += oy1 - oy0 - ih
    flag = SWP_NOZORDER
    result = user32.SetWindowPos(hwnd, 0, 0, 0, width, height, flag)
    if not result:
        raise EWin32('user32.SetWindowPos')
    flag = SWP_NOSIZE + SWP_NOZORDER + SWP_NOACTIVATE
    result = user32.SetWindowPos(hwnd, 0, left, top, 0, 0, flag)
    if not result:
        raise EWin32('user32.SetWindowPos')

def _click_gtor():
    class POINT(c.Structure):
        _fields_ = [
            ('x', w.LONG),
            ('y', w.LONG)
        ]
    PROCESS_QUERY_INFORMATION = 0x400
    def _wait_idle(pid):
        hproc = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)
        result = kernel32.CloseHandle(hproc)
        if not result:
            raise EWin32('kernel32.CloseHandle')
    def _pack(x, y):
        return ((y & 0xFFFF) << 16) | (x & 0xFFFF)
    def _post(hwnd, force, *messages):
        if force:
            pos = POINT()
            result = user32.GetCursorPos(c.byref(pos))
            if not result:
                raise EWin32('user32.GetCursorPos')
        pid = get_pid(hwnd)
        for x, y, wparam, msg in messages:
            result = user32.PostMessageW(hwnd, msg, wparam, _pack(x, y))
            if not result:
                raise EWin32('user32.PostMessageW')
            time.sleep(.01)
            _wait_idle(pid)
    def _bezier(src, dest, progress):
        return (dest - src) * progress + src
    def _bezier2(src, mid, dest, progress):
        return _bezier(
            _bezier(src, mid, progress),
            _bezier(mid, dest, progress),
            progress
        )
    WM_MOUSEMOVE = 0x200
    WM_LBUTTONDOWN = 0x201
    WM_LBUTTONUP = 0x202
    WM_RBUTTONDOWN = 0x0204
    WM_RBUTTONUP = 0x0205
    MK_LBUTTON = 0x0001
    MK_RBUTTON = 0x0002
    def click(hwnd, x, y, force = False):
        _post(
            hwnd,
            force,
            (x, y, MK_LBUTTON, WM_LBUTTONDOWN),
            (x, y, MK_LBUTTON, WM_LBUTTONUP)
        )
    def rclick(hwnd, x, y, force = False):
        _post(
            hwnd,
            force,
            (x, y, MK_RBUTTON, WM_RBUTTONDOWN),
            (x, y, MK_RBUTTON, WM_RBUTTONUP)
        )
    def drag(hwnd, start, end, force = False):
        distance = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** .5
        steps = 1 + int(distance / 10)
        if 1 < steps:
            degree = random.uniform(0, math.pi)
            radius = min(16, random.uniform(0, distance / 4))
            midx = int(
                round((start[0] + end[0]) / 2 + radius * math.cos(degree))
            )
            midy = int(
                round((start[1] + end[1]) / 2 + radius * math.sin(degree))
            )
            factor = 1 / steps
            msgs = [
                (
                    int(round(_bezier2(start[0], midx, end[0], factor * i))),
                    int(round(_bezier2(start[1], midy, end[1], factor * i))),
                    MK_LBUTTON,
                    WM_MOUSEMOVE
                ) for i in range(1, steps)
            ]
        else:
            msgs = []
        msgs.insert(0, (*start, MK_LBUTTON, WM_LBUTTONDOWN))
        msgs.append((*end, MK_LBUTTON, WM_LBUTTONUP))
        _post(hwnd, force, *msgs)
    return (click, rclick, drag)
click, rclick, drag = _click_gtor()

def _grab_gtor():
    SRCCOPY = 0xCC0020
    BI_RGB = 0
    PW_CLIENTONLY = 1
    class BITMAPINFOHEADER(c.Structure):
        _fields_ = [
            ('biSize', w.DWORD),
            ('biWidth', w.LONG),
            ('biHeight', w.LONG),
            ('biPlanes', w.WORD),
            ('biBitCount', w.WORD),
            ('biCompression', w.DWORD),
            ('biSizeImage', w.DWORD),
            ('biXPelsPerMeter', w.LONG),
            ('biYPelsPerMeter', w.LONG),
            ('biClrUsed', w.DWORD),
            ('biClrImportant', w.DWORD)
        ]
    class BITMAPINFO(c.Structure):
        _fields_ = [
            ('bmiHeader', BITMAPINFOHEADER),
            ('bmiColors', w.DWORD * 3)
        ]
    def _rgba(hdc, hbmp, width, height):
        info = BITMAPINFO()
        info.bmiHeader.biSize = c.sizeof(BITMAPINFOHEADER)
        info.bmiHeader.biWidth = width
        info.bmiHeader.biHeight = - height
        info.bmiHeader.biPlanes = 1
        info.bmiHeader.biBitCount = 32
        info.bmiHeader.biCompression = BI_RGB
        info.bmiHeader.biClrUsed = 0
        info.bmiHeader.biClrImportant = 0
        length = width * height * 4
        bgrr = c.create_string_buffer(length)
        lines = gdi32.GetDIBits(hdc, hbmp, 0, height, bgrr, c.byref(info), 0)
        if lines != height:
            raise EWin32('gdi32.GetDIBits')
        rgba = bytearray(length)
        rgba[0::4] = bgrr[2::4]
        rgba[1::4] = bgrr[1::4]
        rgba[2::4] = bgrr[0::4]
        rgba[3::4] = [255] * (length >> 2)
        return rgba
    def grab(hwnd):
        hdcw = user32.GetDC(hwnd)
        hdcm = gdi32.CreateCompatibleDC(hdcw)
        width, height = get_size(hwnd)
        if 1 > width or 1 > height:
            raise EMinimized()
        hbmp = gdi32.CreateCompatibleBitmap(hdcw, width, height)
        gdi32.SelectObject(hdcm, hbmp)
        result = gdi32.BitBlt(
            hdcm,
            0, 0, width, height,
            hdcw,
            0, 0,
            SRCCOPY
        )
        if not result:
            raise EWin32('gdi32.BitBlt')
        rgba = _rgba(hdcm, hbmp, width, height)
        gdi32.DeleteObject(hbmp)
        gdi32.DeleteObject(hdcm)
        user32.ReleaseDC(hwnd, hdcw)
        return rgba
    def grab2(hwnd):
        hdcw = user32.GetDC(hwnd)
        hdcm = gdi32.CreateCompatibleDC(hdcw)
        width, height = get_size(hwnd)
        if 1 > width or 1 > height:
            raise EMinimized()
        hbmp = gdi32.CreateCompatibleBitmap(hdcw, width, height)
        gdi32.SelectObject(hdcm, hbmp)
        result = user32.PrintWindow(hwnd, hdcm, PW_CLIENTONLY)
        if not result:
            raise EWin32('user32.PrintWindow')
        rgba = _rgba(hdcm, hbmp, width, height)
        gdi32.DeleteObject(hbmp)
        gdi32.DeleteObject(hdcm)
        user32.ReleaseDC(hwnd, hdcw)
        return rgba
    return grab
grab = _grab_gtor()

__all__ = [
    'get_euid', 'su',
    'query',
    'get_pid', 'is_minimized', 'minimize', 'restore', 'foreground',
    'get_rect', 'get_size', 'resize',
    'click', 'rclick', 'drag', 'grab',
    'destroy'
]
