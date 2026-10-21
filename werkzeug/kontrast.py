#!/usr/bin/env python3
"""Kontrast-Check der Textfarben von Querencia-Klassisch (WCAG 2.x).

Prüft jedes Schrift/Grund-Paar der Thema-Schicht gegen AA für normalen
Text (4,5:1), getrennt für die helle Fassung (gtk-4.0/gtk.css) und die
dunkle (gtk-4.0/gtk-dark.css, Thema 0.2). Jedes Paar muss in der jeweils
erzeugten Datei vorkommen, damit die Tabelle nicht vom Thema abweicht. Deaktivierte Elemente sind nach
WCAG 1.4.3 ausgenommen und stehen nur zur Information da.

Aufruf:  python3 -I werkzeug/kontrast.py [--markdown]
Exit 1, wenn ein Pflichtpaar AA verfehlt oder eine Farbe im Thema fehlt.
"""

import sys
from pathlib import Path

GTK4 = Path(__file__).resolve().parent.parent / "Querencia-Klassisch" / "gtk-4.0"
# Helle Fassung: nur der Teil vor dem Dunkelblock (@media), damit eine Farbe
# der dunklen Fassung nicht als „im hellen Thema“ zählt.
CSS_HELL = (GTK4 / "gtk.css").read_text().lower().split("/* ==== teil 3: dunkle fassung")[0]
CSS_DUNKEL = (GTK4 / "gtk-dark.css").read_text().lower()

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
    # 0.2.1
    ("Fehlerschrift (label.error) auf Fenstergrund", "#cc0000", "#f2f1f0", True),
    ("Fehlerschrift auf Menügrund", "#cc0000", "#f5f4f2", True),
    ("Fehlerschrift in Ansicht und Eingabefeld", "#cc0000", "#ffffff", True),
    ("Tastenkürzel im Menü (75 %)", "#3c3c3c@0.75", "#f5f4f2", True),
    ("Tastenkürzel auf Auswahl, oben", "#1a1a1a", "#f6a179", True),
    ("Tastenkürzel auf Auswahl, unten", "#1a1a1a", "#f07746", True),
    ("@sidebar_fg_color auf @sidebar_bg_color", "#3c3c3c", "#f5f4f2", True),
    ("@menu_fg_color auf @menu_bg_color", "#3c3c3c", "#f5f4f2", True),
    # Nur zur Information
    ("Deaktivierte Schrift (WCAG-Ausnahme)", "#a5a09a", "#f2f1f0", False),
    ("Vergleich: Tastenkürzel bis 0.2 (55 %)", "#3c3c3c@0.55", "#f5f4f2", False),
    ("Tastenkürzel auf Auswahl, gedrückt (Augenblick)", "#1a1a1a", "#e2683a", False),
    ("Vergleich: weiße Auswahlschrift (Ambiance, Panelmenü)", "#ffffff", "#f07746", False),
    ("Vergleich: weiße Schrift, Verlauf oben", "#ffffff", "#f6a179", False),
]

# Dunkle Fassung (Thema 0.2, Ambiance dunkel)
PAARE_DUNKEL = [
    ("Fensterschrift auf Fenstergrund", "#dfdbd2", "#3c3b37", True),
    ("Werkzeugleiste, Verlauf oben", "#dfdbd2", "#45443f", True),
    ("Menüeintrag auf Menügrund", "#dfdbd2", "#353430", True),
    ("Text in Ansichten und Feldern", "#f2f1f0", "#2b2a27", True),
    ("Zebrazeile", "#f2f1f0", "#353430", True),
    ("Seitenleiste", "#f2f1f0", "#34332f", True),
    ("Auswahl, Verlauf oben", "#1a1a1a", "#f6a179", True),
    ("Auswahl, Verlauf unten (Akzent)", "#1a1a1a", "#f07746", True),
    ("Auswahl ohne Fokus (dunkles Beige)", "#f2f1f0", "#6b6153", True),
    ("Empfohlene Aktion, oben", "#1a1a1a", "#f8ad88", True),
    ("Empfohlene Aktion, unten", "#1a1a1a", "#f07746", True),
    ("Gefährliche Aktion, oben", "#ffffff", "#cc3b35", True),
    ("Gefährliche Aktion, unten", "#ffffff", "#b02a24", True),
    ("Knopf, Verlauf oben", "#dfdbd2", "#57554f", True),
    ("Knopf, Verlauf unten", "#dfdbd2", "#4a4843", True),
    ("Knopf überfahren, oben", "#dfdbd2", "#5f5d57", True),
    ("Gedrückter Knopf", "#dfdbd2", "#33322e", True),
    ("Spaltenkopf, oben", "#dfdbd2", "#55534d", True),
    ("Spaltenkopf, unten", "#dfdbd2", "#46443f", True),
    ("Reiter inaktiv, Verlauf oben", "#bdb7b1", "#36352f", True),
    ("Reiter inaktiv, Verlauf unten", "#bdb7b1", "#2f2e2a", True),
    ("Schalter aus (Textteil)", "#bdb7b1", "#2f2e2a", True),
    ("Schalter an (Textteil)", "#1a1a1a", "#f07746", True),
    ("Tooltip", "#ffffff", "#1e1e1e", True),
    ("Verweis auf Fenstergrund", "#f6a179", "#3c3b37", True),
    ("Verweis auf Ansicht", "#f6a179", "#2b2a27", True),
    ("Besuchter Verweis", "#e5a383", "#3c3b37", True),
    ("Verweis überfahren", "#fbbb9a", "#3c3b37", True),
    ("Fehlerleiste", "#ffffff", "#c7342a", True),
    ("Info-/Frageleiste", "#dfdbd2", "#4d4528", True),
    ("Warnleiste", "#dfdbd2", "#5a4228", True),
    ("Kopfleiste (nur GTK-Dialoge), unten", "#dfdbd2", "#3c3b37", True),
    ("Gedimmter Text (dim-label, 75 %) auf Fenstergrund", "#dfdbd2@0.75", "#3c3b37", True),
    ("Platzhalter (75 %) im Eingabefeld", "#f2f1f0@0.75", "#2b2a27", True),
    ("Skalenmarken", "#b3aea7", "#3c3b37", True),
    # 0.2.1
    ("Fehlerschrift (label.error) auf Fenstergrund und Dialog", "#ed8b85", "#3c3b37", True),
    ("Fehlerschrift auf Menügrund", "#ed8b85", "#353430", True),
    ("Fehlerschrift in Ansicht und Eingabefeld", "#ed8b85", "#2b2a27", True),
    ("Tastenkürzel im Menü (75 %)", "#dfdbd2@0.75", "#353430", True),
    ("Tastenkürzel auf Auswahl, oben", "#1a1a1a", "#f6a179", True),
    ("Tastenkürzel auf Auswahl, unten", "#1a1a1a", "#f07746", True),
    ("@sidebar_fg_color auf @sidebar_bg_color", "#e8e6e3", "#353430", True),
    ("@menu_fg_color auf @menu_bg_color", "#dfdbd2", "#353430", True),
    # Nur zur Information
    ("Deaktivierte Schrift (WCAG-Ausnahme)", "#858079", "#3c3b37", False),
    ("Deaktivierte Schrift im Feld (WCAG-Ausnahme)", "#858079", "#353430", False),
    ("Vergleich: Fehlerschrift bis 0.2 (#cc0000)", "#cc0000", "#3c3b37", False),
    ("Vergleich: Tastenkürzel bis 0.2 (55 %)", "#dfdbd2@0.55", "#353430", False),
    ("Vergleich: weiße Auswahlschrift (Ambiance)", "#ffffff", "#f07746", False),
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


def im_thema(farbe: str, css: str) -> bool:
    if "@" in farbe:
        farbe, a = farbe.split("@")
        # opacity (dim-label) oder relative Farbe (Tastenkürzel, 0.2.1)
        return farbe in css and (f"opacity: {a}" in css or f"alpha * {a})" in css)
    return ERSATZ.get(farbe, farbe) in css


def tabelle(titel: str, paare: list, css: str, md: bool) -> int:
    fehler = 0
    if md:
        print(f"**{titel}**\n")
        print("| Element | Schrift | Grund | Kontrast | AA (4,5:1) |")
        print("|---|---|---|---|---|")
    else:
        print(f"== {titel}")
    for name, fg, bg, pflicht in paare:
        k = verhaeltnis(mischen(fg, bg), bg)
        ok = k >= 4.5
        fehlt = [f for f in (fg, bg) if not im_thema(f, css)]
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
    if md:
        print()
    return fehler


def main() -> int:
    md = "--markdown" in sys.argv[1:]
    fehler = tabelle("Hell (gtk.css)", PAARE, CSS_HELL, md)
    fehler |= tabelle("Dunkel (gtk-dark.css und @media-Block in gtk.css)", PAARE_DUNKEL, CSS_DUNKEL, md)
    return fehler


if __name__ == "__main__":
    sys.exit(main())
