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
        cursor = 8
        length = len(blob)
        while cursor < length:
            size, = struct.unpack('>I', blob[cursor:cursor + 4])
            cursor += 4
            id = blob[cursor:cursor + 4]
            cursor += 4
            data = blob[cursor:cursor + size]
            cursor += size
            crc32, = struct.unpack('>I', blob[cursor:cursor + 4])
            cursor += 4
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
        y = 0
        cursor = 0
        while y < self.height:
            if 1 == alob[cursor]:
                self._filter_recon_sub(alob, cursor, width, fdst)
            elif 2 == alob[cursor]:
                self._filter_recon_up(alob, cursor, width, fdst)
            elif 3 == alob[cursor]:
                self._filter_recon_average(alob, cursor, width, fdst)
            elif 4 == alob[cursor]:
                self._filter_recon_paeth(alob, cursor, width, fdst)
            __unpack(
                samples,
                alob[cursor + 1:cursor + width],
                cursor - y,
                width - 1
            )
            y += 1
            cursor += width
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
        cursor = offset + 1
        while cursor < length:
            line[cursor] = (line[cursor] + line[cursor - offset]) & 255
            cursor += 1
        alob[start:start + length] = line

    def _filter_recon_up(self, alob, start, length, offset):
        line0 = bytearray(length) if not start else alob[start - length:start]
        line = alob[start:start + length]
        cursor = 1
        while cursor < length:
            line[cursor] = (line[cursor] + line0[cursor]) & 255
            cursor += 1
        alob[start:start + length] = line

    def _filter_recon_average(self, alob, start, length, offset):
        line0 = bytearray(length) if not start else alob[start - length:start]
        line = alob[start:start + length]
        cursor = 1
        while cursor <= offset:
            line[cursor] = (line[cursor] + (line0[cursor] >> 1)) & 255
            cursor += 1
        while cursor < length:
            line[cursor] = (
                line[cursor] + (line[cursor - offset] + line0[cursor] >> 1)
            ) & 255
            cursor += 1
        alob[start:start + length] = line

    def _filter_recon_paeth(self, alob, start, length, offset):
        line0 = bytearray(length) if not start else alob[start - length:start]
        line = alob[start:start + length]
        cursor = 1
        while cursor <= offset:
            line[cursor] = (line[cursor] + line0[cursor]) & 255
            cursor += 1
        while cursor < length:
            line[cursor] = (
                line[cursor] + self._filter_paeth(
                    line[cursor - offset],
                    line0[cursor],
                    line0[cursor - offset]
                )
            ) & 255
            cursor += 1
        alob[start:start + length] = line

    def _filter_paeth(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        return a if pa <= pb and pa <= pc \
            else b if pb <= pc \
                else c

    def _unpack_1(self, bits, stream, offset):
        cursor = 0
        while cursor < length:
            bits = raw[cursor]
            samples = [
                bits >> 7, bits >> 6 & 1, bits >> 5 & 1, bits >> 4 & 1,
                bits >> 3 & 1, bits >> 2 & 1, bits >> 1 & 1, bits & 1
            ]
            i = 0
            while i < 8:
                stream[offset + i] = samples[i] * 255
            offset += 8
            cursor += 1

    def _unpack_2(self, stream, raw, offset, length):
        cursor = 0
        while cursor < length:
            bits = raw[cursor]
            samples = [bits >> 6, bits >> 4 & 3, bits >> 2 & 3, bits & 3]
            i = 0
            while i < 4:
                stream[offset + i] = (samples[i] << 6) \
                    + (samples[i] << 4) \
                    + (samples[i] << 2) \
                    + samples[i]
            offset += 4
            cursor += 1

    def _unpack_4(self, stream, raw, offset, length):
        cursor = 0
        while cursor < length:
            bits = raw[cursor] >> 4
            stream[offset] = (bits << 4) + bits
            bits = raw[cursor] & 15
            stream[offset + 1] = (bits << 4) + bits
            offset += 2
            cursor += 1

    def _unpack_8(self, stream, raw, offset, length):
        stream[offset:offset + length] = raw

    def _extract_greyscale(self, samples, palette):
        length = 4 * self.width * self.height
        rgba = bytearray(length)
        rgba[0::4] = samples[0::1]
        rgba[1::4] = samples[0::1]
        rgba[2::4] = samples[0::1]
        if palette[0]:
            cursor = 0
            while cursor < length:
                if palette[0] != rgba[cursor:cursor + 3]:
                    rgba[cursor + 4] = 255
                cursor += 4
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
            cursor = 0
            while cursor < length:
                if palette[0] != rgba[cursor:cursor + 3]:
                    rgba[cursor + 3] = 255
                cursor += 4
        else:
            rgba[3::4] = [255] * (length >> 2)
        return rgba

    def _extract_indexed(self, samples, palette):
        length = self.width * self.height
        rgba = bytearray(4 * length)
        index = 0
        while index < length:
            rgba[4 * index:4 * index + 4] = palette[samples[index]]
            index += 1
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
