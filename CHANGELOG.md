# Änderungsprotokoll – Querencia-Klassisch (GTK-Thema)

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen
nach [Semantic Versioning](https://semver.org/lang/de/). Solange die Hauptversion
0 ist, kann sich alles ändern.

## [0.2.1] – 2026-10-21 (Tag `thema/gtk-0.2.1-int`)

Lesbarkeit (QD-088) und benannte Farben für Programme.

### Geändert
- Dunkel: Fehlerschrift (`label.error`, Eingabefelder mit `.error`)
  `#ed8b85` statt `#cc0000` (4,6:1 statt 1,9:1 auf dem Fenstergrund). Hell
  unverändert `#cc0000`.
- **Hell und dunkel, bewusst sichtbar:** Tastenkürzel in Menüs
  (`popover.menu accelerator`, GTK 3 `menuitem accelerator`) mit 75 % statt
  55 % der Schrift (hell 4,9:1 statt 2,9:1, dunkel 5,8:1 statt 3,9:1), auf
  der orangen Auswahl in voller Schrift. Das ist die einzige Änderung an der
  hellen Darstellung.
- `werkzeug/erzeugen.py`: relative Farben (`rgb(from currentColor …)`)
  brauchen keine Dunkel-Zuordnung.

### Hinzugefügt
- Benannte Farben `@sidebar_bg_color`, `@sidebar_fg_color`,
  `@menu_bg_color`, `@menu_fg_color` in `gtk.css` und `gtk-dark.css`
  (GTK 4 und 3), hell und dunkel; das Thema selbst zeichnet nichts damit
  (docs/farben.md).
- `werkzeug/kontrast.py`: Fehlerschrift, Tastenkürzel und benannte Farben
  (hell 34, dunkel 43 Pflichtpaare).
- Werkzeuge: `werkzeug/regression-021.sh` mit `lauf-021.sh` (Regression
  gegen die Live-Ablage, Archiv mit falschem Kennwort, Menüs mit Kürzeln),
  `werkzeug/farbnamen-probe.sh` (benannte Farben aus einem Programm-Provider),
  `werkzeug/fokus-probe.sh` (Fokus nach Farbschema-Wechsel),
  `werkzeug/vorlage-021-bauen.sh`.
- Integration `integration/021/` (`thema-021-integrieren.sh`, Probe,
  Vorlage mit SHA256SUMS), Rückfall auf 0.2.

## [0.2] – 2026-10-20 (Tag `thema/gtk-0.2`)

Dunkle Fassung nach Ubuntu 10.04 „Ambiance“.

### Hinzugefügt
- `gtk-4.0/gtk-dark.css` und `gtk-3.0/gtk-dark.css`, aus denselben Quellen
  erzeugt: dunkles GTK-Grundthema, helle Schicht umgefärbt nach
  `quelle/dunkel-zuordnung.txt`, Ergänzungen `quelle/gtk4-dunkel.css` und
  `quelle/gtk3-dunkel.css`.
- `gtk-4.0/gtk.css` enthält die dunkle Fassung als Block
  `@media (prefers-color-scheme: dark)`: `color-scheme` `prefer-dark` aus
  dem Settings-Portal schaltet laufende GTK-4-Programme um.
- Kontrastprüfung für die dunkle Fassung (35 Pflichtpaare, WCAG AA).
- Integrationsskript `integration/thema-02-integrieren.sh` (nur Link
  0.1 → 0.2, gsettings unberührt) mit Probe und Vorlage `vorschlag-02`.
- Werkzeuge: `werkzeug/css-sichten.py` (feste Hellfarben in Programm-CSS),
  `werkzeug/bildvergleich.py`, `werkzeug/lauf-farbschema.sh`,
  `werkzeug/belege-02.sh`; isolierte Läufe mit eigenem HOME und
  `GSK_DEBUG=full-redraw`.

### Unverändert
- Helle Darstellung pixelgleich mit 0.1; `gtk-3.0/gtk.css` byte-gleich.

### Bekannte Einschränkungen
- GTK 4.22 lädt `gtk-dark.css` nicht über `color-scheme`, und neu
  gestartete Programme bleiben unter `prefer-dark` hell (GTK-Fehler, Abhilfe
  im Programm in `docs/aufbau.md`).
- Programme mit eigener heller CSS, Files (eigenes Strata-Thema) und der
  labwc-Fensterrahmen bleiben hell.

## [0.1] – 2026-10-20 (Tag `thema/gtk-0.1`)

Erste Fassung des GTK-Themas Querencia-Klassisch für GTK 4 und GTK 3.

### Hinzugefügt
- Heller Fensterinhalt nach Ubuntu 10.04 (Ambiance/Human), klassische Formen,
  Querencia-Akzent `#F07746`; Verweisfarbe nur für `link` und `button.link`.
- Generator `werkzeug/erzeugen.py` aus dem eingebauten Thema von GTK und der
  eigenen Schicht in `quelle/`.

### Bekannte Einschränkungen
- Keine dunkle Variante; Teil 1 hängt von der installierten GTK-Version ab.

[0.2]: https://github.com/querencia-desktop/querencia-thema/releases/tag/thema/gtk-0.2
[0.1]: https://github.com/querencia-desktop/querencia-thema/releases/tag/thema/gtk-0.1
