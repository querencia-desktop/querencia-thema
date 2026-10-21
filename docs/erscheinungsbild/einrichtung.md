# Erscheinungsbild: Einrichtung, labwc-Werte, Proben

> Aus dem früheren Arbeitsrepo `querencia-erscheinungsbild` übernommen (Stand 0.1,
> 20.10.2026). Das Integrationsskript und die Probewerkzeuge, die hier beschrieben
> sind, gehören zur Entwicklungsumgebung und liegen **nicht** in diesem Repo; die
> labwc-Werte stehen in [labwc/](labwc/), die Einrichtung auf einem System übernimmt
> künftig das Paket.

## Skript `integration/erscheinungsbild-integrieren.sh`

| Befehl | Wirkung |
|---|---|
| `pruefen` | nur lesen: fünf gsettings-Schlüssel (alt/neu/gleich/fremd), Zeigerthema, Schriften, labwc-Benutzerkopie (`XCURSOR_*`, Fenstertitel), letzte Sicherung |
| `aktivieren` | `QEB_FREIGABE=ja`; sichert die fünf Werte (mit Kennung „standard“, wenn sie dem Schema-Standard entsprachen), kopiert fehlende Zeiger/Schriften aus `QEB_PAKETE` (nur byte-gleich mit `vorlage/*.liste`), setzt die Schlüssel, prüft jeden, schreibt ins Journal `~/opt/querencia/protokoll.txt` |
| `zurueck` | `QEB_FREIGABE=ja`; stellt die Sicherung her (`gsettings reset` für Standardwerte), entfernt nur selbst angelegte, unveränderte Ordner |
| `labwc-vorschlag` | gibt die Werte für rc.xml und environment.d aus |

Zustände je Schlüssel: **alt** = Live-Stand 20.10.2026 (Schema-Standard:
`Adwaita Sans 11`, `Adwaita Sans 12`, `Monospace 11`, `Adwaita`, `24`),
**neu** = Ziel, **gleich** = Ziel und Ausgang stimmen überein
(`cursor-size` 24), **fremd** = anderer Wert → `aktivieren`/`zurueck`
ändern nichts (Exit 2).

Exit-Codes: 0 erledigt, 1 zurückgerollt, 2 verweigert (nichts geändert),
3 Rückrollen unvollständig. Sperre `…/state/querencia/erscheinungsbild/.sperre`.

Sicherungen: `~/.local/state/querencia/erscheinungsbild/sicherung-<zeit>/`
(`gsettings.txt`, `ziel.txt`, `auswahl.txt`, `angelegt.txt`), Link `letzte`;
nach `zurueck` heißt der Ordner `….zurueckgenommen`.

Was wann wirkt: gsettings sofort in allen GTK-Programmen (über den
Settings-Portal). Der Zeiger über Fenstern und auf dem Desktop kommt von
labwc (`cursor-shape-v1`), also erst mit `XCURSOR_THEME` in der
labwc-Konfiguration.

## labwc: Fenstertitel und Zeiger kommen aus der Runtime-Vorgabe (G2-AG)

Das Skript setzt nur gsettings. Fenstertitel-Schrift (DejaVu Sans Bold 10,
Menü und Fensterwechsler DejaVu Sans 10) und `XCURSOR_THEME=DMZ-White`,
`XCURSOR_SIZE=24` liest labwc aus seiner Konfiguration. Entscheidung der
Status-Session (20.10.2026, nach Antwort von G2-AG): Diese Werte kommen als
Querencia-Standard in die **Vorgabe im Runtime-Repo**
(`session/querencia/labwc/rc.xml` und `environment`), gebaut und
freigegeben von G2-AG. Der Sitzungsstarter übernimmt sie in die
Benutzerkopie `~/.config/querencia/labwc/`, solange der Benutzer die Datei
nicht geändert hat.

Verworfen wurde Fassung 0.2 (Tag `erscheinungsbild/0.2`, git note an
`da74d51`: **nicht verwendet, nie aktiviert**), die einen markierten Block
in die Benutzer-rc.xml und `environment.d/querencia-erscheinungsbild.env`
geschrieben hätte. Gründe (G2-AG): labwc sortiert `environment.d`
alphabetisch, die Datei käme nach `querencia-einstellungen.env` und
überstimmte die Wahl des Benutzers; ein Block in der Benutzer-rc.xml macht
die Datei „vom Benutzer geändert“, danach kommen keine neuen Vorgaben mehr
an und Einstellungen verweigert „Neue Vorgabe übernehmen“.

[`labwc/`](labwc/) enthält die an G2-AG übergebenen Werte (Stand 0.1);
`labwc-vorschlag` gibt sie aus, `pruefen` zeigt, ob sie in der
Benutzerkopie angekommen sind. Isoliert belegt (`werkzeug/doppelort.sh`):
Bei zwei `<font place="…">` nimmt labwc 0.9.8 den späteren.

## Probe und Belege (`werkzeug/`)

| Datei | Zweck |
|---|---|
| `probe.sh`, `probe-innen.sh` | Skriptprobe mit Umlenkung: eigener Bus (dbus-run-session, eigener dconf-service), XDG-Ordner in `gui-test/probe`; 107 Prüfungen (Ausgang→A→zurück, fremd, Variante B mit Kopierweg, 13 Fehler-/Signalstellen, Sperre, labwc-Vorschlag); prüft, dass die Live-dconf-Datei byte-gleich bleibt |
| `isoliert.py` | isolierte headless-labwc-Sitzung (nach querencia-symbole) |
| `profil.sh`, `beleg-lauf.sh` | Wegwerfprofil aus dem Live-Stand und ein Lauf |
| `settings-portal.py` | Ersatz für den Settings-Portal im Wegwerf-Bus (der echte braucht den Dokumente-Portal mit FUSE-Mount) |
| `teil1-schriften.sh`, `textprobe.py`, `kandidaten-*.txt` | Textprobe je Schriftkandidat, Fenstertitel per `labwc --reconfigure` |
| `teil1-zeiger.sh`, `kontaktbogen.*` | Zeigerthemen mit Lupe, Kontaktbogen |
| `teil2.sh`, `rcxml-vorschlag.py` | vorher/nachher: Panel, Menü, Einstellungen, Files, Zeiger |
| `doppelort.sh` | belegt, dass bei zwei `<font place>` der spätere gilt |
| `pakete-holen.sh` | `apt-get download` + `dpkg -x` in einen Wegwerfordner |

Eingaben und Ausgabegröße kommen aus `querencia-symbole/werkzeug/bin/`
(`qeingabe`, `qausgabe`; sie arbeiten nur in einem Laufzeitordner
`qed-runtime-*`).
