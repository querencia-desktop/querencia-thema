# Integration auf der Entwicklungs-VM

Vier Skripte, alle nach dem Muster von `theme-osd-integrieren.sh` (G2-R)
aus querencia-runtime:

| Skript | Schritt | Vorlage | Probe |
|---|---|---|---|
| `integration/022/thema-022-integrieren.sh` | 0.2.1 (`22824d05…`) → 0.2.2, dazu Link `Querencia-Klassisch-Dunkel` | `integration/022/vorlage/` | `integration/022/probe-022.sh` |
| `integration/021/thema-021-integrieren.sh` | 0.2 (`b531c620…`) → 0.2.1 | `integration/021/vorlage/` | `integration/021/probe-021.sh` |
| `integration/thema-02-integrieren.sh` | 0.1 (`a53ff41c…`) → 0.2 (dunkle Fassung) | `integration/vorschlag-02/` | `integration/probe-02.sh` |
| `integration/thema-integrieren.sh` | G2-R (`e72ae8ed…`) → 0.1, mit gsettings | `integration/vorschlag/` | `integration/probe.sh` |

Das Skript 0.1 und seine Vorlage bleiben unverändert: Journal und Übergabe
Thema-1 zeigen darauf (Rückfall von 0.1 auf G2-R).

## Thema 0.2.2 (`022/thema-022-integrieren.sh`)

Aktiver Arbeitsordner: `~/projects/querencia-thema-022/integration/` mit
Skript, Probe und `vorlage/`. `integration/022/` im Repo ist derselbe Stand
(Tag `thema/gtk-0.2.2-int`); `werkzeug/vorlage-022-bauen.sh` baut die
Vorlage aus `Querencia-Klassisch/` und `labwc/`, trägt `BAUM_NEU` und
`SUMMEN_SHA` ein und spiegelt in den Arbeitsordner.

```bash
bash ~/projects/querencia-thema-022/integration/thema-022-integrieren.sh pruefen
QTH_FREIGABE=ja bash ~/projects/querencia-thema-022/integration/thema-022-integrieren.sh aktivieren   # nur nach Freigabe
QTH_FREIGABE=ja bash ~/projects/querencia-thema-022/integration/thema-022-integrieren.sh zurueck      # Rückfall auf 0.2.1
```

- **aktivieren** legt die Ablage `~/opt/querencia-theme/<B16>/` an
  (0555/0444) mit `Querencia-Klassisch/` (GTK 4, GTK 3, `index.theme`,
  `labwc/` wie 0.2.1 plus `labwc/themerc-override-dunkel`) und
  `Querencia-Klassisch-Dunkel/labwc/`. Dann setzt es den neuen Link
  `~/.local/share/themes/Querencia-Klassisch-Dunkel` und stellt den Link
  `Querencia-Klassisch` von 0.2.1 `22824d05…` atomar um. Journalzeile mit
  Rückfallbefehl.
- **zurueck** stellt den Link auf 0.2.1 und entfernt den Dunkel-Link (nur
  wenn er auf die Ablage 0.2.2 zeigt); die Ablage 0.2.2 bleibt. Weiter auf
  0.2 danach mit dem Skript 0.2.1.
- Halbe Zustände (nur ein Link umgestellt) vervollständigen `aktivieren`
  und `zurueck`; ein fremder Link oder Ordner unter einem der beiden Namen
  führt zur Verweigerung.
- Invarianten: `vorlage/SHA256SUMS` = `SUMMEN_SHA` und `sha256sum -c`; Liste
  der Ablage 0.2.1 als `vorlage/liste-021.txt` (`BAUM_ALT`); helles
  labwc-Theme und `index.theme` byte-gleich mit 0.2.1, dazu genau
  `themerc-override-dunkel`; `Querencia-Klassisch-Dunkel/labwc` mit
  `themerc` und 16 Knöpfen; benannte Farben und Kontrastregeln 0.2.2 in der
  Vorlage.
- **Sperre:** `thema-integrieren-gemeinsam.lock` und zusätzlich die
  Sperren der Skripte 0.1, 0.2 und 0.2.1; keines davon kann gleichzeitig
  laufen.
- Unberührt: gsettings, `rc.xml`, `themerc-override` der Sitzung,
  `~/.config/gtk-3.0`, der laufende labwc.
- **Wirkung:** neu gestartete GTK-Programme sehen 0.2.2 sofort (hell:
  Skalenwert, Untermenüpfeil, Schließknopf auf Reitern etwas dunkler).
  Der helle Rahmen bleibt byte-gleich. `Querencia-Klassisch-Dunkel` und
  `themerc-override-dunkel` liegen nur bereit; dunkel wird der Rahmen erst,
  wenn die Sitzung sie nutzt (docs/aufbau.md, „labwc-Themen“).

Probe: `bash integration/022/probe-022.sh` (Wegwerf-Ordner, Ablage 0.2.1
als Kopie, Fehler an jeder Stelle mit Rückrollen, halbe Zustände, fremde
Links und Ordner, alle vier Sperren, halbe Umlenkung). Ergebnis: 69/69.

## Thema 0.2.1 (`021/thema-021-integrieren.sh`)

Aktiver Arbeitsordner (von dort läuft das Skript live):
`~/projects/querencia-thema-021/integration/` mit Skript, Probe und
`vorlage/`. `integration/021/` im Repo ist derselbe Stand (Tag
`thema/gtk-0.2.1-int`); `werkzeug/vorlage-021-bauen.sh` baut die Vorlage,
trägt `BAUM_NEU` und `SUMMEN_SHA` ein und spiegelt in den Arbeitsordner.

```bash
bash ~/projects/querencia-thema-021/integration/thema-021-integrieren.sh pruefen
QTH_FREIGABE=ja bash ~/projects/querencia-thema-021/integration/thema-021-integrieren.sh aktivieren   # nur nach Freigabe
QTH_FREIGABE=ja bash ~/projects/querencia-thema-021/integration/thema-021-integrieren.sh zurueck      # Rückfall auf 0.2
```

- **aktivieren** legt die Ablage `~/opt/querencia-theme/<B16>/Querencia-Klassisch`
  an (0555/0444, Kopie von `vorlage/Querencia-Klassisch`, Herkunftsdatei
  daneben) und stellt den Link von der Ablage 0.2 `b531c620…` atomar auf
  `<B16>` um. Journalzeile mit Rückfallbefehl. gsettings bleiben unberührt.
- **zurueck** stellt den Link auf die Ablage 0.2; die Ablage 0.2.1 bleibt.
  Weiter auf 0.1 geht es danach mit dem Skript 0.2 (`zurueck`); das
  verweigert, solange der Link auf 0.2.1 zeigt.
- Invarianten wie 0.2, dazu: `vorlage/SHA256SUMS` hat die im Skript
  eingetragene Summe `SUMMEN_SHA` und stimmt (`sha256sum -c`); die Liste der
  Ablage 0.2 liegt als `vorlage/liste-02.txt` bei (Summe `BAUM_ALT`);
  außerhalb von `gtk-4.0/` und `gtk-3.0/` alles byte-gleich mit 0.2; die
  Vorlage enthält die benannten Farben.
- **Wirkung:** neu gestartete GTK-Programme sehen 0.2.1 sofort, laufende
  behalten 0.2 bis zum Neustart. Hell ändern sich nur die Tastenkürzel in
  Menüs (etwas dunkler), dunkel zusätzlich die Fehlerschrift.

Probe: `bash integration/021/probe-021.sh` (Wegwerf-Ordner, Ablage 0.2 als
Kopie; zusätzlich eine veränderte Vorlagendatei und eine veränderte
SHA256SUMS in einer Kopie). Ergebnis: 52/52.

## Thema 0.2 (`thema-02-integrieren.sh`)

```bash
bash integration/thema-02-integrieren.sh pruefen
QTH_FREIGABE=ja bash integration/thema-02-integrieren.sh aktivieren   # nur nach Freigabe
QTH_FREIGABE=ja bash integration/thema-02-integrieren.sh zurueck
```

- **aktivieren** legt die Ablage `~/opt/querencia-theme/<B16>/Querencia-Klassisch`
  an (0555/0444, Kopie von `vorschlag-02/`, Herkunftsdatei daneben) und
  stellt den Link `~/.local/share/themes/Querencia-Klassisch` atomar von
  `a53ff41c…` auf `<B16>` um. Journalzeile mit Rückfallbefehl.
- **gsettings bleiben unberührt** (`gtk-theme`, `color-scheme`,
  `overlay-scrolling`); `pruefen` liest sie nur.
- **zurueck** stellt den Link auf `a53ff41c…` zurück; die Ablage 0.2 bleibt.
- Invarianten: Liste 0.1 (`vorschlag/theme-manifest.txt`, `a53ff41c…`),
  Liste 0.2 (`BAUM_NEU`), Vorlage und beide Ablagen gegen ihre Listen,
  außerhalb von `gtk-4.0/` und `gtk-3.0/` alles byte-gleich mit 0.1 (labwc,
  `index.theme`), `gtk-4.0/gtk-dark.css` vorhanden. Link fremd oder fehlend,
  Sperre belegt, Live ohne `QTH_FREIGABE=ja`: Exit 2, nichts geändert.
  Fehler oder Signal mitten im Lauf: Link zurück, Exit 1.
- **Wirkung:** neu gestartete GTK-Programme sehen 0.2 sofort. Laufende
  (Panel, Desktop, offene Fenster) behalten die schon geladene 0.1, bis sie
  neu starten (spätestens bei der nächsten Anmeldung); GTK liest die
  Dateien nur beim Start und beim Wechsel von `gtk-theme`. Hell sieht 0.2
  aus wie 0.1 (pixelgleich, docs/pruefung.md).
- **Vor dem Umschalten auf dunkel** beachten: Programme mit eigener heller
  CSS (Editor, Bilder, Rechner, Systemmonitor, Dateisuche, Software) haben
  im Dunkel-Modus helle Menüs mit heller Schrift, bis der Folgeauftrag
  „CSS-Welle dunkel“ sie nachzieht (Liste in der Übergabe Thema 0.2).

Probe: `bash integration/probe-02.sh` (Wegwerf-Ordner unter
`~/.cache/querencia-thema/`, Ablage 0.1 als Kopie, gsettings als
Schlüsseldatei; Fehler an jeder Stelle und Signale in beide Richtungen,
doppeltes aktivieren/zurueck, veränderte Ablagen, fremder und fehlender
Link, belegte Sperre, Live ohne Freigabe; am Ende echte gsettings, echter
Link und keine Live-Ablage). Ergebnis zuletzt: 46/46.

Nach einer Änderung am Thema:

```bash
python3 -I werkzeug/erzeugen.py
bash werkzeug/vorlage-02-bauen.sh   # vorschlag-02 + Liste, trägt BAUM_NEU ein
bash integration/probe-02.sh
bash werkzeug/summen.sh             # SHA256SUMS erneuern
```

## Thema 0.1 (`thema-integrieren.sh`)

```bash
bash integration/thema-integrieren.sh pruefen
QTH_FREIGABE=ja bash integration/thema-integrieren.sh aktivieren   # nur nach Freigabe
QTH_FREIGABE=ja bash integration/thema-integrieren.sh zurueck
```

### Was „aktivieren“ tut

1. **Ablage** `~/opt/querencia-theme/<B16>/Querencia-Klassisch`
   (Ordner 0555, Dateien 0444). Kopie von `integration/vorschlag/`:
   `labwc/` byte-gleich mit der heute aktiven Ablage `e72ae8ed962abecb`
   (G2-R), neu sind `gtk-4.0/`, `gtk-3.0/` und `index.theme`. `B16` ist der
   Anfang der SHA256 von `vorschlag/theme-manifest.txt` und steht als
   `BAUM_NEU` im Skript.
2. **Link** `~/.local/share/themes/Querencia-Klassisch` von der alten auf die
   neue Ablage, atomar per `mv`.
3. **gsettings** `org.gnome.desktop.interface`: `overlay-scrolling` → `false`,
   dann `gtk-theme` → `Querencia-Klassisch`. Die Werte davor sichert das
   Skript in `~/.local/state/querencia/thema1-gsettings-vorher.txt` (nur
   beim ersten Mal) und in `sicherung-thema1-<Zeit>/vorher.txt`.
4. **Journal**: eine Zeile in `~/opt/querencia/protokoll.txt` mit dem
   Rückfallbefehl.

**Wirkung: sofort.** GTK-4-Programme (auch Panel, Desktop, Files) bekommen
die Änderung über das Settings-Portal und wechseln im laufenden Betrieb.
GTK-3-Programme lesen gsettings direkt. Der Fensterrahmen ändert sich nicht,
ein `labwc --reconfigure` ist nicht nötig. Programme mit eigenem
`GTK_THEME` oder ohne Portal zeigen das Thema erst nach einem Neustart.

### „zurueck“

Stellt Link, `gtk-theme` und `overlay-scrolling` auf die gesicherten Werte.
Die neue Ablage bleibt liegen. Hat jemand `gtk-theme` inzwischen von Hand auf
ein drittes Thema gestellt, verweigert `zurueck` (Exit 2) und ändert nichts.

### Sicherungen und Verweigerungen

- `QTH_FREIGABE=ja` ist live Pflicht; ohne sie Exit 2.
- Prüfsummen: Liste der alten Ablage (`querencia-runtime/integration/theme/
  vorschlag/theme-manifest.txt`, `e72ae8ed…`), Liste der Vorlage (`BAUM_NEU`),
  Vorlage gegen Liste, alte Ablage gegen Liste, vorhandene neue Ablage gegen
  Liste, labwc-Teil der neuen Liste = alte Liste.
- Der Link muss auf die alte oder die neue Ablage zeigen, sonst Exit 2.
- Live nur mit dconf; in der Probe nur mit `GSETTINGS_BACKEND=keyfile` und
  `XDG_CONFIG_HOME` unter `QTH_STATE`.
- Sperre `flock` auf `$STATE/thema-integrieren.lock`.
- Fehler oder Signal mitten im Lauf: Link und beide gsettings-Werte zurück
  (Exit 1). Exit 3, falls das nicht vollständig gelingt.

### Probe

```bash
bash integration/probe.sh
```

Wegwerf-Ordner unter `~/.cache/querencia-thema/`, alte Ablage dort als
Kopie, gsettings als Schlüsseldatei. Die Probe prüft unter anderem Fehler an
jeder Stelle und Signale, doppeltes aktivieren und zurueck, Rückkehr zu einem
anderen Ausgangsthema, ein von Hand geändertes Thema, eine veränderte alte
Ablage, einen fremden Link und Live ohne Freigabe. Am Ende vergleicht sie die
echten gsettings und den echten Link mit dem Stand davor. Ergebnis zuletzt:
43/43.

### Nach einer Änderung am Thema

```bash
python3 -I werkzeug/erzeugen.py
bash werkzeug/vorlage-bauen.sh      # Vorlage + Liste, trägt BAUM_NEU ein
bash integration/probe.sh
bash werkzeug/summen.sh             # SHA256SUMS erneuern
```

Ändert sich der labwc-Teil in querencia-runtime (neue Ablage), müssen hier
`BAUM_ALT`, `LISTE_ALT` und die alte Ablage im Skript angepasst und die
Vorlage neu gebaut werden.
