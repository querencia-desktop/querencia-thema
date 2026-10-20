#!/usr/bin/env python3
"""Sichtung (Thema 0.2): welche Regeln in der eigenen CSS der
Querencia-Programme setzen feste helle Farben, die in der dunklen Fassung
des Themas stören? Liest nur (git show am angegebenen Stand).

Aufruf:  python3 -I werkzeug/css-sichten.py <liste> [--markdown]
<liste>: Zeilen „Programm Repo-Ordner Ref [Pfadanfang]“ (# = Kommentar);
der Pfadanfang begrenzt die Suche auf einen Teil des Repos (Runtime).

Geprüft werden *.css und in *.rs die CSS-Zeichenketten (const …: &str).
Regeln mit Orange oder Rot im Hintergrund bleiben außen vor (Schrift auf
dem Akzent). Gemeldet werden je Regel:
  heller Grund     background*/Verlauf mit Leuchtdichte > 0,45
  dunkle Schrift   color mit Leuchtdichte < 0,12 (auf dunklem Grund unleserlich)
  heller Rand      border*/outline* mit Leuchtdichte > 0,35 (gering)
Dunkle Schrift in Regeln für ausgewählte oder markierte Einträge (:selected,
.qmenu-active, Menüleiste > item:hover) steht auf dem Akzent und zählt nicht.
Der Vorschlag nennt den dunklen Wert aus quelle/dunkel-zuordnung.txt (genau
oder „≈“ den nächsten derselben Rolle); farbige Schrift bekommt eine hellere
Fassung desselben Farbtons mit mindestens 4,5:1 auf #3c3b37.
"""

import colorsys
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FARBE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\([^)]*\)|\bwhite\b|\bblack\b")
REGEL = re.compile(r"([^{}]+)\{([^{}]*)\}")
DEKL = re.compile(r"([a-z-]+)\s*:\s*([^;]+)")
AUF_AKZENT = (":selected", ".qmenu-active", "> item:hover")
RS_CSS = re.compile(r'&str\s*=\s*(r#*)?"(.*?)"#*\s*;', re.S)


def rgb(f: str):
    f = f.lower()
    if f == "white":
        return 255, 255, 255
    if f == "black":
        return 0, 0, 0
    if f.startswith("#"):
        if len(f) == 4:
            f = "#" + "".join(c * 2 for c in f[1:])
        return tuple(int(f[i:i + 2], 16) for i in (1, 3, 5))
    z = [x.strip() for x in f[f.index("(") + 1:-1].split(",")]
    return tuple(int(float(x)) for x in z[:3])


def leucht(c) -> float:
    def k(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * k(r) + 0.7152 * k(g) + 0.0722 * k(b)


def akzent(c) -> bool:
    h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in c))
    return (h * 360 <= 35 or h * 360 >= 350) and s > 0.55 and 0.3 < l < 0.85


def zuordnung():
    tab = {}
    for z in (REPO / "quelle" / "dunkel-zuordnung.txt").read_text().splitlines():
        t = z.split()
        if len(t) >= 3 and not t[0].startswith("#") and t[0] != "akzent" and t[1].startswith("#"):
            tab.setdefault(t[0], {})[t[1]] = t[2]
    return tab


TAB = zuordnung()


def aufhellen(c) -> str:
    """Gleicher Farbton, heller, bis 4,5:1 auf dem dunklen Fenstergrund."""
    h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in c))
    grund = leucht(rgb("#3c3b37"))
    while l < 0.95:
        n = tuple(round(v * 255) for v in colorsys.hls_to_rgb(h, l, s))
        if (leucht(n) + 0.05) / (grund + 0.05) >= 4.5:
            return "#%02x%02x%02x" % n
        l += 0.01
    return "#f2f1f0"


def vorschlag(rolle: str, f: str) -> str:
    c = rgb(f)
    h = "#%02x%02x%02x" % c
    for r in (rolle, "*"):
        if h in TAB.get(r, {}) and not (rolle == "schrift" and TAB[r][h] == h):
            return TAB[r][h]
    if rolle == "schrift" and colorsys.rgb_to_hls(*(v / 255 for v in c))[2] > 0.3:
        return aufhellen(c)
    kand = TAB.get(rolle, {})
    if not kand:
        return "–"
    lh = leucht(rgb(h))
    best = min(kand, key=lambda k: abs(leucht(rgb(k)) - lh))
    return "≈" + kand[best]


def css_bloecke(text: str, start_zeile: int):
    for m in REGEL.finditer(text):
        kopf = " ".join(m.group(1).split())
        if kopf.startswith(("/*", "//")) or "*/" in kopf:
            kopf = kopf.split("*/")[-1].strip()
        rumpf_start = m.start(2)
        dekls = []
        for d in DEKL.finditer(m.group(2)):
            zeile = start_zeile + text.count("\n", 0, rumpf_start + d.start())
            dekls.append((zeile, d.group(1), d.group(2).strip()))
        yield kopf, dekls


def sichten(name: str, datei: str, text: str):
    if datei.endswith(".rs"):
        teile = [(m.group(2), text.count("\n", 0, m.start(2)) + 1) for m in RS_CSS.finditer(text)
                 if "{" in m.group(2) and ":" in m.group(2)]
    else:
        teile = [(text, 1)]
    for css, z0 in teile:
        css = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), css, flags=re.S)
        for kopf, dekls in css_bloecke(css, z0):
            grund = [rgb(f) for _, e, w in dekls if e.startswith("background") for f in FARBE.findall(w)]
            if any(akzent(c) for c in grund):
                continue
            funde = []
            for zeile, e, w in dekls:
                for f in FARBE.findall(w):
                    c = rgb(f)
                    L = leucht(c)
                    if e.startswith("background"):
                        rolle = "verlauf" if "gradient" in w else "flaeche"
                        if L > 0.45:
                            funde.append((zeile, "heller Grund", e, f, vorschlag(rolle, f)))
                    elif e == "color":
                        if L < 0.12 and not any(a in kopf for a in AUF_AKZENT):
                            funde.append((zeile, "dunkle Schrift", e, f, vorschlag("schrift", f)))
                    elif e.startswith(("border", "outline")) and "transparent" not in w:
                        if L > 0.35:
                            funde.append((zeile, "heller Rand", e, f, vorschlag("rand", f)))
            if funde:
                yield kopf, funde


def main() -> int:
    md = "--markdown" in sys.argv[1:]
    liste = Path([a for a in sys.argv[1:] if not a.startswith("--")][0])
    if md:
        print("| Programm | Datei:Zeile | Regel | feste Farbe(n) | Vorschlag dunkel |")
        print("|---|---|---|---|---|")
    summe = {}
    for z in liste.read_text().splitlines():
        if not z.strip() or z.lstrip().startswith("#"):
            continue
        name, repo, ref = z.split()[:3]
        anfang = z.split()[3] if len(z.split()) > 3 else ""
        repo = str(Path(repo).expanduser())
        dateien = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", ref],
                                 capture_output=True, text=True, check=True).stdout.split()
        for d in dateien:
            if not d.startswith(anfang) or not d.endswith((".css", ".rs")) or re.search(r"(^|/)(tests?|target)/", d):
                continue
            text = subprocess.run(["git", "-C", repo, "show", f"{ref}:{d}"],
                                  capture_output=True, text=True, check=True).stdout
            for kopf, funde in sichten(name, d, text):
                art = sorted({f[1] for f in funde})
                summe[name] = summe.get(name, 0) + 1
                farben = "; ".join(f"{e} {f}" for _, _, e, f, _ in funde)
                vor = "; ".join(f"{e} {v}" for _, _, e, _, v in funde)
                zeile = funde[0][0]
                if md:
                    print(f"| {name} | `{d}:{zeile}` | `{kopf[:70]}` ({', '.join(art)}) | {farben} | {vor} |")
                else:
                    print(f"{name:20} {d}:{zeile}  {kopf[:60]}  [{', '.join(art)}]  {farben}  ->  {vor}")
    print()
    print("Regeln je Programm: " + ", ".join(f"{k} {v}" for k, v in summe.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
