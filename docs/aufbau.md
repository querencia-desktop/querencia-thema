# Aufbau des Themas

## Zwei Teile je gtk.css

`werkzeug/erzeugen.py` erzeugt `Querencia-Klassisch/gtk-4.0/gtk.css` und
`gtk-3.0/gtk.css` aus zwei Teilen.

**Teil 1: eingebautes GTK-Thema, umgefärbt.** Grundlage ist das Thema, das
in der installierten Bibliothek steckt. Gelesen wird es mit `gresource extract`:

| GTK | Ressource | Bibliothek auf der VM |
|---|---|---|
| 4.22.4 | `/org/gtk/libgtk/theme/Default/Default-light.css` | `libgtk-4.so.1` |
| 3.24.52 | `/org/gtk/libgtk/theme/Adwaita/gtk-contained.css` | `libgtk-3.so.0` |

Daran ändert der Generator drei Dinge:

1. **Farben.** Die blaue Akzentfamilie (Farbton 190–235°, gesättigt) wird auf
   den Farbton von #F07746 gedreht. Dazu kommen feste Zuordnungen für Grund,
   Schrift, Rahmen und deaktivierte Schrift (`FARBEN` im Skript). So landet
   jedes Blau, auch in seltenen Zuständen, beim Querencia-Orange.
2. **Ecken.** Radien von 5 bis 10 px werden zu 3 px.
3. **Kein `:backdrop`.** Regeln für Fenster ohne Fokus fallen weg. Wie unter
   GNOME 2 zeigt der Fensterrahmen den Fokus, der Inhalt bleibt gleich.

Die Bilder des Grundthemas (Schiebereglermarken als PNG) werden nicht
übernommen. Haken, Punkt und Strich liegen als eigene SVG unter
`quelle/assets/`.

**Teil 2: GNOME-2-Schicht.** `quelle/gtk4-klassisch.css` und
`quelle/gtk3-klassisch.css` formen die Elemente nach Ubuntu 10.04: Knöpfe mit
Verlauf und Rahmen, flache Werkzeugleisten-Knöpfe, die beim Überfahren erhaben
werden, Menüleiste und Menüs wie die Panelmenüs, Reiter mit orangem Strich am
aktiven Reiter, Zebrastreifen, klassische Scrollbalken (13 px, Griff mit
Verlauf), eckige Schieberegler, Fortschrittsbalken in 14 px Höhe, Kästchen mit
dunklem Haken, dunkle Tooltips (Ambiance), eckige Meldungsdialoge. Weil die
Schicht hinten steht, gewinnt sie bei gleicher Spezifität.

Der Kopf jeder erzeugten Datei nennt die SHA256 der Grundlage. Ändert ein
GTK-Update das eingebaute Thema, zeigt `erzeugen.py --pruefen` die Abweichung.
Dann neu erzeugen und isoliert prüfen.

## Wie GTK das Thema findet

| | GTK 4.22 | GTK 3.24 |
|---|---|---|
| Themenname | Settings-Portal (`org.freedesktop.portal.Settings`, Backend xdg-desktop-portal-gtk liest `org.gnome.desktop.interface gtk-theme`) | gsettings `org.gnome.desktop.interface gtk-theme` direkt |
| Scrollbalken | `overlay-scrolling` über das Portal | gsettings direkt |
| ohne Portal | eingebautes Thema „Default“; gsettings und settings.ini werden auf Wayland dann **nicht** gelesen, außer `settings.ini` bei `GDK_DEBUG=no-portals` | – |
| Übersteuern | `GTK_THEME=Querencia-Klassisch` | `GTK_THEME=Querencia-Klassisch` |
| Suchpfad | `$XDG_DATA_HOME/themes`, `~/.themes`, `$XDG_DATA_DIRS/themes` | ebenso |

Isoliert belegt (docs/pruefung.md, Portal-Probe): Ein laufendes
GTK-4-Programm übernimmt eine gsettings-Änderung sofort, weil das Portal
`SettingChanged` sendet. Das gilt auch für Panel und Desktop.

## Klassische Scrollbalken

Ob Scrollbalken überlagert und ausgeblendet werden, entscheidet GTK über die
Einstellung `gtk-overlay-scrolling`, nicht das Thema. Die Integration stellt
deshalb `org.gnome.desktop.interface overlay-scrolling` auf `false`. Das Thema
zeichnet die Balken breit und klassisch. Erzwingt ein Programm trotzdem
Überlagerungsbalken, sind sie wenigstens breit und sichtbar gezeichnet.

## Grenzen

- **Keine Zebrastreifen in GtkTreeView** (GTK 3 und GTK 4). Die alte
  Baumansicht hat keine Zeilenknoten; `:nth-child` träfe die Ansicht selbst
  (isoliert ausprobiert). Streifen gibt es in GTK-4-`ColumnView`
  (Systemmonitor, Dateisuche, Software-Expertenliste).
- **Eigene CSS der Programme geht vor.** Panel, Editor, Rechner, Systemmonitor,
  Dateisuche, Software, Bilder und Files bringen eigene Regeln mit (Priorität
  APPLICATION). Dort bleibt z. B. weiße Schrift auf Orange, bis die Programme
  nachziehen.
- **Firefox (Snap)** sieht nur die Themen aus `gtk-common-themes`, nicht
  `~/.local/share/themes`. Er bleibt bei Adwaita, bis es ein Paket oder einen
  Theme-Snap gibt.
- **GTK-4-Meldungsdialoge** (AlertDialog) sind clientseitig dekoriert und
  haben keine labwc-Titelleiste. Das Thema gibt ihnen einen 1-px-Rahmen in
  der Farbe der labwc-Rahmen. Die Knopfreihe füllt weiterhin die ganze Breite
  (Aufteilung durch GTK).
- Ein dunkles Thema gibt es nicht (nicht verlangt). `color-scheme`
  `prefer-dark` lädt `gtk-dark.css`; die Datei fehlt, also gilt das helle Thema.
