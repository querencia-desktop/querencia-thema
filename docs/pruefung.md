# Prüfung

Alle Prüfungen laufen isoliert. Die Live-Sitzung, dconf und der echte
Theme-Link bleiben unberührt.

## Werkzeuge

| Werkzeug | Zweck |
|---|---|
| `werkzeug/isoliert.py` | Eigener headless labwc 0.9.8, eigener D-Bus, eigenes `XDG_RUNTIME_DIR` und XDG-Profil, `GSETTINGS_BACKEND=memory`. Übernommen aus querencia-rechner (G2-H). Ergänzt um das Aushängen des eigenen gvfs-Mounts und den Portal-Modus `QTH_PORTALE=1`. |
| `werkzeug/belege.sh <fall> <BxH> <thema>` | Ein Fall, ein Bild bzw. zwei (zweites mit per F10 geöffnetem Menü). `thema`: `vorher` (GTK-Standard wie heute live), `nachher`, `weiss`, `dunkel` (Vergleichsvarianten). |
| `werkzeug/alle-belege.sh` | Alle Fälle in 1024×768 und 1920×1080 (ca. 15 min), nach `nachweis/bilder/` |
| `werkzeug/muster4.py`, `muster3.py` | Musterseiten mit allen Elementarten (GTK 4 über PyGObject, GTK 3 über ctypes, weil die VM kein GI für GTK 3 hat) |
| `werkzeug/lauf-portal.sh`, `doc-stellvertreter.py` | Portal-Probe: xdg-desktop-portal(-gtk) im Wegwerf-Bus, gsettings als Schlüsseldatei im Profil, Dokumentenportal nur als Stellvertreter (kein FUSE-Mount, PT-1) |
| `werkzeug/kontrast.py` | WCAG-Kontrast aller Schrift/Grund-Paare |
| `integration/probe.sh` | Probe des Integrationsskripts |

Eingaben (`qeingabe`) und Auflösung (`qausgabe`) kommen aus
`querencia-rechner/werkzeug/bin` (`QTH_WERKZEUG_BIN`). Sie verweigern den
Dienst außerhalb einer isolierten Sitzung. Die Programme sind die
Live-Binaries aus `~/opt/querencia` (nur ausgeführt, in der Isolation).

Fälle: Musterseiten (Knöpfe und Felder, Listen, Regler, Text, Dialog,
Popover, Tooltip, kleines Fenster), GTK-3-Musterseite (Felder, Liste) sowie
Einstellungen, Files, Rechner, Editor, Systemmonitor, Dateisuche, Software,
Bilder, Panel (mit offenem Menü) und Desktop.

## Wie die Tests das Thema setzen

- GTK 4 ohne Portal (`GDK_DEBUG=no-portals`): `settings.ini` im Profil mit
  `gtk-theme-name` und `gtk-overlay-scrolling=false`.
- GTK 3: `GTK_THEME=Querencia-Klassisch`, `GTK_OVERLAY_SCROLLING=0`.
  Unter Wayland liest GTK 3 gsettings (im Test nur im Speicher), nicht
  `settings.ini`.
- Portal-Probe: wie live über gsettings → Portal → Programm.

## Ergebnisse (20.10.2026)

- **Alle Programme** sehen mit dem Thema stimmig aus. Wo sie eigene CSS haben
  (Menüs, Listen, Panel), bleibt diese vorrangig und passt farblich.
  Vorher/nachher je Programm in beiden Auflösungen:
  .
- **Portal-Probe:** Ein laufendes GTK-4-Programm und das Panel wechseln das
  Thema sofort, sobald `gtk-theme` umgestellt wird; das Thema verschwindet
  ebenso sofort beim Zurückstellen. Ohne Portal fällt GTK 4.22 auf das
  eingebaute „Default“ zurück (`start Default` im Diagnoseprotokoll), gsettings
  liest es dann nicht.
- **Lange Listen:** ColumnView mit 200 Zeilen und Zebrastreifen,
  Systemmonitor mit rund 450 Prozessen. Die Scrollbalken sind dauerhaft
  sichtbar und klassisch.
- **Kleine Fenster:** Rechner (300 px breit) unverändert gut. Die
  Mindestgröße bestimmen die Programme, nicht das Thema. Die Musterseite
  hält z. B. 810 px Breite.
- **Kontrast:** 26 Pflichtpaare bestehen WCAG AA, siehe `docs/farben.md`.
- **Unverändert gegenüber vorher und nicht vom Thema verursacht:** Files ist
  in 1024×768 breiter als der Bildschirm (Standardgröße des Programms);
  Systemmonitor kürzt lange PIDs („1511…“); Bilder zeigt den Hinweis „Kein
  Bild geöffnet“ grau auf grau (eigene CSS).
