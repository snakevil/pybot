# encoding: utf-8

import time
import struct
import platform
import os

import rsa

from .. import core
from .app import App

__all__ = ['License']

class License(object):
    def __init__(self):
        self._bundle = ''
        self._version = 255
        self._hwaddr = b'\xfe\xdc\xba\x98\x76\x54'
        self._born = int(time.time())
        self._deadline = self._born - 1

    @classmethod
    def load(cls, blob, cipher):
        lic = cls()
        blob = rsa.decrypt(blob, rsa.PrivateKey.load_pkcs1(cipher))
        if 1 == blob[0]:
            version, lic._hwaddr, lic._born, lic._deadline, \
            lic._version, bundle = struct.unpack(
                '>B6s2IB%ds' % (len(blob) - 16), blob
            )
            lic._bundle = bundle.decode('utf-8')
        return lic

    def save(self, cipher):
        bundle = self._bundle.encode('utf-8')
        return rsa.encrypt(
            struct.pack(
                '>B6s2IB%ds' % len(bundle),
                1,
                self._hwaddr,
                self._born,
                self._deadline,
                self._version,
                bundle
            ),
            rsa.PublicKey.load_pkcs1(cipher)
        )

    def verify(self, app):
        if not isinstance(app, App):
            return False
        if self._deadline and time.time() > self._deadline:
            return False
        appcls = type(app)
        if '.'.join([appcls.__module__, appcls.__name__]) != self._bundle:
            return False
        if self._version and self._version != app.version()[0]:
            return False
        if b'\x00\x00\x00\x00\x00\x00' != self._hwaddr \
                and self._hwaddr not in self._mac():
            return False
        return True

    @classmethod
    def new(cls, app, hwaddr = None, days = 0, version = True):
        if not isinstance(app, App):
            raise core.EType(app, App)
        lic = cls()
        appcls = type(app)
        lic._bundle = '.'.join([appcls.__module__, appcls.__name__])
        lic._version = app.version()[0] if version else 0
        lic._hwaddr = hwaddr if isinstance(hwaddr, bytes) and 6 == len(hwaddr) \
            else lic._mac()[0]
        lic._deadline = 0 if 1 > days \
            else lic._born + 86400 * int(days)
        return lic

    @classmethod
    def payload(cls, app, cipher):
        if not isinstance(app, App):
            raise core.EType(app, App)
        appcls = type(app)
        bundle = '.'.join([appcls.__module__, appcls.__name__]).encode('utf-8')
        blen = len(bundle)
        macs = cls._mac()
        mlen = len(macs)
        payload = struct.pack(
            '>B%ds2B%ds' % (6 * mlen, blen),
            mlen,
            b''.join(macs),
            app.version()[0],
            blen,
            bundle
        )
        sign = rsa.sign(payload, rsa.PrivateKey.load_pkcs1(cipher), 'MD5')
        return b''.join([
            payload,
            struct.pack('>H', len(sign)),
            sign
        ])

    @classmethod
    def _mac(cls):
        if not hasattr(cls, '_macs'):
            system = platform.system()
            if 'Windows' == system:
                cls._macs = cls._mac_win32()
            elif 'Darwin' == system:
                cls._macs = cls._mac_macos()
            else:
                cls._macs = cls._mac_linux()
        return cls._macs

    @staticmethod
    def _mac_win32():
        output = os.popen('C:/Windows/System32/ipconfig.exe /all').read()
        macs = []
        active = False
        virtual = False
        mac = b''
        for line in output.split('\n'):
            if '   Physical' == line[0:11]:
                mac = bytes.fromhex(line[39:56].replace('-', ''))
                if b'\x00\x00\x00\x00\x00\x00' == mac:
                    mac = b''
                continue
            if '   Description' == line[0:14] \
                    and 'Microsoft Wi-Fi Direct Virtual' == line[39:69]:
                virtual = True
                continue
            if '   IPv' == line[0:6]:
                active = True
                continue
            if not line:
                if mac and not virtual:
                    if active:
                        macs.insert(0, mac)
                    else:
                        macs.append(mac)
                active = False
                virtual = False
                mac = b''
        return macs

    @staticmethod
    def _mac_macos():
        output = os.popen('/sbin/ifconfig -av').read()
        macs = []
        active = False
        mac = b''
        type = ''
        for line in output.split('\n'):
            if 'ether ' == line[1:7]:
                mac = bytes.fromhex(line[7:].strip().replace(':', ''))
                continue
            if 'status: ' == line[1:9]:
                active = 'a' == line[9]
                continue
            if 'type: ' == line[1:7]:
                type = line[7:]
                continue
            if 'qosmarking' == line[1:11]:
                if mac and type:
                    if active:
                        macs.insert(0, mac)
                    else:
                        macs.append(mac)
                active = False
                mac = b''
                type = ''
        return macs

    @staticmethod
    def _mac_linux():
        output = os.popen('/sbin/ifconfig -a').read()
        macs = []
        active = False
        mac = b''
        type = ''
        for line in output.split('\n'):
            if 'Link encap:' == line[10:21] and -1 < line.find('HWaddr', 21):
                type, cmac = line[21:].split('HWaddr')
                type = type.strip()
                mac = bytes.fromhex(cmac.strip().replace(':', ''))
                continue
            if 'inet' == line[10:14]:
                active = True
                continue
            if not line:
                if mac and mac not in macs:
                    if active:
                        macs.insert(0, mac)
                    else:
                        macs.append(mac)
                active = False
                mac = b''
                type = ''
        return macs
