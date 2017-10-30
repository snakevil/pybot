# encoding: utf-8

import ctypes as c
import ctypes.wintypes as w
import re
import time

user32 = c.windll.user32
kernel32 = c.windll.kernel32
gdi32 = c.windll.gdi32

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
        user32.EnumWindows(_proxy(_every), 0)
        return _stack[1]
    return query
query = _query_gtor()

def get_pid(hwnd):
    pid = c.c_int()
    user32.GetWindowThreadProcessId(hwnd, c.byref(pid))
    return pid.value

def is_minimized(hwnd):
    return bool(user32.IsIconic(hwnd))

def _show_gtor(cmd):
    def show(hwnd):
        user32.ShowWindow(hwnd, cmd)
    return show
minimize = _show_gtor(6)
restore = _show_gtor(9)

def foreground(hwnd):
    user32.SetForegroundWindow(hwnd)

def get_rect(hwnd):
    rect = w.RECT()
    user32.GetWindowRect(hwnd, c.byref(rect))
    return ((rect.left, rect.top), (rect.right, rect.bottom))

def get_size(hwnd):
    rect = w.RECT()
    user32.GetClientRect(hwnd, c.byref(rect))
    return (rect.right - rect.left, rect.bottom - rect.top)

def _click_gtor():
    PROCESS_QUERY_INFORMATION = 0x400
    def _wait_idle(pid):
        hproc = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)
        kernel32.CloseHandle(hproc)
    WM_LBUTTONDOWN = 0x201
    WM_LBUTTONUP = 0x202
    def click(hwnd, x, y):
        pos = ((y & 0xFFFF) << 16) | (x & 0xFFFF)
        pid = get_pid(hwnd)
        user32.PostMessageW(hwnd, WM_LBUTTONDOWN, 0, pos)
        time.sleep(10)
        _wait_idle(pid)
        user32.PostMessageW(hwnd, WM_LBUTTONUP, 0, pos)
        time.sleep(10)
        _wait_idle(pid)
    return click
click = _click_gtor()

def _grab_gtor():
    SRCCOPY = 0xCC0020
    BI_RGB = 0
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
    def grab(hwnd):
        hdcw = user32.GetDC(hwnd)
        hdcm = gdi32.CreateCompatibleDC(hdcw)
        width, height = get_size(hwnd)
        hbmp = gdi32.CreateCompatibleBitmap(hdcw, width, height)
        gdi32.SelectObject(hdcm, hbmp)
        gdi32.BitBlt(
            hdcm,
            0, 0, width, height,
            hdcw,
            0, 0,
            SRCCOPY
        )
        info = BITMAPINFO()
        info.bmiHeader.biSize = c.sizeof(BITMAPINFOHEADER)
        info.bmiHeader.biWidth = width
        info.bmiHeader.biHeight = - height
        info.bmiHeader.biPlanes = 1
        info.bmiHeader.biBitCount = 32
        info.bmiHeader.biCompression = BI_RGB
        info.bmiHeader.biClrUsed = 0
        info.bmiHeader.biClrImportant = 0
        bgra = c.create_string_buffer(width * height * 4)
        bits = gdi32.GetDIBits(hdcm, hbmp, 0, height, bgra, c.byref(info), 0)
        gdi32.DeleteObject(hbmp)
        gdi32.DeleteObject(hdcm)
        user32.ReleaseDC(hwnd, hdcw)
        return bytearray(bgra)
    return grab
grab = _grab_gtor()

__all__ = [
    'query',
    'get_pid', 'is_minimized', 'minimize', 'restore', 'foreground',
    'get_rect', 'get_size',
    'click',
    'grab'
]
