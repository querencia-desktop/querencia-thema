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
├─ gtk-4.0/    gtk.css + assets/ (alle Querencia-Programme)
└─ gtk-3.0/    gtk.css + assets/ (Fremdprogramme mit GTK 3)
```

## Benutzen

Das Thema gilt, wenn `org.gnome.desktop.interface gtk-theme` auf
`Querencia-Klassisch` steht. GTK 4 liest das über das Settings-Portal,
GTK 3 direkt aus gsettings. Laufende Programme wechseln sofort. Zum
Ausprobieren eines einzelnen Programms reicht:

```bash
GTK_THEME=Querencia-Klassisch querencia-rechner
```

Auf der Entwicklungs-VM richtet `integration/thema-integrieren.sh` das Thema
ein. Es tut das nur nach Freigabe durch die Status-Session, siehe
[docs/integration.md](docs/integration.md). Später kommt es nach
`/usr/share/themes/Querencia-Klassisch/` (Paket).

## Bauen

`gtk.css` wird erzeugt, nicht von Hand geschrieben:

```bash
python3 -I werkzeug/erzeugen.py
```

Der Generator nimmt das eingebaute Thema der installierten GTK-Bibliothek,
dreht dessen Blau auf den Querencia-Akzent, macht die Ecken klassisch und
hängt die eigene Schicht `quelle/gtk4-klassisch.css` bzw.
`quelle/gtk3-klassisch.css` an. Einzelheiten stehen in
[docs/aufbau.md](docs/aufbau.md).

## Lizenz und Herkunft

GPL-3.0-or-later (siehe `LICENSE`), wie die Querencia-Programme.

- Teil 1 jeder `gtk.css` ist aus dem eingebauten Thema von GTK abgeleitet
  (GTK 4 „Default“, GTK 3 „Adwaita“; GNOME-Projekt, LGPL-2.1-or-later). Die
  LGPL erlaubt die Weitergabe unter der GPL.
- Die Farbwerte orientieren sich an den Ubuntu-10.04-Themen **Ambiance**
  (Paket light-themes 0.1.6.6) und **Human** (human-theme 0.39.1), © Canonical
  Ltd, CC BY-SA 3.0. Übernommen sind nur einzelne Farbwerte und Proportionen,
  keine Grafiken und kein Code. Marken und „look and feel“ von Ubuntu sind
  davon nicht erfasst; das Thema heißt deshalb nicht Ambiance oder Human.
- Haken, Punkt und Strich unter `quelle/assets/` sind eigene SVG-Dateien.
