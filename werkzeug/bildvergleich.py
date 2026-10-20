#!/usr/bin/env python3
"""Vergleicht zwei PNG-Bildschirmfotos Pixel für Pixel (Thema 0.2,
Regression hell: Repo gegen Live-Ablage) und liest einzelne Pixel.

Aufruf:  bildvergleich.py <a.png> <b.png>      Exit 0 = pixelgleich
         bildvergleich.py --pixel <png> x,y [x,y …]
Ohne Fremdbibliotheken (zlib, PNG-Filter nach Spezifikation).
"""

import struct
import sys
import zlib


def lese(pfad: str):
    d = open(pfad, "rb").read()
    i, idat = 8, b""
    while i < len(d):
        n = struct.unpack(">I", d[i:i + 4])[0]
        typ, inhalt = d[i + 4:i + 8], d[i + 8:i + 8 + n]
        if typ == b"IHDR":
            w, h, _, ct = struct.unpack(">IIBB", inhalt[:10])
        elif typ == b"IDAT":
            idat += inhalt
        i += 12 + n
    roh = zlib.decompress(idat)
    bpp = {2: 3, 6: 4}[ct]
    st = w * bpp
    zeilen, vorige, p = [], bytearray(st), 0
    for _ in range(h):
        f, z = roh[p], bytearray(roh[p + 1:p + 1 + st])
        p += 1 + st
        for x in range(st):
            a = z[x - bpp] if x >= bpp else 0
            b = vorige[x]
            c = vorige[x - bpp] if x >= bpp else 0
            if f == 1:
                z[x] = (z[x] + a) & 255
            elif f == 2:
                z[x] = (z[x] + b) & 255
            elif f == 3:
                z[x] = (z[x] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                z[x] = (z[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        zeilen.append(bytes(z[i] for i in range(st) if bpp == 3 or i % 4 != 3))
        vorige = z
    return w, h, zeilen


def main() -> int:
    if sys.argv[1] == "--pixel":
        w, h, z = lese(sys.argv[2])
        for xy in sys.argv[3:]:
            x, y = (int(v) for v in xy.split(","))
            print(f"{xy} #{z[y][3 * x:3 * x + 3].hex()}")
        return 0
    a, b = lese(sys.argv[1]), lese(sys.argv[2])
    if a[:2] != b[:2]:
        print(f"Größe verschieden: {a[:2]} gegen {b[:2]}")
        return 1
    punkte = [(i // 3, y) for y, (za, zb) in enumerate(zip(a[2], b[2]))
              for i in range(0, len(za), 3) if za[i:i + 3] != zb[i:i + 3]]
    anders = len(punkte)
    rahmen = ""
    if punkte:
        xs, ys = [p[0] for p in punkte], [p[1] for p in punkte]
        rahmen = f", Bereich x {min(xs)}–{max(xs)}, y {min(ys)}–{max(ys)}"
    print(f"{'pixelgleich' if not anders else f'{anders} Pixel verschieden'} ({a[0]}x{a[1]}{rahmen})")
    return 0 if not anders else 1


if __name__ == "__main__":
    sys.exit(main())
