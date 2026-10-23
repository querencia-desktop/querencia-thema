# Aufbau des Themas

## Zwei Teile je gtk.css

`werkzeug/erzeugen.py` erzeugt `Querencia-Klassisch/gtk-4.0/gtk.css` und
`gtk-3.0/gtk.css` aus zwei Teilen, dazu je eine `gtk-dark.css` (siehe
„Dunkle Fassung“).

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

## Dunkle Fassung (0.2)

Aus denselben Quellen entsteht die dunkle Fassung nach Ubuntu 10.04
„Ambiance“: Fenster, Menü- und Werkzeugleiste `#3c3b37`, Schrift `#dfdbd2`,
Ränder `#2b2a27`, Ansichten (Listen, Editoren, Textfelder) `#2b2a27` mit
Schrift `#f2f1f0`. Akzent und Auswahl bleiben: Orange-Verlauf mit Schrift
`#1a1a1a`. Werte und Kontraste: `docs/farben.md`.

| Teil | hell (`gtk.css`) | dunkel (`gtk-dark.css`) |
|---|---|---|
| 1 | `Default-light.css` bzw. `gtk-contained.css`, `FARBEN` | `Default-dark.css` bzw. `gtk-contained-dark.css`, `FARBEN_DUNKEL`, übrige Grautöne warm (Ambiance) |
| 2 | `quelle/gtk4-klassisch.css` bzw. `gtk3-klassisch.css` | dieselbe Schicht, umgefärbt nach `quelle/dunkel-zuordnung.txt` |
| 3 | – | `quelle/gtk4-dunkel.css` bzw. `gtk3-dunkel.css` (Ergänzungen) |

Die Umfärbung der Schicht geht je Deklaration nach Rolle: `color` (Schrift),
Hintergrund ohne Verlauf (Fläche), Verlauf (erhabene Elemente), Rand,
Schatten. So kann `#ffffff` als Fläche zur Ansicht `#2b2a27` werden, als
Verlaufsanfang eines Knopfs zu `#5f5d57` und als Schrift weiß bleiben. Regeln
mit Orange oder Rot im Hintergrund (Auswahl, empfohlene und gefährliche
Aktion) bleiben unverändert. Fehlt einer Farbe die Zeile in der Zuordnung,
bricht `erzeugen.py` ab; nicht gebrauchte Zeilen meldet es als Hinweis.

`gtk-4.0/gtk.css` enthält die dunkle Fassung zusätzlich als Block
`@media (prefers-color-scheme: dark) { … }` am Ende (Teil 3 im Kopf). In
der hellen Darstellung greift der Block nicht; sie ist pixelgleich mit 0.1
(docs/pruefung.md). `gtk-3.0/gtk.css` bleibt byte-gleich, GTK 3 kennt keine
Medienabfragen.

### Wie GTK 4.22 zwischen hell und dunkel wählt

Gemessen isoliert (Probethema mit drei Farben) und an der Quelle
(`gtk/gtksettings.c`, `gtk/gtkcssprovider.c`, Zweig gtk-4-22):

- `color-scheme` aus dem Settings-Portal landet in
  `GtkSettings:gtk-interface-color-scheme` und ist an die Eigenschaft
  `prefers-color-scheme` des Themenanbieters gebunden. Sie wirkt nur über
  `@media (prefers-color-scheme: dark)`. **`gtk-dark.css` lädt GTK dabei
  nicht**; das tut es nur mit `GTK_THEME=Querencia-Klassisch:dark` oder
  `gtk-application-prefer-dark-theme`.
- **Laufende Programme** wechseln beim Umschalten sofort in beide Richtungen.
- **Neu gestartete Programme bleiben hell**, auch wenn `prefer-dark` schon
  gilt: `gtk_css_provider_load_named()` setzt das Farbschema beim Laden des
  Themas auf „Standard“ zurück, ohne die Bindung zu erneuern. Erst der
  nächste Wechsel greift. Abhilfe im Programm (gemessen): nach dem Start
  einmal `gtk::Settings::default().unwrap().notify("gtk-interface-color-scheme")`;
  die Bindung überträgt den Wert dann neu und das Thema wird dunkel. Das ist
  ein Punkt für den Folgeauftrag „CSS-Welle dunkel“.
- GTK 3 kennt `color-scheme` nicht. Dunkel nur über
  `GTK_THEME=Querencia-Klassisch:dark` oder `gtk-application-prefer-dark-theme`.

## Wie GTK das Thema findet

| | GTK 4.22 | GTK 3.24 |
|---|---|---|
| Themenname | Settings-Portal (`org.freedesktop.portal.Settings`, Backend xdg-desktop-portal-gtk liest `org.gnome.desktop.interface gtk-theme`) | gsettings `org.gnome.desktop.interface gtk-theme` direkt |
| Scrollbalken | `overlay-scrolling` über das Portal | gsettings direkt |
| ohne Portal | eingebautes Thema „Default“; gsettings und settings.ini werden auf Wayland dann **nicht** gelesen, außer `settings.ini` bei `GDK_DEBUG=no-portals` | – |
| Übersteuern | `GTK_THEME=Querencia-Klassisch` | `GTK_THEME=Querencia-Klassisch` |
| dunkel | `color-scheme` `prefer-dark` über das Portal (Medienabfrage in `gtk.css`); `GTK_THEME=…:dark` lädt `gtk-dark.css` | nur `GTK_THEME=…:dark` bzw. `gtk-application-prefer-dark-theme=true` in `~/.config/gtk-3.0/settings.ini` (`gtk-dark.css`), beides nur beim Start; `color-scheme` allein wirkt nicht (0.2.2 gemessen) |
| Suchpfad | `$XDG_DATA_HOME/themes`, `~/.themes`, `$XDG_DATA_DIRS/themes` | ebenso |

Isoliert belegt (docs/pruefung.md, Portal-Probe): Ein laufendes
GTK-4-Programm übernimmt eine gsettings-Änderung sofort, weil das Portal
`SettingChanged` sendet. Das gilt auch für Panel und Desktop.

## GTK 3 dunkel für fremde Programme (0.2.2, QD-103)

Alle Querencia-Programme sind GTK 4. GTK 3 brauchen nur fremde Programme,
auf der VM z. B. `gcr-viewer`, `gcr-prompter` und die Dialoge von
`xdg-desktop-portal-gtk` (Dateiwahl für Nicht-GTK-Programme). Isoliert
gemessen mit `werkzeug/gtk3-belege.sh` (GTK 3.24.52, Musterfenster
`werkzeug/gtk3-muster.ui` in `gtk-builder-tool preview`):

- `color-scheme` `prefer-dark` allein: GTK 3 bleibt hell (pixelgleich mit
  „Standard“). GTK 3 kennt den Schlüssel nicht.
- `gtk-application-prefer-dark-theme=true` in
  `$XDG_CONFIG_HOME/gtk-3.0/settings.ini`: GTK 3 lädt `gtk-dark.css`,
  pixelgleich mit `GTK_THEME=Querencia-Klassisch:dark`, Menü eingeschlossen.
- Die Datei wirkt nur beim Start. Ein laufendes GTK-3-Programm bleibt hell,
  wenn sie während des Laufs geschrieben wird (auch zusammen mit
  `color-scheme`). Fremde GTK-3-Programme werden also dunkel, wenn sie nach
  dem Umschalten starten.
- `gtk-dark.css` deckt das Musterfenster vollständig ab: Menüleiste und Menü
  samt Kürzeln, Werkzeugleiste, Knöpfe (normal, empfohlen, gefährlich,
  gesperrt), Kästchen, Optionsfelder, Schalter, Eingabefelder mit Platzhalter
  und Fehler, Drehfeld, Auswahlliste, Regler, Fortschritt, Pegel, Liste mit
  Spalten, Textansicht, Infoleiste, Verweis, Reiter, Statusleiste. Alle Paare
  erreichen AA (Tabellen „GTK 3“ in `docs/farben.md`).
- Abweichend von GTK 4 färbt GTK 3 die Infoleisten aller Arten gleich
  (Grundthema Adwaita 3, hell `#f1e6d9`, dunkel `#44403b`, je AA).

Für die Sitzung (Schalter „Dunkle Darstellung“) heißt das: bei dunkel
`gtk-application-prefer-dark-theme=true` in
`~/.config/gtk-3.0/settings.ini` setzen, bei hell den Schlüssel entfernen.
Das Thema braucht dafür keine weitere Änderung.

## labwc-Themen (0.2.2)

Seit 0.2.2 liegen die labwc-Teile im Repo (`labwc/`), vorher nur im
Runtime-Repo (`data/themes/Querencia-Klassisch/labwc`):

| Datei | Inhalt |
|---|---|
| `labwc/Querencia-Klassisch/` | helles Theme, `themerc` und 16 Knöpfe, byte-gleich mit dem Runtime-Repo und der Ablage 0.2.1 |
| `labwc/Querencia-Klassisch-Dunkel/` | dunkles Theme, gleicher Aufbau (`themerc` und 16 Knöpfe): Titelleiste `#4a4843` → `#3c3b37`, inaktiv `#353430`, Titel `#f2f1f0` bzw. `#a8a29d`, dunkle Knöpfe (Glyphen ≥ 4,5:1), Fenstermenü und Fensterwechsler wie die dunklen GTK-Menüs |

`werkzeug/labwc-knoepfe.py` erzeugt die PNG-Knöpfe beider Themen
(`--pruefen` vergleicht nur). Die Zeichnung stammt aus `theme_b.py`
(Variante B); die hellen Knöpfe kommen byte-gleich heraus.

labwc 0.9.8 wählt sein Theme nicht nach `color-scheme`. Dunkel wird der
Rahmen, wenn `<theme><name>` in der `rc.xml` des Benutzers
`Querencia-Klassisch-Dunkel` nennt und labwc neu liest (`--reconfigure` oder
Anmeldung). Den Namen schaltet Einstellungen 0.1.6 (Entscheidung der
Startsession, 22.10.2026). Ein `themerc-override` (nur Farben) kam nicht in
Frage: Er kann die Knopfbilder des aktiven Themes nicht tauschen
(`src/theme.c`, `load_button`).

labwc sucht ein Theme in `$XDG_DATA_HOME/themes` (Vorgabe
`~/.local/share/themes`), `~/.themes` und `$XDG_DATA_DIRS/themes`, jeweils
`<Name>/labwc/themerc`, erster Treffer gewinnt (`src/common/dir.c`). Live
ist `XDG_DATA_HOME` nicht gesetzt; beide Themen liegen deshalb als Links in
`~/.local/share/themes` (gemessen, Beleg `labwc-suchpfad.txt` der Übergabe
0.2.2).

Ein Ordner nur mit `labwc/` ist kein GTK-Thema: Die GTK-Thema-Auswahl von
Einstellungen 0.1.5 verlangt `gtk-4.0/gtk.css`, der GTK-Inspector ebenso;
`Querencia-Klassisch-Dunkel` erscheint dort nicht, wohl aber unter
Fensterdesign (labwc-Themen). Isoliert belegt mit
`werkzeug/themenliste-belege.sh`.

Isoliert belegt mit `werkzeug/labwc-belege.sh` (hell, dunkel, zurück in
1024×768 und 1920×1080; der Rückweg ist pixelgleich mit hell).

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
- **Dunkel nur für laufende Programme** ohne Abhilfe im Programm (siehe
  „Wie GTK 4.22 zwischen hell und dunkel wählt“).
- **Eigene CSS der Programme bleibt hell.** Feste helle Flächen und dunkle
  Schrift in der Programm-CSS gehen der dunklen Fassung vor; Liste in der
  Übergabe Thema 0.2 (Werkzeug `werkzeug/css-sichten.py`).
- **Fensterrahmen dunkel nur über den Theme-Namen.** labwc wählt das Thema
  nicht nach `color-scheme`; dunkel wird der Rahmen erst, wenn `rc.xml`
  `Querencia-Klassisch-Dunkel` nennt (Einstellungen 0.1.6, siehe
  „labwc-Themen“).
- **GTK 3 wird nur beim Start dunkel** (settings.ini), siehe „GTK 3 dunkel“.
- Ein neues Theme im Link erreicht laufende Programme erst beim Neustart oder
  beim Wechsel von `gtk-theme`; GTK liest die Dateien nicht erneut.
