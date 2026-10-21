#!/usr/bin/env python3
"""Thema 0.2.1: zählt Pixel genau einer Farbe in einem PNG, wahlweise nur in
einem Bereich (Beleg, dass eine neue Farbe tatsächlich gezeichnet wird).

Aufruf:  farbzaehler.py <png> #rrggbb [#rrggbb …] [--bereich x0,y0,x1,y1]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bildvergleich import lese  # noqa: E402


def main() -> int:
    args = sys.argv[1:]
    bereich = None
    if "--bereich" in args:
        i = args.index("--bereich")
        bereich = [int(v) for v in args[i + 1].split(",")]
        del args[i:i + 2]
    w, h, px = lese(args[0])
    x0, y0, x1, y1 = bereich or (0, 0, w - 1, h - 1)
    for farbe in args[1:]:
        ziel = bytes.fromhex(farbe[1:7])
        n = sum(1 for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if px[y][3 * x:3 * x + 3] == ziel)
        print(f"{farbe}: {n} Pixel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
