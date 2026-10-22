#!/usr/bin/env python3
"""Kontrast-Check der Textfarben von Querencia-Klassisch (WCAG 2.x).

Prüft jedes Schrift/Grund-Paar der Thema-Schicht gegen AA für normalen
Text (4,5:1), getrennt für die helle Fassung (gtk-4.0/gtk.css) und die
dunkle (gtk-4.0/gtk-dark.css, Thema 0.2). Jedes Paar muss in der jeweils
erzeugten Datei vorkommen, damit die Tabelle nicht vom Thema abweicht. Deaktivierte Elemente sind nach
WCAG 1.4.3 ausgenommen und stehen nur zur Information da.

Seit 0.2.2 zusätzlich:
- GTK 3 (gtk-3.0/gtk.css und gtk-dark.css): alle Paare der GTK-4-Tabellen,
  deren Farben auch in GTK 3 stehen, dazu die Paare, in denen GTK 3 andere
  Farben nimmt (PAARE_GTK3*);
- labwc (labwc/*/themerc, themerc-override-dunkel): Fenstertitel, Fenstermenü
  und Fensterwechsler hell und dunkel; Titelknöpfe gegen ihre Fläche mit
  3:1 (WCAG 1.4.11, Farben aus werkzeug/labwc-knoepfe.py).

Aufruf:  python3 -I werkzeug/kontrast.py [--markdown]
Exit 1, wenn ein Pflichtpaar AA verfehlt oder eine Farbe im Thema fehlt.
"""

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GTK4 = REPO / "Querencia-Klassisch" / "gtk-4.0"
GTK3 = REPO / "Querencia-Klassisch" / "gtk-3.0"
# Helle Fassung: nur der Teil vor dem Dunkelblock (@media), damit eine Farbe
# der dunklen Fassung nicht als „im hellen Thema“ zählt.
CSS_HELL = (GTK4 / "gtk.css").read_text().lower().split("/* ==== teil 3: dunkle fassung")[0]
CSS_DUNKEL = (GTK4 / "gtk-dark.css").read_text().lower()
CSS3_HELL = (GTK3 / "gtk.css").read_text().lower()
CSS3_DUNKEL = (GTK3 / "gtk-dark.css").read_text().lower()
LABWC_HELL = (REPO / "labwc" / "Querencia-Klassisch" / "themerc").read_text().lower()
LABWC_DUNKEL = (REPO / "labwc" / "Querencia-Klassisch-Dunkel" / "themerc").read_text().lower()



def themerc(*pfade: Path) -> str:
    """Wirksame Werte (spätere Datei gewinnt, wie theme_init mit
    themerc-override) als Text key: wert."""
    werte = {}
    for p in pfade:
        for zeile in p.read_text().lower().splitlines():
            if ":" in zeile and not zeile.lstrip().startswith("#"):
                k, w = zeile.split(":", 1)
                werte[k.strip()] = w.strip()
    return "\n".join(f"{k}: {w}" for k, w in werte.items())


# Override: wirksam ist das helle Theme plus themerc-override-dunkel
LABWC_OVERRIDE = themerc(REPO / "labwc" / "Querencia-Klassisch" / "themerc", REPO / "labwc" / "themerc-override-dunkel")

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
    # 0.2.2
    ("Skalenwert und Skalenmarken (75 %)", "#3c3c3c@0.75", "#f2f1f0", True),
    # Symbole: 3:1 (WCAG 1.4.11)
    ("Pfeil zum Untermenü (75 %)", "#3c3c3c@0.75", "#f5f4f2", True, 3.0),
    ("Schließknopf auf aktivem Reiter (75 %)", "#3c3c3c@0.75", "#f2f1f0", True, 3.0),
    ("Schließknopf auf inaktivem Reiter (75 %), unten", "#5a5652@0.75", "#dedad6", True, 3.0),
    # Nur zur Information
    ("Deaktivierte Schrift (WCAG-Ausnahme)", "#a5a09a", "#f2f1f0", False),
    ("Vergleich: Skalenwert bis 0.2.1 (55 %)", "#3c3c3c@0.55", "#f2f1f0", False),
    ("Vergleich: Pfeil, Schließknopf bis 0.2.1 (30 %)", "#3c3c3c@0.3", "#f2f1f0", False, 3.0),
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
    # 0.2.1
    ("Fehlerschrift (label.error) auf Fenstergrund und Dialog", "#ed8b85", "#3c3b37", True),
    ("Fehlerschrift auf Menügrund", "#ed8b85", "#353430", True),
    ("Fehlerschrift in Ansicht und Eingabefeld", "#ed8b85", "#2b2a27", True),
    ("Tastenkürzel im Menü (75 %)", "#dfdbd2@0.75", "#353430", True),
    ("Tastenkürzel auf Auswahl, oben", "#1a1a1a", "#f6a179", True),
    ("Tastenkürzel auf Auswahl, unten", "#1a1a1a", "#f07746", True),
    ("@sidebar_fg_color auf @sidebar_bg_color", "#e8e6e3", "#353430", True),
    ("@menu_fg_color auf @menu_bg_color", "#dfdbd2", "#353430", True),
    # 0.2.2 (bis 0.2.1 hier „Skalenmarken #b3aea7“: galt nur für Marken ohne
    # Ausrichtung, waagrechte und senkrechte Marken hatten 55 %)
    ("Skalenwert und Skalenmarken (75 %)", "#dfdbd2@0.75", "#3c3b37", True),
    ("Pfeil zum Untermenü (75 %)", "#dfdbd2@0.75", "#353430", True, 3.0),
    ("Schließknopf auf aktivem Reiter (75 %)", "#dfdbd2@0.75", "#3c3b37", True, 3.0),
    ("Schließknopf auf inaktivem Reiter (75 %), unten", "#bdb7b1@0.75", "#2f2e2a", True, 3.0),
    # Nur zur Information
    ("Deaktivierte Schrift (WCAG-Ausnahme)", "#858079", "#3c3b37", False),
    ("Deaktivierte Schrift im Feld (WCAG-Ausnahme)", "#858079", "#353430", False),
    ("Vergleich: Fehlerschrift bis 0.2 (#cc0000)", "#cc0000", "#3c3b37", False),
    ("Vergleich: Tastenkürzel bis 0.2 (55 %)", "#dfdbd2@0.55", "#353430", False),
    ("Vergleich: weiße Auswahlschrift (Ambiance)", "#ffffff", "#f07746", False),
    ("Vergleich: Skalenwert bis 0.2.1 (55 %)", "#dfdbd2@0.55", "#3c3b37", False),
]

# GTK 3: Paare mit eigenen Farben (Grundthema Adwaita 3 statt GTK-4-Default).
# Die Infoleisten sind in GTK 3 für alle Arten gleich gefärbt.
PAARE_GTK3 = [
    ("Infoleiste (alle Arten, Adwaita 3)", "#3c3c3c", "#f1e6d9", True),
    ("Seitenleiste", "#3c3c3c", "#fbfafa", True),
]
PAARE_GTK3_DUNKEL = [
    ("Infoleiste (alle Arten, Adwaita 3)", "#dfdbd2", "#44403b", True),
    ("Seitenleiste", "#dfdbd2", "#31302e", True),
]

# labwc: (Element, Schrift, Grund, Pflicht); Farben müssen in der themerc
# stehen, dunkel zusätzlich in themerc-override-dunkel (außer Knöpfe).
OSD_AKTIV_HELL = "#f4dbd0"     # #F0774633 über #f5f4f2
OSD_AKTIV_DUNKEL = "#5a4134"   # #F0774633 über #353430
PAARE_LABWC = [
    ("Titel aktiv, Verlauf oben", "#000000", "#eeece9", True),
    ("Titel aktiv, Verlauf unten", "#000000", "#d8d4d0", True),
    ("Titel inaktiv", "#6e6e6e", "#f2f1ef", True),
    ("Fensterwechsler", "#3c3c3c", "#f5f4f2", True),
    ("Fensterwechsler, gewählter Eintrag", "#3c3c3c", OSD_AKTIV_HELL, True),
    ("Info: Fenstermenü (labwc-Standard, nicht im Theme)", "#000000", "#fcfbfa", False),
]
PAARE_LABWC_DUNKEL = [
    ("Titel aktiv, Verlauf oben", "#f2f1f0", "#4a4843", True),
    ("Titel aktiv, Verlauf unten", "#f2f1f0", "#3c3b37", True),
    ("Titel inaktiv", "#a8a29d", "#353430", True),
    ("Fenstermenü", "#dfdbd2", "#353430", True),
    ("Fenstermenü, Auswahl", "#1a1a1a", "#f07746", True),
    ("Fenstermenü, Überschrift", "#dfdbd2", "#3c3b37", True),
    ("Fensterwechsler", "#dfdbd2", "#353430", True),
    ("Fensterwechsler, gewählter Eintrag", "#dfdbd2", OSD_AKTIV_DUNKEL, True),
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
        # opacity (dim-label), relative Farbe (Tastenkürzel, 0.2.1) bzw. in
        # GTK 3 alpha(currentColor, …)
        return farbe in css and (f"opacity: {a}" in css or f"alpha * {a})" in css
                                 or f"alpha(currentcolor, {a})" in css)
    ersatz = {**ERSATZ, OSD_AKTIV_HELL: "#f0774633", OSD_AKTIV_DUNKEL: "#f0774633"}
    return ersatz.get(farbe, farbe) in css


def gtk3_paare(paare: list, css: str, eigene: list) -> list:
    """GTK-4-Paare, deren Farben auch in GTK 3 stehen, plus eigene Paare."""
    return [p for p in paare if all(im_thema(f, css) for f in p[1:3])] + eigene


def knoepfe() -> list:
    """Titelknöpfe: Symbol gegen die Knopffläche (oben und unten im Verlauf).
    Beim X zählt der Umriss (kreuz_rand, außen breiter gezeichnet) als die an
    die Fläche grenzende Farbe; dunkel ist er gleich der X-Farbe."""
    spec = importlib.util.spec_from_file_location("labwc_knoepfe", REPO / "werkzeug" / "labwc-knoepfe.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    hexa = lambda t: "#%02x%02x%02x" % t  # noqa: E731
    paare = []
    for thema, ((an, an_h), (aus, aus_h)) in m.THEMEN.items():
        for zustand, f in (("aktiv", an), ("aktiv überfahren", an_h), ("inaktiv", aus), ("inaktiv überfahren", aus_h)):
            for teil, farbe in (("Symbol", f["symbol"]), ("Schließen-X, Umriss", f["kreuz_rand"])):
                for lage in ("oben", "unten"):
                    paare.append((f"{thema}: {teil} {zustand}, {lage}", hexa(farbe), hexa(f[lage]), True, 3.0))
    return paare


def tabelle(titel: str, paare: list, css: str, md: bool, grenze: float = 4.5) -> int:
    fehler = 0
    if md:
        print(f"**{titel}**\n")
        print(f"| Element | Schrift | Grund | Kontrast | AA ({str(grenze).replace('.', ',')}:1) |")
        print("|---|---|---|---|---|")
    else:
        print(f"== {titel}")
    for name, fg, bg, pflicht, *eigene in paare:
        g = eigene[0] if eigene else grenze
        k = verhaeltnis(mischen(fg, bg), bg)
        ok = k >= g
        fehlt = [f for f in (fg, bg) if css is not None and not im_thema(f, css)]
        if pflicht and (not ok or fehlt):
            fehler = 1
        urteil = ("bestanden" if ok else "verfehlt") if pflicht else ("(Info) " + ("erfüllt" if ok else "unter AA"))
        if fehlt:
            urteil += " – nicht im Thema: " + ", ".join(fehlt)
        k_txt = f"{k:.1f}:1".replace(".", ",")
        if g != grenze:
            urteil += f" (Grenze {g:.0f}:1, Symbol)"
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
    fehler |= tabelle("GTK 3 hell (gtk-3.0/gtk.css)", gtk3_paare(PAARE, CSS3_HELL, PAARE_GTK3), CSS3_HELL, md)
    fehler |= tabelle("GTK 3 dunkel (gtk-3.0/gtk-dark.css)",
                      gtk3_paare(PAARE_DUNKEL, CSS3_DUNKEL, PAARE_GTK3_DUNKEL), CSS3_DUNKEL, md)
    fehler |= tabelle("labwc hell (labwc/Querencia-Klassisch/themerc)", PAARE_LABWC, LABWC_HELL, md)
    fehler |= tabelle("labwc dunkel (Querencia-Klassisch-Dunkel/themerc)", PAARE_LABWC_DUNKEL, LABWC_DUNKEL, md)
    fehler |= tabelle("labwc dunkel (Querencia-Klassisch mit themerc-override-dunkel)",
                      PAARE_LABWC_DUNKEL, LABWC_OVERRIDE, md)
    fehler |= tabelle("labwc-Titelknöpfe (Symbol gegen Fläche, WCAG 1.4.11)", knoepfe(), None, md, 3.0)
    return fehler


if __name__ == "__main__":
    sys.exit(main())
