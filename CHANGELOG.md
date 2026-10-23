# Änderungsprotokoll – Querencia-Klassisch (GTK-Thema)

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen
nach [Semantic Versioning](https://semver.org/lang/de/). Solange die Hauptversion
0 ist, kann sich alles ändern.

## [0.2.2] – 2026-10-22 (Tags `thema/gtk-0.2.2-2`, `thema/gtk-0.2.2-2-int`)

Fassung 2. Die nie aktivierte Fassung 1 (Tags `thema/gtk-0.2.2`,
`thema/gtk-0.2.2-int`, `integration/022/`) hatte zusätzlich
`themerc-override-dunkel` und dunkle Knöpfe mit 3:1; sie bleibt eingefroren
liegen.

Fensterrahmen dunkel (QD-088 Punkt 6), GTK 3 dunkel geprüft (QD-103),
Kontrastlauf über GTK 4, GTK 3 und labwc.

### Hinzugefügt
- labwc-Teile im Repo (`labwc/`): helles Theme `Querencia-Klassisch`
  (byte-gleich mit dem Runtime-Repo und der Ablage 0.2.1), neues dunkles
  Theme `Querencia-Klassisch-Dunkel` (Titelleiste `#4a4843` → `#3c3b37`,
  Titel `#f2f1f0` 8,1:1, inaktiv `#a8a29d` 4,9:1, dunkle Knöpfe, dunkles
  Fenstermenü und dunkler Fensterwechsler, dunkle Knöpfe mit Glyphen
  ≥ 4,5:1). Den Namen in `rc.xml` schaltet Einstellungen 0.1.6.
- `werkzeug/labwc-knoepfe.py` (Knöpfe beider Themen, `--pruefen`),
  `werkzeug/labwc-belege.sh` und `labwc-fenster.py` (Belege hell, dunkel,
  zurück in 1024×768 und 1920×1080), `werkzeug/themenliste-belege.sh`
  (Einstellungen 0.1.5 und GTK-Inspector listen das Dunkel-Theme nicht als
  GTK-Thema), `werkzeug/gtk3-belege.sh` mit `gtk3-muster.ui` (GTK 3
  hell/dunkel), `werkzeug/fokus-probe-022.sh` (Fokus nach Taste und
  Farbschema-Wechsel).
- `werkzeug/kontrast.py`: Tabellen GTK 3 hell/dunkel, labwc hell/dunkel und
  Titelknöpfe (dunkel 4,5:1, hell 3:1); Grenze 3:1 für Symbole.
- Integration `integration/022-2/` (`thema-022-2-integrieren.sh`, Probe,
  Vorlage mit SHA256SUMS); Ablage enthält zusätzlich
  `Querencia-Klassisch-Dunkel/labwc`, neuer Link
  `~/.local/share/themes/Querencia-Klassisch-Dunkel`. Gemeinsame Sperre mit
  den Skripten 0.1, 0.2 und 0.2.1; `zurueck` verweigert, solange die
  Benutzer-`rc.xml` den dunklen Namen trägt.

### Geändert
- **Hell und dunkel, sichtbar:** Skalenwert und Skalenmarken mit 75 % statt
  55 % der Schrift (hell 4,9:1 statt 2,9:1), Pfeil zum Untermenü und
  Schließknopf auf Reitern mit 75 % statt 30 % (GTK 4 und GTK 3; GTK 3 ohne
  Untermenüpfeil, dort war er schon voll).
- `quelle/dunkel-zuordnung.txt`: Zeile Skalenmarken `#8f8a85` entfällt.
- `werkzeug/isoliert.py`: keine `QUERENCIA_*`-Variable der Live-Sitzung im
  isolierten Lauf, `GIO_USE_VFS=local` (kein gvfsd/wsdd).

### Geprüft, ohne Änderung
- GTK 3: `gtk-dark.css` ist für fremde Programme vollständig; dunkel nur
  über `gtk-application-prefer-dark-theme` in `settings.ini` und nur beim
  Start (docs/aufbau.md).
- QD-088 (5): Ein Farbschema-Wechsel verschiebt den Fokus nicht, weder unter
  Querencia-Klassisch noch unter GTK-Default. Der Fokusrahmen kommt von der
  Tastatureingabe davor (GTK `focus-visible`) und geht nach einigen Sekunden
  ohne Taste aus.

## [0.2.1] – 2026-10-21 (Tag `thema/gtk-0.2.1-int`)

Lesbarkeit und benannte Farben für Programme.

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

### Hinzugefügt
- `docs/erscheinungsbild/`: Schrift und Mauszeiger (Werte, labwc-Vorgaben,
  Entscheidungsvorlage), übernommen aus dem Arbeitsrepo
  querencia-erscheinungsbild 0.1.

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
