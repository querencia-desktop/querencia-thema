#!/usr/bin/env python3
"""Erzeugt Querencia-Klassisch/gtk-4.0/gtk.css, gtk-4.0/gtk-dark.css,
gtk-3.0/gtk.css und gtk-3.0/gtk-dark.css.

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

Dunkle Fassung (Thema 0.2): Grundlage ist das dunkle eingebaute Thema
(Default-dark.css bzw. gtk-contained-dark.css) mit denselben Schritten und
den Farben aus FARBEN_DUNKEL; übrige Grautöne bekommen den warmen
Ambiance-Ton. Die helle Schicht wird über quelle/dunkel-zuordnung.txt
umgefärbt (jede Farbe braucht dort eine Zeile), danach folgt
quelle/gtk4-dunkel.css bzw. quelle/gtk3-dunkel.css. Das Ergebnis steht in
gtk-dark.css und, nur für GTK 4, zusätzlich in gtk.css als Block
`@media (prefers-color-scheme: dark)`: GTK 4.22 lädt gtk-dark.css nur bei
GTK_THEME=…:dark oder gtk-application-prefer-dark-theme, das Farbschema aus
dem Settings-Portal wirkt nur über die Medienabfrage (docs/aufbau.md).

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
    "gtk-4.0": {
        "lib": "libgtk-4.so.1",
        "hell": "/org/gtk/libgtk/theme/Default/Default-light.css",
        "dunkel": "/org/gtk/libgtk/theme/Default/Default-dark.css",
        "schicht": REPO / "quelle" / "gtk4-klassisch.css",
        "schicht_dunkel": REPO / "quelle" / "gtk4-dunkel.css",
        "medien": True,   # GTK 4 kennt @media (prefers-color-scheme)
    },
    "gtk-3.0": {
        "lib": "libgtk-3.so.0",
        "hell": "/org/gtk/libgtk/theme/Adwaita/gtk-contained.css",
        "dunkel": "/org/gtk/libgtk/theme/Adwaita/gtk-contained-dark.css",
        "schicht": REPO / "quelle" / "gtk3-klassisch.css",
        "schicht_dunkel": REPO / "quelle" / "gtk3-dunkel.css",
        "medien": False,
    },
}
ZUORDNUNG = REPO / "quelle" / "dunkel-zuordnung.txt"

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

# Dunkles Grundthema -> Querencia-Klassisch dunkel (Ambiance-Palette).
FARBEN_DUNKEL = {
    "#353535": "#3c3b37",   # Fenstergrund (Ambiance)
    "#2d2d2d": "#2b2a27",   # Ansicht
    "#eeeeec": "#dfdbd2",   # Schrift (Ambiance)
    "#1b1b1b": "#23221f",   # Rahmen
    "#919190": "#858079",   # deaktivierte Schrift
    "#2ec27e": "#f07746",   # GTK 4: Ablageziel beim Ziehen im Akzent
    "#3584e4": "#f07746",   # Akzent genau
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


def warm(r: int, g: int, b: int):
    """Neutrales Grau des dunklen Grundthemas in den warmen Ambiance-Ton
    (#353535-Stufe -> #3c3b37-Art); Weiß, Schwarz und Farben bleiben."""
    if max(r, g, b) - min(r, g, b) > 3:
        return None
    v = round((r + g + b) / 3)
    if not 8 < v < 248:
        return None
    return v, v - round(v * 0.02), v - round(v * 0.07)


def zuordnen(r: int, g: int, b: int, farben: dict, waerme: bool):
    alt = "#%02x%02x%02x" % (r, g, b)
    if alt in farben:
        neu = farben[alt]
        return tuple(int(neu[i:i + 2], 16) for i in (1, 3, 5))
    neu = blau_zu_orange(r, g, b)
    if neu is None and waerme:
        neu = warm(r, g, b)
    return neu


def farbe_hex(m: re.Match, farben: dict, waerme: bool) -> str:
    alt = m.group(0).lower()
    neu = zuordnen(*(int(alt[i:i + 2], 16) for i in (1, 3, 5)), farben, waerme)
    return "#%02x%02x%02x" % neu if neu else m.group(0)


def farbe_rgba(m: re.Match, farben: dict, waerme: bool) -> str:
    neu = zuordnen(int(m.group(2)), int(m.group(3)), int(m.group(4)), farben, waerme)
    if not neu:
        return m.group(0)
    r2, g2, b2 = neu
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


def grund_umsetzen(basis: str, farben: dict, waerme: bool) -> str:
    teile = []
    for b in bloecke(basis):
        b = ohne_backdrop(b)
        if not b:
            continue
        b = HEX.sub(lambda m: farbe_hex(m, farben, waerme), b)
        b = RGBA.sub(lambda m: farbe_rgba(m, farben, waerme), b)
        b = RADIUS.sub(ecken, b)
        teile.append(b)
    umgesetzt = assets("".join(teile))
    return re.sub(r"\n{3,}", "\n\n", umgesetzt).strip() + "\n"


# ------------------------------------------------- helle Schicht -> dunkel

# rgb(from currentColor …) ist eine relative Farbe ohne festen Wert (0.2.1:
# Tastenkürzel im Menü) und braucht keine Zuordnung.
FARBTOKEN = re.compile(r"#[0-9a-fA-F]{6}\b|rgba?\((?!\s*from\b)[^)]*\)")
DEKLARATION = re.compile(r"([a-z-]+)(\s*:\s*)([^;{}]+)")


def norm(farbe: str) -> str:
    return re.sub(r"\s+", "", farbe.lower())


def css_farbe(farbe: str) -> str:
    return farbe.replace(",", ", ") if farbe.startswith("rgb") else farbe


def zuordnung_lesen() -> tuple[dict, set]:
    tabelle, akzent = {}, set()
    for nr, zeile in enumerate(ZUORDNUNG.read_text().splitlines(), 1):
        teile = zeile.split()
        if not teile or teile[0].startswith("#"):
            continue
        if teile[0] == "akzent":
            akzent.add(norm(teile[1]))
            continue
        if len(teile) < 3 or teile[0] not in ("*", "schrift", "flaeche", "verlauf", "rand", "schatten"):
            raise SystemExit(f"erzeugen: {ZUORDNUNG.name}:{nr}: unlesbar: {zeile}")
        schluessel = (teile[0], norm(teile[1]))
        if schluessel in tabelle:
            raise SystemExit(f"erzeugen: {ZUORDNUNG.name}:{nr}: doppelt: {zeile}")
        tabelle[schluessel] = css_farbe(norm(teile[2]))
    return tabelle, akzent


def rolle(eigenschaft: str, wert: str):
    if eigenschaft == "color":
        return "schrift"
    if eigenschaft.startswith(("border", "outline")):
        return "rand"
    if eigenschaft == "box-shadow":
        return "schatten"
    if eigenschaft.startswith("background"):
        return "verlauf" if "gradient" in wert else "flaeche"
    return None


def schicht_dunkel(css: str, name: str, tabelle: dict, akzent: set, benutzt: set) -> str:
    """Färbt die helle Schicht nach der Zuordnung um. Regeln mit einem
    Akzent im Hintergrund (Auswahl, empfohlene/gefährliche Aktion) bleiben
    unverändert: ihre Schrift steht auf Orange oder Rot."""
    fehlt = []

    def regel(block: str) -> str:
        if block.startswith(("/*", "@")) or "{" not in block:
            return block
        kopf, rumpf = block.split("{", 1)
        for e, _, w in DEKLARATION.findall(rumpf):
            if e.startswith("background") and any(norm(t) in akzent for t in FARBTOKEN.findall(w)):
                return block

        def deklaration(m: re.Match) -> str:
            eig, wert = m.group(1), m.group(3)
            r = rolle(eig, wert)

            def farbe(t: re.Match) -> str:
                k = norm(t.group(0))
                for schluessel in ((r, k), ("*", k)):
                    if schluessel in tabelle:
                        benutzt.add(schluessel)
                        return tabelle[schluessel]
                if k in akzent:
                    return t.group(0)
                fehlt.append(f"{r or eig} {k} ({kopf.strip()[:50]})")
                return t.group(0)
            return m.group(1) + m.group(2) + FARBTOKEN.sub(farbe, wert)
        return kopf + "{" + DEKLARATION.sub(deklaration, rumpf)

    aus = "".join(regel(b) for b in bloecke(css))
    if fehlt:
        raise SystemExit(f"erzeugen: {name}: Farben ohne Dunkel-Zuordnung in {ZUORDNUNG.name}:\n  "
                         + "\n  ".join(dict.fromkeys(fehlt)))
    return aus


def erzeuge(ordner: str, tabelle: dict, akzent: set, benutzt: set) -> dict:
    q = QUELLEN[ordner]
    schicht, schicht_d = q["schicht"], q["schicht_dunkel"]
    basis = grundthema(q["lib"], q["hell"])
    basis_d = grundthema(q["lib"], q["dunkel"])
    summe = hashlib.sha256(basis.encode()).hexdigest()
    summe_d = hashlib.sha256(basis_d.encode()).hexdigest()
    rel = lambda p: p.relative_to(REPO).as_posix()   # noqa: E731
    kopf = (
        "/* Querencia-Klassisch – GTK-Thema für Querencia Desktop (" + ordner + ").\n"
        " * ERZEUGT von werkzeug/erzeugen.py – nicht von Hand ändern.\n"
        " *\n"
        " * Teil 1: eingebautes GTK-Thema (" + q["hell"] + ",\n"
        " *         GTK, LGPL-2.1-or-later) mit Querencia-Farben, 3-px-Ecken und\n"
        " *         ohne :backdrop; SHA256 der Grundlage " + summe + ".\n"
        " * Teil 2: " + rel(schicht) + " (GPL-3.0-or-later).\n"
        + (" * Teil 3: dunkle Fassung wie gtk-dark.css als Block\n"
           " *         @media (prefers-color-scheme: dark).\n" if q["medien"] else "")
        + " */\n\n"
    )
    trenner = "\n/* ==== Teil 2: " + schicht.name + " ==== */\n\n"
    hell = grund_umsetzen(basis, FARBEN, False).strip() + "\n" + trenner + schicht.read_text()
    dunkel = (
        grund_umsetzen(basis_d, FARBEN_DUNKEL, True).strip() + "\n"
        + "\n/* ==== Teil 2: " + schicht.name + ", umgefärbt nach " + ZUORDNUNG.name + " ==== */\n\n"
        + schicht_dunkel(schicht.read_text(), schicht.name, tabelle, akzent, benutzt)
        + "\n/* ==== Teil 3: " + schicht_d.name + " ==== */\n\n"
        + schicht_d.read_text()
    )
    kopf_d = (
        "/* Querencia-Klassisch dunkel – GTK-Thema für Querencia Desktop (" + ordner + ").\n"
        " * ERZEUGT von werkzeug/erzeugen.py – nicht von Hand ändern.\n"
        " *\n"
        " * Teil 1: eingebautes GTK-Thema (" + q["dunkel"] + ",\n"
        " *         GTK, LGPL-2.1-or-later) mit Querencia-Farben (Ambiance dunkel),\n"
        " *         3-px-Ecken und ohne :backdrop; SHA256 der Grundlage " + summe_d + ".\n"
        " * Teil 2: " + rel(schicht) + ", umgefärbt nach " + rel(ZUORDNUNG) + ".\n"
        " * Teil 3: " + rel(schicht_d) + " (alle GPL-3.0-or-later).\n"
        " */\n\n"
    )
    dateien = {"gtk-dark.css": kopf_d + dunkel}
    if q["medien"]:
        hell += ("\n/* ==== Teil 3: dunkle Fassung (gleich gtk-dark.css) ==== */\n\n"
                 "@media (prefers-color-scheme: dark) {\n\n" + dunkel + "\n}\n")
    dateien["gtk.css"] = kopf + hell
    return {"dateien": dateien, "summe": summe, "summe_d": summe_d}


def main() -> int:
    pruefen = "--pruefen" in sys.argv[1:]
    abweichung = 0
    tabelle, akzent = zuordnung_lesen()
    benutzt = set()
    for ordner in QUELLEN:
        e = erzeuge(ordner, tabelle, akzent, benutzt)
        for datei, css in e["dateien"].items():
            ziel = THEMA / ordner / datei
            if pruefen:
                if not ziel.exists() or ziel.read_text() != css:
                    print(f"erzeugen: {ziel.relative_to(REPO)} weicht ab (Grundlage {e['summe'][:16]}/{e['summe_d'][:16]})")
                    abweichung = 1
                continue
            ziel.parent.mkdir(parents=True, exist_ok=True)
            ziel.write_text(css)
            print(f"erzeugen: {ziel.relative_to(REPO)} ({len(css)} Bytes, Grundlage {e['summe'][:16]}/{e['summe_d'][:16]})")
        if not pruefen:
            adir = THEMA / ordner / "assets"
            if adir.exists():
                shutil.rmtree(adir)
            shutil.copytree(REPO / "quelle" / "assets", adir)
    for r, k in sorted(set(tabelle) - benutzt):
        print(f"erzeugen: Hinweis: Zuordnung {r} {k} wird nicht gebraucht")
    return abweichung


if __name__ == "__main__":
    sys.exit(main())
