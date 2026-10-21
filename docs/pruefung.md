# Prüfung

Alle Prüfungen laufen isoliert. Die Live-Sitzung, dconf und der echte
Theme-Link bleiben unberührt.

## Werkzeuge

| Werkzeug | Zweck |
|---|---|
| `werkzeug/isoliert.py` | Eigener headless labwc 0.9.8, eigener D-Bus, eigenes `XDG_RUNTIME_DIR` und XDG-Profil, `GSETTINGS_BACKEND=memory`. Übernommen aus querencia-rechner (G2-H). Ergänzt um das Aushängen des eigenen gvfs-Mounts und den Portal-Modus `QTH_PORTALE=1`. |
| `werkzeug/belege.sh <fall> <BxH> <thema>` | Ein Fall, ein Bild bzw. zwei (zweites mit per F10 geöffnetem Menü). `thema`: `vorher` (GTK-Standard wie heute live), `nachher`, `weiss`, `dunkel` (Vergleichsvarianten), `farbschema` (0.2: hell starten, über das Portal auf dunkel und zurück, eigenes HOME), `gtkdark` (0.2: `GTK_THEME=…:dark`, lädt `gtk-dark.css`). `QTH_THEMA_QUELLE` nimmt das Thema aus einer Ablage. Alle Läufe mit `GSK_DEBUG=full-redraw`. |
| `werkzeug/belege-02.sh [ziel]` | 0.2: Bilder hell/dunkel (Einstellungen, Files, Editor, Panel-Menü in 1024×768 und 1920×1080, weitere Programme in 1024×768) und Regression hell gegen die Live-Ablage, nach  (ca. 15 min) |
| `werkzeug/lauf-farbschema.sh` | läuft in der Isolation: Programm hell, `color-scheme prefer-dark`, Menü, zurück auf `default`; je Schritt ein Bild |
| `werkzeug/farbschema-start.sh`, `farbschema-probe.py` | 0.2: Startfehler von GTK 4.22 (Neustart unter `prefer-dark` bleibt hell, mit `Settings.notify` dunkel) |
| `werkzeug/bildvergleich.py` | Pixelvergleich zweier PNG mit Bereich der Abweichung, Pixel lesen |
| `werkzeug/css-sichten.py`, `css-sichten-liste.txt` | 0.2: feste Hellfarben in der eigenen CSS der Programme (Live-Stände, nur `git show`) |
| `werkzeug/alle-belege.sh` | Alle Fälle in 1024×768 und 1920×1080 (ca. 15 min), nach `nachweis/bilder/` |
| `werkzeug/muster4.py`, `muster3.py` | Musterseiten mit allen Elementarten (GTK 4 über PyGObject, GTK 3 über ctypes, weil die VM kein GI für GTK 3 hat) |
| `werkzeug/lauf-portal.sh`, `doc-stellvertreter.py` | Portal-Probe: xdg-desktop-portal(-gtk) im Wegwerf-Bus, gsettings als Schlüsseldatei im Profil, Dokumentenportal nur als Stellvertreter (kein FUSE-Mount, PT-1) |
| `werkzeug/kontrast.py` | WCAG-Kontrast aller Schrift/Grund-Paare |
| `werkzeug/regression-021.sh`, `lauf-021.sh` | 0.2.1: Regression gegen die Live-Ablage in der gekürzten Matrix (de 1024×768, en 1920×1080; hell und dunkel über das Portal, Cursor ohne Blinken); Archiv mit falschem Kennwort (`label.error`), Menüs per F10 (Tastenkürzel); Pixelvergleich neu gegen live, nach  (ca. 5 min mit 4 parallelen Läufen) |
| `werkzeug/farbzaehler.py` | 0.2.1: Pixel einer Farbe in einem Bereich zählen (Beleg für neue Farbwerte) |
| `werkzeug/farbnamen-probe.sh`, `farbnamen-probe.py` | 0.2.1: benannte Farben aus einem Programm-Provider ohne Bindung, hell, dunkel, Neustart mit und ohne `Settings.notify` |
| `werkzeug/fokus-probe.sh`, `fokus-probe.py` | 0.2.1: Fokus und `focus-visible` nach Farbschema-Wechsel und nach F10/Esc, Querencia gegen GTK-Default |
| `integration/probe.sh`, `integration/probe-02.sh`, `integration/021/probe-021.sh` | Probe der Integrationsskripte 0.1, 0.2 und 0.2.1 |

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

## Ergebnisse 0.2.1 (21.10.2026)

- **Kontrast:** `kontrast.py` Exit 0, hell 34/34 und dunkel 43/43
  Pflichtpaare nach AA (docs/farben.md).
- **Regression gegen die Live-Ablage 0.2** (`regression-021.sh`, 48 Läufe,
  alle „fertig“): 50 Bildpaare, 38 pixelgleich. Die 12 Abweichungen liegen
  nur an den beabsichtigten Stellen:
  - hell und dunkel die Spalte der Tastenkürzel in den Menüs von Dokumente,
    Editor und Rechner (Bereich je nur die Kürzel);
  - dunkel die Fehlerzeile im Kennwortfenster von Archiv.
  - Pixelgleich: alle Startbilder, Archiv hell mit Fehlerzeile, die
    Kennwortfenster vor der Eingabe, Einstellungen, Musterseiten (deren
    Menüs haben keine Kürzel).
- **Farbwerte im Bild** (`farbzaehler.py`): Archiv dunkel, Fehlerzeile neu
  122 Pixel `#ed8b85` und 0 `#cc0000`, live umgekehrt; hell beide
  122 `#cc0000`. Dokumente-Menü hell neu 45 Pixel `#6a6a6a` (75 % auf
  `#f5f4f2`), live 49 `#8f8f8e` (55 %); dunkel neu 45 `#b4b1aa`.
- **Benannte Farben** (`farbnamen-probe.sh`): aus einem Programm-Provider
  ohne Bindung hell `#f5f4f2 #3c3c3c #f5f4f2 #3c3c3c`, nach dem Wechsel
  dunkel `#353430 #e8e6e3 #353430 #dfdbd2`, zurück hell. Ein Neustart unter
  `prefer-dark` bleibt ohne `Settings.notify` hell (GTK-4.22-Startfehler,
  docs/aufbau.md), mit `notify` dunkel.
- **Fokus nach Farbschema-Wechsel** (`fokus-probe.sh`, Notiz Systemmonitor
  0.1.3): Der Wechsel allein verschiebt weder Fokus noch Fokusrahmen
  (Start = zurück, pixelgleich, mit Querencia und mit GTK-Default). Nach
  F10/Esc bleibt der Fokus in GTK auf dem Menüleisten-Eintrag (Zustand
  `:focus :hover`). `focus-visible` geht nach Tasten an und ohne Taste nach
  wenigen Sekunden von selbst aus. Querencia zeichnet `menubar > item:hover`
  orange, deshalb sieht man den behaltenen Zustand; GTK-Default zeichnet
  `:hover` dort nicht. Einordnung: GTK-Verhalten, vom Thema sichtbar
  gemacht, kein Programmfehler; für Pixelvergleiche jede Folge mit
  derselben Eingabe beginnen.
- **Integration:** Probe 0.2.1 52/52; `pruefen` live Exit 0 (Link auf
  0.2, Ablage 0.2.1 fehlt, SHA256SUMS der Vorlage in Ordnung).

## Ergebnisse 0.2 (20.10.2026, dunkle Fassung)

- **Umschalten über das Portal:** Einstellungen, Panel (Leisten), die
  Musterseiten und die Ansichten von Editor, Systemmonitor und Rechner
  wechseln beim Setzen von `color-scheme prefer-dark` sofort ins Dunkle und
  beim Zurücksetzen wieder ins Helle (Pixelprobe: Fenstergrund `#f2f1f0` →
  `#3c3b37` → `#f2f1f0`). Bilder: 
  (`*-1-hell`, `*-2-dunkel`, `*-3-dunkel-menue`, `*-4-wieder-hell`).
- **Startfehler GTK 4.22:** ein Programm, das unter `prefer-dark` neu
  startet, bleibt hell (`#3c3c3c`); mit einmal `Settings.notify` nach dem
  Start dunkel (`#dfdbd2`). Beleg `werkzeug/farbschema-start.sh`.
- **`gtk-dark.css`** lädt mit `GTK_THEME=Querencia-Klassisch:dark` in GTK 4
  und GTK 3 (Bilder `gtk-dark/`). GTK 3 folgt `color-scheme` nicht.
- **Regression hell:** Repo 0.2 gegen Live-Ablage 0.1, isoliert, 17 Bilder:
  13 pixelgleich; Abweichungen nur am Textcursor (Editor, 1 px breit), am
  laufenden Spinner (Regler-Musterseite) und an Messwerten (Systemmonitor).
  Ein Gegenlauf Live gegen Live zeigt dieselben Stellen.
- **Programm-CSS:** Wo Programme feste helle Flächen setzen (Menüleisten,
  Menüs, Statusleisten, Reiter, Rechneranzeige, Software-Listen,
  Benachrichtigungen), bleiben diese hell; in Menüs mit eigenem hellem Grund
  wird die Schrift des Themas hell und unleserlich (Editor, Bilder, Rechner,
  Systemmonitor, Dateisuche, Software). Liste mit Datei:Zeile in der
  Übergabe Thema 0.2. Files folgt seinem eigenen Strata-Thema und bleibt
  hell; der labwc-Rahmen bleibt hell.
- **Kontrast:** 35 Pflichtpaare der dunklen Fassung bestehen WCAG AA
  (`docs/farben.md`), die 26 der hellen weiterhin.

## Ergebnisse 0.1 (20.10.2026)

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
