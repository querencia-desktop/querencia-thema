#!/usr/bin/env python3
"""Erzeugt Querencia-Klassisch/gtk-4.0/gtk.css und gtk-3.0/gtk.css.

Grundlage ist das eingebaute Thema der installierten GTK-Bibliothek
(GTK 4: resource:///org/gtk/libgtk/theme/Default/Default-light.css,
GTK 3: resource:///org/gtk/libgtk/theme/Adwaita/gtk-contained.css), gelesen
mit `gresource extract`. Daran ändert das Skript drei Dinge:

  1. Farben: die blaue Akzentfamilie wird auf den Querencia-Akzent #F07746
     gedreht, einige Grautöne auf die Ambiance-Palette gesetzt (FARBEN).
  2. Ecken: große Radien (5 bis 9 px) werden zu 3 px (GNOME 2).
  3. :backdrop fällt weg: Fenster ohne Fokus sehen aus wie mit Fokus,
     wie unter GNOME 2 (die Rahmenfarbe zeigt den Fokus, nicht der Inhalt).

Danach hängt es die eigene Schicht quelle/gtk4-klassisch.css bzw.
quelle/gtk3-klassisch.css an. Bilder aus dem Grundthema werden nicht
übernommen; die drei Markierungen (Haken, Punkt, Strich) liegen als eigene
SVG unter quelle/assets/.

Aufruf:  python3 -I werkzeug/erzeugen.py [--pruefen]
--pruefen erzeugt in den Arbeitsspeicher und vergleicht mit den Dateien im
Repo (Exit 1 bei Abweichung), ohne etwas zu schreiben.
"""

import colorsys
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
THEMA = REPO / "Querencia-Klassisch"

QUELLEN = {
    "gtk-4.0": ("libgtk-4.so.1", "/org/gtk/libgtk/theme/Default/Default-light.css",
                REPO / "quelle" / "gtk4-klassisch.css"),
    "gtk-3.0": ("libgtk-3.so.0", "/org/gtk/libgtk/theme/Adwaita/gtk-contained.css",
                REPO / "quelle" / "gtk3-klassisch.css"),
}

# Feste Zuordnungen (Grundthema -> Querencia-Klassisch). Alles Übrige, was
# nicht zur blauen Familie gehört, bleibt wie im Grundthema.
FARBEN = {
    "#f6f5f4": "#f2f1f0",   # Fenstergrund (Ambiance bg_color)
    "#2e3436": "#3c3c3c",   # Schrift (Ambiance text_color, Panel)
    "#cdc7c2": "#c7c2be",   # Rahmen hell (Panelmenüs, Programme)
    "#929595": "#8f8a85",   # deaktivierte Schrift
    "#2ec27e": "#f07746",   # GTK 4: Ablageziel beim Ziehen (drop) im Akzent
    "#3584e4": "#f07746",   # Akzent genau (die Drehung träfe #f17948)
}

AKZENT_H = 17.4 / 360  # Farbton von #F07746


def lib_pfad(name: str) -> str:
    aus = subprocess.run(["ldconfig", "-p"], capture_output=True, text=True, check=True).stdout
    for zeile in aus.splitlines():
        teile = zeile.strip().split()
        if teile and teile[0] == name and "x86-64" in zeile:
            return teile[-1]
    raise SystemExit(f"erzeugen: {name} nicht gefunden")


def grundthema(lib: str, pfad: str) -> str:
    return subprocess.run(["gresource", "extract", lib_pfad(lib), pfad],
                          capture_output=True, text=True, check=True).stdout


def blau_zu_orange(r: int, g: int, b: int):
    """Blaue Akzentfamilie (Farbton 190-235°, gesättigt) auf den Akzent drehen;
    Helligkeit leicht anheben, damit #3584e4 genau auf #f07746 fällt."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if not (190 / 360 <= h <= 235 / 360 and s >= 0.3 and 0.08 < l < 0.97):
        return None
    l2 = min(0.97, l + 0.061)
    s2 = min(1.0, s * 1.118)
    r2, g2, b2 = colorsys.hls_to_rgb(AKZENT_H, l2, s2)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def farbe_hex(m: re.Match) -> str:
    alt = m.group(0).lower()
    if alt in FARBEN:
        return FARBEN[alt]
    r, g, b = (int(alt[i:i + 2], 16) for i in (1, 3, 5))
    neu = blau_zu_orange(r, g, b)
    return "#%02x%02x%02x" % neu if neu else m.group(0)


def farbe_rgba(m: re.Match) -> str:
    r, g, b = int(m.group(2)), int(m.group(3)), int(m.group(4))
    alt = "#%02x%02x%02x" % (r, g, b)
    if alt in FARBEN:
        neu = FARBEN[alt]
        r2, g2, b2 = (int(neu[i:i + 2], 16) for i in (1, 3, 5))
    else:
        o = blau_zu_orange(r, g, b)
        if not o:
            return m.group(0)
        r2, g2, b2 = o
    if m.group(1) == "rgba":
        return f"rgba({r2}, {g2}, {b2}, {m.group(5)})"
    return f"rgb({r2}, {g2}, {b2})"


HEX = re.compile(r"#[0-9a-fA-F]{6}\b")
RGBA = re.compile(r"\b(rgba?)\((\d+), (\d+), (\d+)(?:, ([0-9.]+))?\)")
RADIUS = re.compile(r"(border(?:-[a-z]+)*-radius:\s*)([^;}]+)")
GROSSE_ECKEN = {"5px", "5.5px", "6px", "7px", "8px", "9px", "10px"}


def ecken(m: re.Match) -> str:
    werte = ["3px" if w in GROSSE_ECKEN else w for w in m.group(2).split()]
    return m.group(1) + " ".join(werte)


def bloecke(css: str):
    """Teilt CSS auf oberster Ebene in Kommentare und Regeln (mit
    verschachtelten @-Blöcken wie @keyframes)."""
    i, n = 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            j = css.index("*/", i) + 2
            yield css[i:j]
            i = j
            continue
        if css[i].isspace():
            j = i
            while j < n and css[j].isspace():
                j += 1
            yield css[i:j]
            i = j
            continue
        j = css.find("{", i)
        semi = css.find(";", i)
        if semi != -1 and (j == -1 or semi < j):   # @import u. ä.
            yield css[i:semi + 1]
            i = semi + 1
            continue
        tiefe, k = 0, j
        while k < n:
            if css[k] == "{":
                tiefe += 1
            elif css[k] == "}":
                tiefe -= 1
                if tiefe == 0:
                    break
            k += 1
        yield css[i:k + 1]
        i = k + 1


def ohne_backdrop(block: str) -> str:
    if block.startswith("@") or "{" not in block:
        return block
    kopf, rumpf = block.split("{", 1)
    waehler = [w.strip() for w in kopf.split(",")]
    bleiben = [w for w in waehler if ":backdrop" not in w]
    if not bleiben:
        return ""
    return ", ".join(bleiben) + " {" + rumpf


def assets(css: str) -> str:
    # GTK 3: PNG-Ersatz der Symbolbilder -> eigene SVG
    css = re.sub(r'url\("assets/([a-z-]+-symbolic)\.symbolic\.png"\)', r'url("assets/\1.svg")', css)
    # Schiebereglerbilder des Grundthemas (Markierungen) entfallen; die eigene
    # Schicht zeichnet den Regler mit Verlauf.
    css = re.sub(r'-gtk-scaled\(url\("assets/slider-[^"]+"\), url\("assets/slider-[^"]+"\)\)', "none", css)
    css = re.sub(r'url\("assets/slider-[^"]+"\)', "none", css)
    return css


def erzeuge(ordner: str) -> tuple[str, str]:
    lib, pfad, schicht = QUELLEN[ordner]
    basis = grundthema(lib, pfad)
    teile = []
    for b in bloecke(basis):
        b = ohne_backdrop(b)
        if not b:
            continue
        b = HEX.sub(farbe_hex, b)
        b = RGBA.sub(farbe_rgba, b)
        b = RADIUS.sub(ecken, b)
        teile.append(b)
    umgesetzt = assets("".join(teile))
    umgesetzt = re.sub(r"\n{3,}", "\n\n", umgesetzt)
    summe = hashlib.sha256(basis.encode()).hexdigest()
    kopf = (
        "/* Querencia-Klassisch – GTK-Thema für Querencia Desktop (" + ordner + ").\n"
        " * ERZEUGT von werkzeug/erzeugen.py – nicht von Hand ändern.\n"
        " *\n"
        " * Teil 1: eingebautes GTK-Thema (" + pfad + ",\n"
        " *         GTK, LGPL-2.1-or-later) mit Querencia-Farben, 3-px-Ecken und\n"
        " *         ohne :backdrop; SHA256 der Grundlage " + summe + ".\n"
        " * Teil 2: " + schicht.relative_to(REPO).as_posix() + " (GPL-3.0-or-later).\n"
        " */\n\n"
    )
    trenner = "\n/* ==== Teil 2: " + schicht.name + " ==== */\n\n"
    return kopf + umgesetzt.strip() + "\n" + trenner + schicht.read_text(), summe


def main() -> int:
    pruefen = "--pruefen" in sys.argv[1:]
    abweichung = 0
    for ordner in QUELLEN:
        css, summe = erzeuge(ordner)
        ziel = THEMA / ordner / "gtk.css"
        if pruefen:
            if not ziel.exists() or ziel.read_text() != css:
                print(f"erzeugen: {ziel.relative_to(REPO)} weicht ab (Grundlage {summe[:16]})")
                abweichung = 1
            continue
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(css)
        adir = ziel.parent / "assets"
        if adir.exists():
            shutil.rmtree(adir)
        shutil.copytree(REPO / "quelle" / "assets", adir)
        print(f"erzeugen: {ziel.relative_to(REPO)} ({len(css)} Bytes, Grundlage {summe[:16]})")
    return abweichung


if __name__ == "__main__":
    sys.exit(main())
