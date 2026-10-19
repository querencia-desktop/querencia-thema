#!/usr/bin/env python3
"""Kontrast-Check der Textfarben von Querencia-Klassisch (WCAG 2.x).

Prüft jedes Schrift/Grund-Paar der Thema-Schicht gegen AA für normalen
Text (4,5:1). Jedes Paar muss in der erzeugten gtk-4.0/gtk.css vorkommen,
damit die Tabelle nicht vom Thema abweicht. Deaktivierte Elemente sind nach
WCAG 1.4.3 ausgenommen und stehen nur zur Information da.

Aufruf:  python3 -I werkzeug/kontrast.py [--markdown]
Exit 1, wenn ein Pflichtpaar AA verfehlt oder eine Farbe im Thema fehlt.
"""

import sys
from pathlib import Path

CSS = (Path(__file__).resolve().parent.parent / "Querencia-Klassisch" / "gtk-4.0" / "gtk.css").read_text().lower()

# (Element, Schrift, Grund, Pflicht)
PAARE = [
    ("Fensterschrift auf Fenstergrund", "#3c3c3c", "#f2f1f0", True),
    ("Menüeintrag auf Menügrund", "#3c3c3c", "#f5f4f2", True),
    ("Text in Ansichten und Feldern", "#1a1a1a", "#ffffff", True),
    ("Zebrazeile", "#1a1a1a", "#f5f4f2", True),
    ("Auswahl, Verlauf oben", "#1a1a1a", "#f6a179", True),
    ("Auswahl, Verlauf unten (Akzent)", "#1a1a1a", "#f07746", True),
    ("Auswahl ohne Fokus (Ambiance-Beige)", "#1a1a1a", "#c6b9a6", True),
    ("Empfohlene Aktion, oben", "#1a1a1a", "#f8ad88", True),
    ("Empfohlene Aktion, unten", "#1a1a1a", "#f07746", True),
    ("Gefährliche Aktion, oben", "#ffffff", "#cc3b35", True),
    ("Gefährliche Aktion, unten", "#ffffff", "#b02a24", True),
    ("Knopf, Verlauf unten", "#3c3c3c", "#e9e6e2", True),
    ("Gedrückter Knopf", "#3c3c3c", "#d6d2cd", True),
    ("Spaltenkopf", "#3c3c3c", "#ecebe9", True),
    ("Reiter inaktiv, Verlauf unten", "#5a5652", "#dedad6", True),
    ("Tooltip", "#ffffff", "#1e1e1e", True),
    ("Verweis auf Fenstergrund", "#b33c0b", "#f2f1f0", True),
    ("Verweis auf Weiß", "#b33c0b", "#ffffff", True),
    ("Besuchter Verweis", "#8a3a1c", "#f2f1f0", True),
    ("Fehlerleiste", "#ffffff", "#c7342a", True),
    ("Info-/Frageleiste", "#3c3c3c", "#fcf3c8", True),
    ("Warnleiste", "#3c3c3c", "#fbdcb5", True),
    ("Kopfleiste (nur GTK-Dialoge), unten", "#3c3c3c", "#d8d4d0", True),
    ("Schalter an (Textteil)", "#1a1a1a", "#f07746", True),
    ("Gedimmter Text (dim-label, 75 %) auf Fenstergrund", "#3c3c3c@0.75", "#f2f1f0", True),
    ("Platzhalter (75 %) im Eingabefeld", "#1a1a1a@0.75", "#ffffff", True),
    # Nur zur Information
    ("Deaktivierte Schrift (WCAG-Ausnahme)", "#a5a09a", "#f2f1f0", False),
    ("Vergleich: weiße Auswahlschrift (Ambiance, Panelmenü)", "#ffffff", "#f07746", False),
    ("Vergleich: weiße Schrift, Verlauf oben", "#ffffff", "#f6a179", False),
]

# rgba(30, 30, 30, 0.95) über dem hellen Grund ergibt etwa #1e1e1e;
# in der CSS steht der rgba-Wert.
ERSATZ = {"#1e1e1e": "rgba(30, 30, 30, 0.95)"}


def kanal(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def leucht(h: str) -> float:
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * kanal(r) + 0.7152 * kanal(g) + 0.0722 * kanal(b)


def verhaeltnis(a: str, b: str) -> float:
    la, lb = sorted((leucht(a), leucht(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mischen(fg: str, bg: str) -> str:
    """'#rrggbb@deckkraft' über bg gemischt (GTK-opacity)."""
    if "@" not in fg:
        return fg
    farbe, a = fg.split("@")
    a = float(a)
    k = [round(a * int(farbe[i:i + 2], 16) + (1 - a) * int(bg[i:i + 2], 16)) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(k)


def im_thema(farbe: str) -> bool:
    if "@" in farbe:
        farbe, a = farbe.split("@")
        return farbe in CSS and f"opacity: {a}" in CSS
    return ERSATZ.get(farbe, farbe) in CSS


def main() -> int:
    md = "--markdown" in sys.argv[1:]
    fehler = 0
    if md:
        print("| Element | Schrift | Grund | Kontrast | AA (4,5:1) |")
        print("|---|---|---|---|---|")
    for name, fg, bg, pflicht in PAARE:
        k = verhaeltnis(mischen(fg, bg), bg)
        ok = k >= 4.5
        fehlt = [f for f in (fg, bg) if not im_thema(f)]
        if pflicht and (not ok or fehlt):
            fehler = 1
        urteil = ("bestanden" if ok else "verfehlt") if pflicht else ("(Info) " + ("erfüllt" if ok else "unter AA"))
        if fehlt:
            urteil += " – nicht im Thema: " + ", ".join(fehlt)
        k_txt = f"{k:.1f}:1".replace(".", ",")
        if md:
            print(f"| {name} | `{fg}` | `{bg}` | {k_txt} | {urteil} |")
        else:
            print(f"{k_txt:>8}  {urteil:<12}  {fg} auf {bg}  {name}")
    return fehler


if __name__ == "__main__":
    sys.exit(main())
