#!/usr/bin/env python3
"""Titelknöpfe der labwc-Themen „Querencia-Klassisch“ und
„Querencia-Klassisch-Dunkel“ (Thema 0.2.2).

    labwc-knoepfe.py            schreibt die PNG nach labwc/<Thema>/
    labwc-knoepfe.py --pruefen  vergleicht nur (Exit 1 bei Abweichung)

Zeichnung und helle Farben unverändert aus
querencia-werkstatt-w3-system/theme-b/werkzeug/theme_b.py (Variante B, live
seit Alpha 1): eckige Knopffläche mit 3D-Kante, Symbole für Minimieren und
Maximieren, rotes X für Schließen. Die hellen PNG sind byte-gleich mit
querencia-runtime data/themes/Querencia-Klassisch/labwc (nachgeprüft mit
--pruefen). Die dunklen nehmen die Knopffarben der dunklen GTK-Fassung
(Verlauf #57554f → #4a4843, Rand #23221f), Symbole #f2f1f0 und ein
einfarbiges X in der dunklen Fehlerschrift #ed8b85 (überfahren #f3a7a1,
inaktiv #cc8a85). Ein dunkler Umriss wie hell verschwände auf der dunklen
Fläche; ohne ihn grenzt sich das X selbst mit mindestens 3:1 ab
(werkzeug/kontrast.py, Tabelle Titelknöpfe).

Nur Standardbibliothek und GdkPixbuf (python3-gi).
"""
import math
import os
import sys

import gi

gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, GLib  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BW, BH = 24, 22  # window.button.width/height

# Hell (theme_b.py, RGB 0..255)
AKTIV = {
    "rahmen": (122, 117, 112),
    "licht": (255, 255, 255),
    "schatten": (160, 155, 150),
    "oben": (246, 245, 243),
    "unten": (214, 210, 206),
    "symbol": (0, 0, 0),
    "kreuz": (204, 0, 0),
    "kreuz_rand": (130, 0, 0),
}
AKTIV_HOVER = dict(AKTIV, rahmen=(80, 76, 72), oben=(255, 255, 255), unten=(240, 238, 235))
INAKTIV = dict(AKTIV, rahmen=(170, 166, 162), licht=(252, 252, 251), schatten=(196, 193, 190),
               oben=(246, 245, 244), unten=(232, 230, 228), symbol=(110, 110, 110),
               kreuz=(196, 110, 110), kreuz_rand=(160, 90, 90))
INAKTIV_HOVER = dict(INAKTIV, rahmen=(80, 76, 72), oben=(255, 255, 255), unten=(240, 238, 236),
                     symbol=(60, 60, 60), kreuz=(204, 0, 0), kreuz_rand=(130, 0, 0))

# Dunkel (Knopf der dunklen GTK-Fassung, docs/farben.md)
D_AKTIV = {
    "rahmen": (0x23, 0x22, 0x1f),
    "licht": (0x67, 0x65, 0x5f),
    "schatten": (0x3a, 0x39, 0x35),
    "oben": (0x57, 0x55, 0x4f),
    "unten": (0x4a, 0x48, 0x43),
    "symbol": (0xf2, 0xf1, 0xf0),
    "kreuz": (0xed, 0x8b, 0x85),
    "kreuz_rand": (0xed, 0x8b, 0x85),
}
D_AKTIV_HOVER = dict(D_AKTIV, rahmen=(0x14, 0x13, 0x11), licht=(0x76, 0x74, 0x6e),
                     oben=(0x66, 0x64, 0x5e), unten=(0x5a, 0x58, 0x52),
                     kreuz=(0xf3, 0xa7, 0xa1), kreuz_rand=(0xf3, 0xa7, 0xa1))
D_INAKTIV = dict(D_AKTIV, rahmen=(0x2b, 0x2a, 0x27), licht=(0x55, 0x53, 0x4d), schatten=(0x38, 0x37, 0x33),
                 oben=(0x4a, 0x48, 0x43), unten=(0x40, 0x3f, 0x3b), symbol=(0xa8, 0xa2, 0x9d),
                 kreuz=(0xcc, 0x8a, 0x85), kreuz_rand=(0xcc, 0x8a, 0x85))
D_INAKTIV_HOVER = dict(D_AKTIV_HOVER)

THEMEN = {
    "Querencia-Klassisch": ((AKTIV, AKTIV_HOVER), (INAKTIV, INAKTIV_HOVER)),
    "Querencia-Klassisch-Dunkel": ((D_AKTIV, D_AKTIV_HOVER), (D_INAKTIV, D_INAKTIV_HOVER)),
}


class Bild:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[(0, 0, 0, 0)] * w for _ in range(h)]

    def setze(self, x, y, rgb, a=1.0):
        if not (0 <= x < self.w and 0 <= y < self.h) or a <= 0:
            return
        r0, g0, b0, a0 = self.px[y][x]
        a0 /= 255.0
        an = a + a0 * (1 - a)
        if an <= 0:
            return
        mix = [(c * a + c0 * a0 * (1 - a)) / an for c, c0 in zip(rgb, (r0, g0, b0))]
        self.px[y][x] = (round(mix[0]), round(mix[1]), round(mix[2]), round(an * 255))

    def rechteck(self, x0, y0, x1, y1, rgb):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.setze(x, y, rgb)

    def linie(self, ax, ay, bx, by, breite, rgb):
        """Kantengeglättete Linie (Abstand Pixelmitte → Strecke)."""
        for y in range(self.h):
            for x in range(self.w):
                px_, py_ = x + 0.5, y + 0.5
                dx, dy = bx - ax, by - ay
                t = max(0.0, min(1.0, ((px_ - ax) * dx + (py_ - ay) * dy) / (dx * dx + dy * dy)))
                d = math.hypot(px_ - (ax + t * dx), py_ - (ay + t * dy))
                a = max(0.0, min(1.0, breite / 2 + 0.5 - d))
                self.setze(x, y, rgb, a)

    def png(self) -> bytes:
        daten = bytearray()
        for zeile in self.px:
            for r, g, b, a in zeile:
                daten += bytes((r, g, b, a))
        pix = GdkPixbuf.Pixbuf.new_from_bytes(GLib.Bytes.new(bytes(daten)), GdkPixbuf.Colorspace.RGB,
                                              True, 8, self.w, self.h, self.w * 4)
        ok, puffer = pix.save_to_bufferv("png", [], [])
        assert ok
        return bytes(puffer)


def flaeche(f):
    """Eckige Knopffläche mit dezenter 3D-Kante, 1 px Luft rundum."""
    b = Bild(BW, BH)
    x0, y0, x1, y1 = 1, 1, BW - 2, BH - 2
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        rgb = tuple(round(o + (u - o) * t) for o, u in zip(f["oben"], f["unten"]))
        b.rechteck(x0, y, x1, y, rgb)
    b.rechteck(x0, y0, x1, y0, f["rahmen"])
    b.rechteck(x0, y1, x1, y1, f["rahmen"])
    b.rechteck(x0, y0, x0, y1, f["rahmen"])
    b.rechteck(x1, y0, x1, y1, f["rahmen"])
    b.rechteck(x0 + 1, y0 + 1, x1 - 1, y0 + 1, f["licht"])
    b.rechteck(x0 + 1, y0 + 1, x0 + 1, y1 - 1, f["licht"])
    b.rechteck(x0 + 1, y1 - 1, x1 - 1, y1 - 1, f["schatten"])
    b.rechteck(x1 - 1, y0 + 1, x1 - 1, y1 - 1, f["schatten"])
    return b


def symbol(art, f):
    b = flaeche(f)
    cx, cy = BW // 2, BH // 2
    s = f["symbol"]
    if art == "iconify":
        b.rechteck(cx - 5, cy + 3, cx + 4, cy + 4, s)
    elif art == "max":
        x0, y0, x1, y1 = cx - 5, cy - 5, cx + 4, cy + 4
        b.rechteck(x0, y0, x1, y0 + 1, s)
        b.rechteck(x0, y1, x1, y1, s)
        b.rechteck(x0, y0, x0, y1, s)
        b.rechteck(x1, y0, x1, y1, s)
    elif art == "max_toggled":
        x0, y0, x1, y1 = cx - 2, cy - 6, cx + 5, cy + 1
        b.rechteck(x0, y0, x1, y0 + 1, s); b.rechteck(x1, y0, x1, y1, s)
        b.rechteck(x0, y0, x0, y0 + 2, s); b.rechteck(x1 - 2, y1, x1, y1, s)
        x0, y0, x1, y1 = cx - 6, cy - 2, cx + 2, cy + 5
        b.rechteck(x0, y0, x1, y0 + 1, s); b.rechteck(x0, y1, x1, y1, s)
        b.rechteck(x0, y0, x0, y1, s); b.rechteck(x1, y0, x1, y1, s)
    elif art == "close":
        a, e = 6.5, 15.5
        oy = (BH - BW) / 2
        for (ax, ay, bx, by) in [(a, a + oy, e + 2, e + 2 + oy), (e + 2, a + oy, a, e + 2 + oy)]:
            b.linie(ax, ay, bx, by, 3.6, f["kreuz_rand"])
        for (ax, ay, bx, by) in [(a, a + oy, e + 2, e + 2 + oy), (e + 2, a + oy, a, e + 2 + oy)]:
            b.linie(ax, ay, bx, by, 2.4, f["kreuz"])
    return b


def knoepfe(thema):
    (an, an_h), (aus, aus_h) = THEMEN[thema]
    for art in ("iconify", "max", "max_toggled", "close"):
        for zustand, normal, hover in (("active", an, an_h), ("inactive", aus, aus_h)):
            yield f"{art}-{zustand}.png", symbol(art, normal).png()
            yield f"{art}_hover-{zustand}.png", symbol(art, hover).png()


def main() -> int:
    pruefen = "--pruefen" in sys.argv[1:]
    fehler = 0
    for thema in THEMEN:
        ziel = os.path.join(REPO, "labwc", thema)
        os.makedirs(ziel, exist_ok=True)
        for name, daten in knoepfe(thema):
            pfad = os.path.join(ziel, name)
            alt = open(pfad, "rb").read() if os.path.exists(pfad) else None
            if alt == daten:
                continue
            if pruefen:
                print(f"weicht ab: labwc/{thema}/{name}")
                fehler = 1
            else:
                with open(pfad, "wb") as f:
                    f.write(daten)
                print(f"geschrieben: labwc/{thema}/{name}")
    if pruefen and not fehler:
        print("labwc-Knöpfe: alle 32 PNG wie erzeugt")
    return fehler


if __name__ == "__main__":
    sys.exit(main())
