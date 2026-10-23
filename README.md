# Querencia Thema

GTK-Thema „Querencia-Klassisch“ für alle, die Querencia Desktop benutzen.
Teil von [Querencia Desktop](https://querencialinux.org)
– einer klassischen Desktopumgebung im GNOME-2-Stil für Wayland (labwc,
Rust, GTK 4).
Installiert wird es zusammen mit Querencia Desktop aus der APT-Quelle;
Anleitung auf <https://querencialinux.org>.

Es ergänzt das gleichnamige labwc-Fensterthema (Rahmen, Titelleiste,
Fensterwechsler) zu einem gemeinsamen Thema `Querencia-Klassisch`:

```
Querencia-Klassisch/
├─ index.theme
├─ labwc/      Fensterrahmen und Knöpfe (Quelle: labwc/ im Repo)
├─ gtk-4.0/    gtk.css (+ Dunkelblock), gtk-dark.css, assets/ (alle Querencia-Programme)
└─ gtk-3.0/    gtk.css, gtk-dark.css, assets/ (Fremdprogramme mit GTK 3)
Querencia-Klassisch-Dunkel/
└─ labwc/      dunkles labwc-Theme (seit 0.2.2)
```

Seit 0.2 gibt es eine dunkle Fassung nach Ambiance (Fenster, Menü- und
Werkzeugleisten `#3c3b37`, Ansichten dunkel, Auswahl weiter Orange mit
dunkler Schrift). Sie gilt bei `color-scheme` `prefer-dark` (Einstellungen →
Erscheinungsbild). Seit 0.2.1 ist die Fehlerschrift dunkel lesbar, die
Tastenkürzel in Menüs erreichen hell und dunkel WCAG AA, und Programme
finden benannte Farben für Seitenleiste und Menü (`@sidebar_bg_color`,
`@menu_bg_color` u. a., siehe [docs/farben.md](docs/farben.md)). Seit 0.2.2
gibt es die Fensterrahmen auch dunkel (labwc-Theme
`Querencia-Klassisch-Dunkel`, gewählt über Einstellungen), GTK 3 ist dunkel geprüft, und gedimmte Bedienteile (Skalen,
Untermenüpfeil, Schließknopf auf Reitern) erreichen AA.

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
| Version | 0.2.2 Fassung 2 (Tags `thema/gtk-0.2.2-2`, `thema/gtk-0.2.2-2-int`, Vorlage `integration/022-2/vorlage`), noch nicht live |
| Auf der Entwicklungs-VM | 0.2.1 live seit 21.10.2026 18:05 (Tag `thema/gtk-0.2.1-int`, Ablage `22824d05ceb49cad`; `gtk-theme` = `Querencia-Klassisch`, `color-scheme` `default`) |
| Letzte Prüfung | isolierte Läufe gegen die Live-Ablage 0.2.1, labwc hell/dunkel, GTK 3 hell/dunkel, Kontraste GTK 4, GTK 3 und labwc nach WCAG AA, siehe [docs/pruefung.md](docs/pruefung.md) und [docs/farben.md](docs/farben.md) |
| Getestet auf | Ubuntu 26.04, labwc 0.9.8, GTK 4.22 und GTK 3 |

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

Auf der Entwicklungs-VM richten `integration/thema-integrieren.sh` (0.1),
`integration/thema-02-integrieren.sh` (0.2),
`integration/021/thema-021-integrieren.sh` (0.2.1) und
`integration/022-2/thema-022-2-integrieren.sh` (0.2.2) das Thema ein. Es tut das nur nach Freigabe durch die Status-Session, siehe
[docs/integration.md](docs/integration.md). Später kommt es nach
`/usr/share/themes/Querencia-Klassisch/` (Paket).

## Prüfen

`python3 -I werkzeug/erzeugen.py` erzeugt `gtk.css` und `gtk-dark.css` für GTK 4 und GTK 3 (nie von Hand schreiben), `python3 -I werkzeug/kontrast.py` prüft die Kontraste hell und dunkel (GTK 4, GTK 3, labwc), `python3 -I werkzeug/labwc-knoepfe.py` erzeugt die labwc-Knöpfe; geprüft wird nur isoliert (`werkzeug/isoliert.py`: eigener labwc, eigener D-Bus, Portale im Wegwerf-Bus).
Generator, Schichten und Grenzen: [docs/aufbau.md](docs/aufbau.md); Prüfung und Belegbilder: [docs/pruefung.md](docs/pruefung.md); Integration: [docs/integration.md](docs/integration.md).

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
