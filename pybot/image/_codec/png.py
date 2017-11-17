# encoding: utf-8

import struct
import zlib

''' http://www.w3.org/TR/PNG
'''
class PNG(object):
    GREYSCALE = 0

    TRUECOLOR = 0b10

    INDEXED = 0b11

    GREYSCALE_ALPHA = 0b100

    TRUECOLOR_ALPHA = 0b110

    def __init__(self, width, height, depth = 8, type = TRUECOLOR):
        self.width = width
        self.height = height
        if self.GREYSCALE == type:
            assert depth in [1, 2, 4, 8, 16]
        elif self.INDEXED == type:
            assert depth in [1, 2, 4, 8]
        else:
            assert depth in [8, 16]
        self.depth = depth
        self.type = type

    def pixel(self, x, y):
        pos = 4 * (self.width * y + x)
        return tuple(self.data[pos:pos + 4])

    def encode(self, alob):
        length = self.width * self.height
        alphas = bytearray(length)
        if self.GREYSCALE_ALPHA == self.type:
            alphas[:] = alob[3::4]
            if 255 == min(list(alphas)):
                self.type = self.GREYSCALE
                alphas[:] = alob[0::4]
                alob = alphas
        elif self.TRUECOLOR_ALPHA == self.type:
            alphas[:] = alob[3::4]
            if 255 == min(list(alphas)):
                self.type = self.TRUECOLOR
                alphas = bytearray(3 * length)
                alphas[0::3] = alob[0::4]
                alphas[1::3] = alob[1::4]
                alphas[2::3] = alob[2::4]
                alob = alphas
        return b''.join([
            b'\x89PNG\r\n\x1a\n',
            self._encode_chunk(
                b'IHDR',
                struct.pack(
                    '>2I5B',
                    self.width, self.height,
                    self.depth, self.type, 0, 0, 0
                )
            ),
            self._encode_chunk(
                b'IDAT',
                zlib.compress(self._pack(alob, self.depth))
            ),
            b'\x00\x00\x00\x00IEND\xaeB`\x82'
        ])

    def _encode_chunk(self, id, blob):
        chunk = [
            struct.pack('>I', len(blob)),
            id,
            blob
        ]
        chunk.append(struct.pack('>I', zlib.crc32(b''.join(chunk[1:3]))))
        return b''.join(chunk)

    def _pack(self, samples, depth):
        assert 8 == depth
        size = 1 + (3 & self.type) + (1 if 3 < self.type else 0)
        if self.INDEXED == self.type:
            size = 1
        width = size * self.width
        return b''.join([
            b'\x00' + samples[width * y:width * (y + 1)] \
                for y in range(self.height)
        ])

    @classmethod
    def decode(cls, blob):
        chunks = cls._decode_chunks(blob)
        ihdr = cls._decode_ihdr(chunks[b'IHDR'])
        self = cls(*ihdr[0:4])
        assert self.INDEXED != self.type or b'PLTE' in chunks
        assert not ihdr[-1]
        self.data = self._decode_idat(
            bytearray(zlib.decompress(chunks[b'IDAT'])),
            self._decode_plte(chunks.get(b'PLTE'), chunks.get(b'tRNS')),
            self._decode_sbit(chunks.get(b'sBIT'))
        )
        return self

    @staticmethod
    def _decode_chunks(blob):
        ids = [b'IHDR', b'PLTE', b'IDAT', b'IEND', b'tRNS', b'sBIT']
        mask = 0xffffffff
        chunks = {}
        i = 8
        length = len(blob)
        while i < length:
            size, = struct.unpack('>I', blob[i:i + 4])
            i += 4
            id = blob[i:i + 4]
            i += 4
            data = blob[i:i + size]
            i += size
            crc32, = struct.unpack('>I', blob[i:i + 4])
            i += 4
            if id not in ids:
                continue
            assert mask & zlib.crc32(id + data) == crc32
            if b'IDAT' == id and id in chunks:
                chunks[id] += data
            else:
                assert id not in chunks
                chunks[id] = data
        assert b'IHDR' in chunks and b'IDAT' in chunks and b'IEND' in chunks
        return chunks

    @staticmethod
    def _decode_ihdr(blob):
        return struct.unpack('>2I5B', blob)

    def _decode_sbit(self, blob):
        pass

    def _decode_plte(self, blob, trns):
        if self.INDEXED == self.type:
            return tuple([
                blob[3 * i:3 * i + 3] + (b'\xff' if not trns else trns[i]) \
                    for i in range(len(blob) // 3)
            ])
        if not trns:
            return (None,)
        color = bytearray(255, 255, 255, 255)
        if self.GREYSCALE == self.type:
            r, = struct.unpack('>H', trns)
            color[0] = color[1] = color[2] = r
        elif self.TRUECOLOR == self.type:
            color[0:3] = struct.unpack('>3H', trns)
        return (bytes(color),)

    def _decode_idat(self, alob, palette, sbit):
        ''' 1. read pixel data
                1.1. extract
                1.2. filter recon
            2. convert to rgba
                2.2. stretch to 8bit
                2.1. expand rgb
                2.2. correct alpha
            3. shift significant bits
        '''
        # 每像素的采样数量
        size = 1 + (3 & self.type) + (1 if 3 < self.type else 0)
        if self.INDEXED == self.type:
            size = 1
        # 总字节数
        length = len(alob)
        # 每行的字节数
        width = ((size * self.depth * self.width + 7) >> 3) + 1
        # 反滤偏移字节数
        fdst = 1 if 8 > self.depth else size * self.depth >> 3
        # 解码深度
        if 7 < self.depth:
            __unpack = self._unpack_8
        elif 4 == self.depth:
            __unpack = self._unpack_4
        elif 2 == self.depth:
            __unpack = self._unpack_2
        else:
            __unpack = self._unpack_1
        # 已解码的采样流
        samples = bytearray(size * self.width * self.height)
        i = 0
        for y in range(self.height):
            if 1 == alob[i]:
                self._filter_recon_sub(alob, i, width, fdst)
            elif 2 == alob[i]:
                self._filter_recon_up(alob, i, width, fdst)
            elif 3 == alob[i]:
                self._filter_recon_average(alob, i, width, fdst)
            elif 4 == alob[i]:
                self._filter_recon_paeth(alob, i, width, fdst)
            __unpack(
                samples,
                alob[i + 1:i + width],
                i - y,
                width - 1
            )
            i += width
        if self.TRUECOLOR_ALPHA == self.type:
            return self._extract_trucolor_alpha(samples)
        if self.TRUECOLOR == self.type:
            return self._extract_trucolor(samples, palette)
        if self.GREYSCALE == self.type:
            return self._extract_greyscale(samples, palette)
        if self.GREYSCALE_ALPHA == self.type:
            return self._extract_greyscale_alpha(samples)
        return self._extract_indexed(samples, palette)

    def _filter_recon_sub(self, alob, start, length, offset):
        line = alob[start:start + length]
        for i in range(offset + 1, length):
            line[i] = (line[i] + line[i - offset]) & 255
        alob[start:start + length] = line

    def _filter_recon_up(self, alob, start, length, offset):
        line0 = bytearray(length) if not start else alob[start - length:start]
        line = alob[start:start + length]
        for i in range(length):
            line[i] = (line[i] + line0[i]) & 255
        alob[start:start + length] = line

    def _filter_recon_average(self, alob, start, length, offset):
        line0 = bytearray(length) if not start else alob[start - length:start]
        line = alob[start:start + length]
        for i in range(1, offset + 1):
            line[i] = (line[i] + (line0[i] >> 1)) & 255
        for i in range(offset + 1, length):
            line[i] = (
                line[i] + (line[i - offset] + line0[i] >> 1)
            ) & 255
        alob[start:start + length] = line

    def _filter_recon_paeth(self, alob, start, length, offset):
        line0 = bytearray(length) if not start else alob[start - length:start]
        line = alob[start:start + length]
        for i in range(1, offset + 1):
            line[i] = (line[i] + line0[i]) & 255
        for i in range(offset + 1, length):
            line[i] = (
                line[i] + self._filter_paeth(
                    line[i - offset],
                    line0[i],
                    line0[i - offset]
                )
            ) & 255
        alob[start:start + length] = line

    def _filter_paeth(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        return a if pa <= pb and pa <= pc \
            else b if pb <= pc \
                else c

    def _unpack_1(self, stream, raw, offset, length):
        for i in range(length):
            bits = raw[i]
            samples = [
                bits >> 7, bits >> 6 & 1, bits >> 5 & 1, bits >> 4 & 1,
                bits >> 3 & 1, bits >> 2 & 1, bits >> 1 & 1, bits & 1
            ]
            for j in range(8):
                stream[offset + j] = 255 if samples[j] else 0
            offset += 8

    def _unpack_2(self, stream, raw, offset, length):
        for i in range(length):
            bits = raw[i]
            samples = [bits >> 6, bits >> 4 & 3, bits >> 2 & 3, bits & 3]
            for j in range(4):
                stream[offset + j] = (samples[j] << 6) \
                    + (samples[j] << 4) \
                    + (samples[j] << 2) \
                    + samples[j]
            offset += 4

    def _unpack_4(self, stream, raw, offset, length):
        for i in range(length):
            bits = raw[i] >> 4
            stream[offset] = (bits << 4) + bits
            bits = raw[i] & 15
            stream[offset + 1] = (bits << 4) + bits
            offset += 2

    def _unpack_8(self, stream, raw, offset, length):
        stream[offset:offset + length] = raw

    def _extract_greyscale(self, samples, palette):
        length = 4 * self.width * self.height
        rgba = bytearray(length)
        rgba[0::4] = samples[0::1]
        rgba[1::4] = samples[0::1]
        rgba[2::4] = samples[0::1]
        if palette[0]:
            for i in range(0, length, 4):
                if palette[0] != rgba[i:i + 3]:
                    rgba[i + 3] = 255
        else:
            rgba[3::4] = [255] * (length >> 2)
        return rgba

    def _extract_trucolor(self, samples, palette):
        length = 4 * self.width * self.height
        rgba = bytearray(length)
        rgba[0::4] = samples[0::3]
        rgba[1::4] = samples[1::3]
        rgba[2::4] = samples[2::3]
        if palette[0]:
            for i in range(0, length, 4):
                if palette[0] != rgba[i:i + 3]:
                    rgba[i + 3] = 255
        else:
            rgba[3::4] = [255] * (length >> 2)
        return rgba

    def _extract_indexed(self, samples, palette):
        length = self.width * self.height
        rgba = bytearray(4 * length)
        for i in range(length):
            rgba[4 * i:4 * i + 4] = palette[samples[i]]
        return rgba

    def _extract_greyscale_alpha(self, samples):
        length = self.width * self.height
        rgba = bytearray(4 * length)
        rgba[0::4] = samples[0::2]
        rgba[1::4] = samples[0::2]
        rgba[2::4] = samples[0::2]
        rgba[3::4] = samples[1::2]
        return rgba

    def _extract_trucolor_alpha(self, samples):
        return samples
