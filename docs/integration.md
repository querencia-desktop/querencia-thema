# Integration auf der Entwicklungs-VM

Skript: `integration/thema-integrieren.sh`. Das Muster folgt
`theme-osd-integrieren.sh` (G2-R) aus querencia-runtime.

```bash
bash integration/thema-integrieren.sh pruefen
QTH_FREIGABE=ja bash integration/thema-integrieren.sh aktivieren   # nur nach Freigabe
QTH_FREIGABE=ja bash integration/thema-integrieren.sh zurueck
```

## Was „aktivieren“ tut

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

## „zurueck“

Stellt Link, `gtk-theme` und `overlay-scrolling` auf die gesicherten Werte.
Die neue Ablage bleibt liegen. Hat jemand `gtk-theme` inzwischen von Hand auf
ein drittes Thema gestellt, verweigert `zurueck` (Exit 2) und ändert nichts.

## Sicherungen und Verweigerungen

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

## Probe

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

## Nach einer Änderung am Thema

```bash
python3 -I werkzeug/erzeugen.py
bash werkzeug/vorlage-bauen.sh      # Vorlage + Liste, trägt BAUM_NEU ein
bash integration/probe.sh
bash werkzeug/summen.sh             # SHA256SUMS erneuern
```

Ändert sich der labwc-Teil in querencia-runtime (neue Ablage), müssen hier
`BAUM_ALT`, `LISTE_ALT` und die alte Ablage im Skript angepasst und die
Vorlage neu gebaut werden.
