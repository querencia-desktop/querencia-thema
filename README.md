# Querencia-Klassisch – GTK-Thema

GTK-Thema von **Querencia Desktop** in der Optik von Ubuntu 10.04: der helle
Ambiance-Fensterinhalt mit den Formen von Human/Clearlooks (Knöpfe mit leichtem
Verlauf und Rahmen, Menüleisten und Werkzeugleisten wie unter GNOME 2,
klassische Scrollbalken, Reiter, Zebrastreifen in Spaltenlisten) und dem
Querencia-Akzent **#F07746** für Auswahl, Fokus und Fortschritt.

Es ergänzt das gleichnamige labwc-Fensterthema (Rahmen, Titelleiste,
Fensterwechsler) zu einem gemeinsamen Thema `Querencia-Klassisch`:

```
Querencia-Klassisch/
├─ index.theme
├─ labwc/      Fensterrahmen (aus querencia-runtime, hier nicht enthalten)
├─ gtk-4.0/    gtk.css (+ Dunkelblock), gtk-dark.css, assets/ (alle Querencia-Programme)
└─ gtk-3.0/    gtk.css, gtk-dark.css, assets/ (Fremdprogramme mit GTK 3)
```

Seit 0.2 gibt es eine dunkle Fassung nach Ambiance (Fenster, Menü- und
Werkzeugleisten `#3c3b37`, Ansichten dunkel, Auswahl weiter Orange mit
dunkler Schrift). Sie gilt bei `color-scheme` `prefer-dark` (Einstellungen →
Erscheinungsbild). Seit 0.2.1 ist die Fehlerschrift dunkel lesbar, die
Tastenkürzel in Menüs erreichen hell und dunkel WCAG AA, und Programme
finden benannte Farben für Seitenleiste und Menü (`@sidebar_bg_color`,
`@menu_bg_color` u. a., siehe [docs/farben.md](docs/farben.md)).

> **Alpha.** Teil 1 jeder `gtk.css` hängt von der installierten GTK-Version
> ab. GTK 4.22 schaltet nur laufende Programme dunkel; neu gestartete
> bleiben hell, bis das Programm nachhilft (siehe
> [docs/aufbau.md](docs/aufbau.md)). Programme mit eigener heller CSS
> folgen der dunklen Fassung noch nicht.

## Stand

| | |
|---|---|
| Version | 0.2.1 (Tag `thema/gtk-0.2.1-int`, Vorlage `integration/021/vorlage`), noch nicht live |
| Auf der Entwicklungs-VM | 0.2 live seit 21.10.2026 10:26 (Tag `thema/gtk-0.2`, Ablage `b531c62050830d10`; `gtk-theme` = `Querencia-Klassisch`, `color-scheme` `default`) |
| Letzte Prüfung | isolierte Läufe hell/dunkel über das Settings-Portal gegen die Live-Ablage 0.2 (de 1024×768, en 1920×1080), hell pixelgleich außer den Tastenkürzeln, Kontraste hell und dunkel nach WCAG AA, siehe [docs/pruefung.md](docs/pruefung.md) und [docs/farben.md](docs/farben.md) |
| Getestet auf | Ubuntu 26.04, labwc 0.9.8, GTK 4.22 und GTK 3 |

Änderungen je Version: [CHANGELOG.md](CHANGELOG.md).

## Benutzen

Das Thema gilt, wenn `org.gnome.desktop.interface gtk-theme` auf
`Querencia-Klassisch` steht. GTK 4 liest das über das Settings-Portal,
GTK 3 direkt aus gsettings. Laufende Programme wechseln sofort. Zum
Ausprobieren eines einzelnen Programms reicht:

```bash
GTK_THEME=Querencia-Klassisch querencia-rechner
```

Dunkel: `org.gnome.desktop.interface color-scheme` auf `prefer-dark`
(Einstellungen → Erscheinungsbild); ein einzelnes Programm dunkel testen mit
`GTK_THEME=Querencia-Klassisch:dark`.

Auf der Entwicklungs-VM richten `integration/thema-integrieren.sh` (0.1),
`integration/thema-02-integrieren.sh` (0.2) und
`integration/021/thema-021-integrieren.sh` (0.2.1) das Thema ein. Es tut das nur nach Freigabe durch die Status-Session, siehe
[docs/integration.md](docs/integration.md). Später kommt es nach
`/usr/share/themes/Querencia-Klassisch/` (Paket).

## Bauen und Prüfen

`python3 -I werkzeug/erzeugen.py` erzeugt `gtk.css` und `gtk-dark.css` für GTK 4 und GTK 3 (nie von Hand schreiben), `python3 -I werkzeug/kontrast.py` prüft die Kontraste hell und dunkel; geprüft wird nur isoliert (`werkzeug/isoliert.py`: eigener labwc, eigener D-Bus, Portale im Wegwerf-Bus).
Generator, Schichten und Grenzen: [docs/aufbau.md](docs/aufbau.md); Prüfung und Belegbilder: [docs/pruefung.md](docs/pruefung.md); Integration: [docs/integration.md](docs/integration.md).

## Lizenz und Herkunft

GPL-3.0-or-later, siehe [LICENSE](LICENSE) (reiner Lizenztext), wie die
Querencia-Programme. Copyright 2026 Querencia Desktop contributors;
Urheberhinweis sowie die Herkunft von Teil 1 in
[COPYRIGHT](COPYRIGHT).

- Teil 1 jeder `gtk.css` ist aus dem eingebauten Thema von GTK abgeleitet
  (GTK 4 „Default“, GTK 3 „Adwaita“; GNOME-Projekt, LGPL-2.1-or-later). Die
  LGPL erlaubt die Weitergabe unter der GPL.
- Die Farbwerte orientieren sich an den Ubuntu-10.04-Themen **Ambiance**
  (Paket light-themes 0.1.6.6) und **Human** (human-theme 0.39.1), © Canonical
  Ltd, CC BY-SA 3.0. Übernommen sind nur einzelne Farbwerte und Proportionen,
  keine Grafiken und kein Code. Marken und „look and feel“ von Ubuntu sind
  davon nicht erfasst; das Thema heißt deshalb nicht Ambiance oder Human.
- Haken, Punkt und Strich unter `quelle/assets/` sind eigene SVG-Dateien.

Name und Logo „Querencia“ sind keine freien Inhalte (Markenregel).

