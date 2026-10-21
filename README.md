# Querencia Thema

GTK-Thema „Querencia-Klassisch“ für alle, die Querencia Desktop benutzen.
Teil von [Querencia Desktop](https://querencialinux.org)
– einer klassischen Desktopumgebung im GNOME-2-Stil für Wayland (labwc,
Rust, GTK 4).
Installiert wird es zusammen mit Querencia Desktop aus der APT-Quelle;
Anleitung auf <https://querencialinux.org>.

*English summary:* The “Querencia-Klassisch” GTK 4 and GTK 3 theme: the light
Ubuntu 10.04 look (Ambiance content area, Human/Clearlooks shapes) with the
Querencia orange accent and, since 0.2, a dark Ambiance variant, generated
from GTK's built-in theme. Part of Querencia Desktop, a classic GNOME-2-style
desktop for Wayland. Alpha; documentation is in German.

> **Alpha.** Teil 1 jeder `gtk.css` hängt von der installierten GTK-Version
> ab. GTK 4.22 schaltet nur laufende Programme dunkel; neu gestartete bleiben
> hell, bis das Programm nachhilft ([docs/aufbau.md](docs/aufbau.md)).
> Programme mit eigener heller CSS folgen der dunklen Fassung noch nicht.

## Zweck

- Heller Fensterinhalt mit den Formen von GNOME 2: Knöpfe mit leichtem
  Verlauf und Rahmen, Menü- und Werkzeugleisten, klassische Scrollbalken,
  Reiter, Zebrastreifen in Spaltenlisten; Querencia-Akzent `#F07746` für
  Auswahl, Fokus und Fortschritt.
- Seit 0.2 eine dunkle Fassung nach Ambiance (Fenster, Menü- und
  Werkzeugleisten `#3c3b37`, Ansichten dunkel, Auswahl weiter Orange mit
  dunkler Schrift); sie gilt bei `color-scheme` `prefer-dark`.
- Ergänzt das gleichnamige labwc-Fensterthema (Rahmen, Titelleiste,
  Fensterwechsler, im Repo `querencia-shell`) zu einem gemeinsamen Thema
  `Querencia-Klassisch`.
- Schriften und Mauszeiger (DejaVu Sans 10, DejaVu Sans Mono 10, fette
  Fenstertitel, DMZ-White 24): Werte, labwc-Vorgaben und Entscheidung in
  [docs/erscheinungsbild/](docs/erscheinungsbild/uebersicht.md); die Dateien
  selbst kommen aus Ubuntu-Paketen.
- Bewusst **nicht** Teil dieses Repos: Fensterrahmen (labwc), Symbole
  (`querencia-symbole`), Schrift- und Zeigerdateien.

| Ordner | Inhalt |
|---|---|
| `Querencia-Klassisch/` | fertiges Thema: `index.theme`, `gtk-4.0/` und `gtk-3.0/` je mit `gtk.css`, `gtk-dark.css` und `assets/` (erzeugt, nicht von Hand ändern) |
| `quelle/` | eigene Schicht `gtk4-klassisch.css`, `gtk3-klassisch.css`, dunkle Ergänzungen und Farbzuordnung, eigene SVG-Assets |
| `werkzeug/` | Generator `erzeugen.py`, Kontrastprüfung, Musterseiten, isolierte Belegläufe |
| `docs/` | Aufbau, Farben, Prüfung, Einrichtung in der Entwicklungsumgebung; `erscheinungsbild/` Schrift und Mauszeiger |
| `SHA256SUMS` | Prüfsummen von Thema, Quellen und Werkzeugen |

## Stand

| | |
|---|---|
| Version | 0.2.1 (Tag `thema/gtk-0.2.1`, Prüfsummen `thema/gtk-0.2.1-1`; Fehlerschrift dunkel, Tastenkürzel mit WCAG AA) |
| Letzte Prüfung | isolierte Läufe hell und dunkel über das Settings-Portal (de 1024×768, en 1920×1080), Kontraste hell und dunkel nach WCAG AA ([docs/pruefung.md](docs/pruefung.md), [docs/farben.md](docs/farben.md)) |
| Bekannte Lücken | Teil 1 hängt von der installierten GTK-Version ab (Grundlage im Kopf der `gtk.css`); GTK 4.22 lädt `gtk-dark.css` nicht über `color-scheme`; Programme mit eigener heller CSS, Files und der labwc-Rahmen bleiben hell |
| Getestet auf | Ubuntu 26.04, labwc 0.9.8, GTK 4.22 und GTK 3.24 |
| Nicht getestet | andere GTK-Versionen, HiDPI |

## Bauen

`gtk.css` wird erzeugt, nicht von Hand geschrieben (Voraussetzung: `python3`
und die GTK-Bibliotheken, deren eingebautes Thema die Grundlage ist):

```bash
python3 -I werkzeug/erzeugen.py
```

Der Generator erzeugt `gtk.css` und `gtk-dark.css` für GTK 4 und GTK 3. Er
nimmt das eingebaute Thema der installierten GTK-Bibliothek, dreht dessen Blau
auf den Querencia-Akzent, macht die Ecken klassisch, hängt die eigene Schicht
aus `quelle/` an und färbt für die dunkle Fassung nach
`quelle/dunkel-zuordnung.txt` um: [docs/aufbau.md](docs/aufbau.md).

Benutzen: `org.gnome.desktop.interface gtk-theme` auf `Querencia-Klassisch`
(GTK 4 über das Settings-Portal, GTK 3 über gsettings); für einen
Einzeltest `GTK_THEME=Querencia-Klassisch <programm>`. Paketziel:
`/usr/share/themes/Querencia-Klassisch/`. Dunkel: `color-scheme` auf
`prefer-dark` (Einstellungen → Erscheinungsbild), Einzeltest mit
`GTK_THEME=Querencia-Klassisch:dark <programm>`.

## Prüfen

Keine CI (Daten-Repo). Prüfen heißt: `werkzeug/erzeugen.py` ausführen und mit
`git status` vergleichen, `sha256sum -c SHA256SUMS`, Kontrast hell und dunkel
mit `werkzeug/kontrast.py`; Belegläufe nur in einer abgeschotteten Sitzung
(eigener labwc ohne Bildschirm, eigenes `XDG_RUNTIME_DIR` und Profil), nie in
der laufenden Desktopsitzung: [docs/pruefung.md](docs/pruefung.md).
Arbeitsweise: [CONTRIBUTING.md](CONTRIBUTING.md).

## Vorbild und Abgrenzung

Vorbild sind **die Ubuntu-10.04-Themen Ambiance und Human (GNOME 2.30)**.
Übernommen sind nur einzelne Farbwerte und Proportionen, **keine Grafiken und
kein Code** aus diesen Themen; Marken und „look and feel“ von Ubuntu sind davon
nicht erfasst, das Thema heißt deshalb nicht Ambiance oder Human. Das Projekt
ist mit Canonical, GNOME und deren Autoren weder verbunden noch von ihnen
unterstützt.

Fremdbestandteile: Teil 1 jeder `gtk.css` ist aus dem eingebauten Thema von
GTK abgeleitet (GTK 4 „Default“, GTK 3 „Adwaita“; GNOME-Projekt,
LGPL-2.1-or-later, die Weitergabe unter der GPL erlaubt). Die Farbwerte
orientieren sich an Ambiance (light-themes 0.1.6.6) und Human (human-theme
0.39.1), © Canonical Ltd, CC BY-SA 3.0. Haken, Punkt und Strich unter
`quelle/assets/` sind eigene SVG-Dateien.

## Lizenz

GPL-3.0-or-later, siehe [LICENSE](LICENSE). Copyright 2026 Querencia Desktop
contributors; Urheberhinweis und die Herkunft von Teil 1 in
[COPYRIGHT](COPYRIGHT).

Name und Logo „Querencia“ sind keine freien Inhalte: [MARKE.md](MARKE.md).

## Fehler melden

Fehler, Wünsche und Fragen zu Querencia gehen an die gemeinsame Meldestelle:
<https://github.com/querencia-desktop/querencia/issues/new/choose>.
Sicherheitslücken bitte nicht öffentlich melden, siehe [SECURITY.md](SECURITY.md).
