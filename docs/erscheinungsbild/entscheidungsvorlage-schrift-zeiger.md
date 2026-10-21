# Entscheidungsvorlage Schrift und Mauszeiger (Thema-3)

Stand 20.10.2026 00:40. Für den Besitzer, über die Status-Session.
Belegbilder: nicht veröffentlicht (Entwicklungsumgebung).

## 0. Ist-Stand (gemessen, nur gelesen)

| Was | Wert | Wirklich sichtbar |
|---|---|---|
| `font-name` | `Adwaita Sans 11` | **DejaVu Sans 11** – Adwaita Sans ist nicht installiert, fontconfig ersetzt sie |
| `document-font-name` | `Adwaita Sans 12` | DejaVu Sans 12 |
| `monospace-font-name` | `Monospace 11` | DejaVu Sans Mono 11 |
| Fenstertitel (rc.xml) | kein `<font place="ActiveWindow">` | labwc-Standard `sans 10`, normal (nicht fett) → DejaVu Sans 10 |
| Fensterwechsler (rc.xml) | `OnScreenDisplay` = `Adwaita Sans 11` | DejaVu Sans 11 |
| `cursor-theme` / `cursor-size` | `Adwaita` / `24` | – |
| `XCURSOR_THEME`/`XCURSOR_SIZE` (labwc-environment) | nicht gesetzt | `default` → `Inherits=Adwaita`, 24 |
| Schriften installiert | DejaVu Sans/Serif/Mono (`fonts-dejavu-core`), Noto Color Emoji | |
| Zeigerthemen installiert | nur Adwaita | |

Wichtig für den Zeiger: GTK 4.22 fragt den Zeiger über `cursor-shape-v1` beim
Compositor an. Was man über Fenstern und auf dem Desktop sieht, bestimmt
deshalb **labwc** mit `XCURSOR_THEME`/`XCURSOR_SIZE`; der gsettings-Schlüssel
`cursor-theme` gilt nur für Programme, die den Zeiger selbst zeichnen
(Rückfall, XWayland). Beides muss gleich gesetzt werden.

## 1. Pakete in Ubuntu 26.04.1 (apt-cache policy, nur gelesen)

| Paket | Kandidat | Archiv | installiert | Lizenz (debian/copyright, Font-`name`-Tabelle) |
|---|---|---|---|---|
| fonts-dejavu-core | 2.37-8build1 | main | **ja** | Bitstream-Vera-Lizenz, DejaVu-Änderungen gemeinfrei |
| fonts-dejavu-extra | 2.37-8build1 | main | nein | wie oben (echte Kursive/Oblique, Condensed) |
| fonts-ubuntu | 0.869+git20240321 | main | nein | **Ubuntu Font Licence 1.0** (Ubuntu, Ubuntu Sans, Ubuntu Mono, Ubuntu Sans Mono; auch Ubuntu Sans hat in diesem Paket UFL) |
| fonts-ubuntu-classic | 0.83-6ubuntu2 | universe | nein | UFL 1.0; **Conflicts: fonts-ubuntu** (beide heißen „Ubuntu“) |
| fonts-liberation | 2.1.5-3build1 | main | nein | OFL-1.1 |
| fonts-cantarell | 0.303.1-4 | universe | nein | OFL-1.1 |
| fonts-noto-core | 20201225-2build1 | main | nein | OFL-1.1 (13 MB) |
| fonts-adwaita-sans | 49.0+dfsg-2 | universe | nein | OFL-1.1 (`fonts-adwaita` ist nur ein Sammelpaket) |
| dmz-cursor-theme | 0.4.5.3build1 | main | nein | **CC-BY-SA-3.0** (Bilder), GPL-2+ (Erzeugungsskript) |
| xcursor-themes (whiteglass …) | 1.0.6 | main | nein | MIT/X11 |
| breeze-cursor-theme | 6.6.5 | universe | nein | GPL-2+ |

## 2. Schrift – Empfehlung

**Variante A (empfohlen): genau Ubuntu 10.04 – DejaVu, alles 10 pt.**
GNOME 2 in Ubuntu 10.04 stand auf „Sans 10“ (Anwendung, Dokument),
„Sans Bold 10“ (Fenstertitel) und „Monospace 10“, aufgelöst nach DejaVu.

| Rolle | Schlüssel/Ort | Wert 1920×1080 | Wert 1024×768 |
|---|---|---|---|
| Oberfläche | `font-name` | `DejaVu Sans 10` | `DejaVu Sans 10` |
| Dokumente | `document-font-name` | `DejaVu Sans 10` | `DejaVu Sans 10` |
| Dicktengleich | `monospace-font-name` | `DejaVu Sans Mono 10` | `DejaVu Sans Mono 10` |
| Fenstertitel | rc.xml `ActiveWindow`/`InactiveWindow` | `DejaVu Sans`, 10, bold | gleich |
| Fensterwechsler | rc.xml `OnScreenDisplay` | `DejaVu Sans` 10 | gleich |

Begründung:
- Das ist der Originalzustand des Vorbilds; die Schrift ist schon installiert
  (kein Paket nötig) und heute ohnehin sichtbar – nur 11/12 pt statt 10 pt
  und ein Schriftname, den es nicht gibt.
- Größe: GTK rechnet Punkt immer mit 96 dpi, die Auflösung ändert die
  Pixelgröße nicht. Der Monitor (ASUS VS247, 520×290 mm bei 1920×1080)
  hat ~94 dpi, 10 pt sind dort ~13 px wie bei 10.04 auf einem 96-dpi-Bildschirm.
  Bei 1024×768 (VM-Fenster, alte 15″) ist 10 pt Pflicht, 11–12 pt lassen
  Dialoge über den Rand wachsen. Deshalb eine Größe für beide.
- Titel fett wie 10.04 (heute normal, weil rc.xml nichts setzt).
- Optional `fonts-dejavu-extra`: echte Kursive (DejaVu Sans Oblique) statt
  von Pango schräg gerechneter; nicht nötig für den Anblick der Oberfläche.

**Variante B: Ubuntu-Schrift (Look ab Ubuntu 10.10).** `Ubuntu 10`,
`Ubuntu 10`, `Ubuntu Mono 11` (zeichnet kleiner, deshalb 11), Titel
`Ubuntu Bold 10`; Paket `fonts-ubuntu` (main). Nicht 10.04, aber das, was
viele mit „Ubuntu klassisch“ verbinden. UFL 1.0 erlaubt Nutzung und
Weitergabe; abgeleitete (veränderte) Schriften müssen umbenannt werden,
„Ubuntu“ ist eine Marke von Canonical (TRADEMARKS.txt im Paket). Nicht
OSI-geprüft; Debian-Status nicht geprüft.

Nicht empfohlen: Cantarell, Adwaita Sans, Noto Sans (GNOME-3/4-Anmutung),
Liberation Sans (Arial-Ersatz, für Dokumente gedacht). Vergleich in
`schriften-*/s00-uebersicht-*.png`.

## 3. Mauszeiger – Empfehlung

**DMZ-White, Größe 24** (`dmz-cursor-theme`, main). Das ist der Zeiger von
Ubuntu 10.04: weißer Pfeil mit schwarzem Rand. Größe 24 ist die heutige
Größe und eine der drei eingebauten Stufen (24, 32, 48), wird also nicht
skaliert; 32 nur auf Wunsch (größer, Barrierefreiheit/HiDPI).

Geprüft in der isolierten labwc-Sitzung (`zeiger/00-kontaktbogen-zeiger.png`):
Pfeil auf freier Fläche, I-Balken über dem Textfeld, Pfeil über der
Titelleiste, Größenänderungspfeil am Rand – alle aus DMZ-White. DMZ-White
hat nur die alten X11-Namen (`left_ptr`, `xterm` …), keine CSS-Namen
(`default`, `text`, `pointer`); wlroots 0.19 und GTK fallen für die
geprüften Fälle auf die alten Namen zurück. Nicht einzeln geprüft: seltene
Formen (`not-allowed`, `col-resize`, `zoom-in`) – fehlt eine, zeigt labwc
den Standardpfeil.

Vergleich: DMZ-Black ≈ heutiges Adwaita (schwarz), whiteglass (X.org,
unscharf bei 24), Breeze (KDE). Kein Kandidat sieht 10.04 ähnlicher.

**Eigenes Querencia-Zeigerthema – nur Vorschlag, nicht gebaut:**
„Querencia-Klassisch“ auf Basis DMZ-White (CC-BY-SA-3.0 → die Ableitung
wäre ebenfalls CC-BY-SA, Namensnennung Novell), ergänzt um alle CSS-Namen
als Links und einen Warte-Zeiger in der Akzentfarbe `#F07746`; erzeugt aus
SVG mit `xcursorgen`, Stufen 24/32/48. Lohnt sich erst, wenn Zeiger Teil
der Marke werden sollen.

## 4. Lizenz und Veröffentlichung (analog LIZENZEN.md Q9)

Schriften und Zeiger werden **nicht mitgeliefert**, sondern nur empfohlen:
das Repo `querencia-erscheinungsbild` (GPL-3.0-or-later) enthält nur die
Namen in den Einstellungen, keine Font- oder Xcursor-Datei. Später im
Metapaket `querencia-desktop` als `Recommends: dmz-cursor-theme,
fonts-dejavu-core` (Variante B: `fonts-ubuntu`). Damit gibt es keine
Lizenzfolge für die Querencia-Quellen. Würde man DMZ-White mitliefern:
CC-BY-SA-3.0 verlangt Namensnennung und gleiche Lizenz für diese Dateien –
verträglich, aber unnötig.

## 5. Was pottrauschen installiert (sudo) und was ohne sudo geht

Mit sudo (empfohlen, bekommt Sicherheits- und Paketaktualisierungen):

```bash
sudo apt install dmz-cursor-theme fonts-dejavu-extra
```

Variante B zusätzlich `fonts-ubuntu`. Variante A ohne Kursive braucht nur
`dmz-cursor-theme`.

Ohne sudo (das Integrationsskript kann das, falls der Besitzer kein apt will):
`apt-get download` + `dpkg -x` in einen Wegwerfordner, dann

- Zeiger: `…/usr/share/icons/DMZ-White/` → `~/.local/share/icons/DMZ-White/`
  (labwc/wlroots sucht dort zuerst: `$XDG_DATA_HOME/icons`)
- Schriften: `…/usr/share/fonts/truetype/…/*.ttf` → `~/.local/share/fonts/<paket>/`, dann `fc-cache`

Nachteil: keine Aktualisierung über apt; eine spätere Paketinstallation
ist harmlos (die Benutzerkopie hat Vorrang, gleicher Inhalt).

## 6. Was wann wirkt

- gsettings (Oberfläche, Dokumente, Dicktengleich, `cursor-theme`/`-size`):
  sofort in laufenden GTK-Programmen (Panel, Desktop, Files, Einstellungen).
- Fenstertitel (rc.xml) und `XCURSOR_THEME`/`XCURSOR_SIZE`: nicht im
  Runtime-Repo, sondern in der Benutzerkopie `~/.config/querencia/labwc/`
  (G2-AG): `rc.xml` `<theme><font place="ActiveWindow|InactiveWindow|OnScreenDisplay">`
  und `environment.d/*.env`. Wirkt erst, wenn G2-AG Teil A greift (ab der
  nächsten Anmeldung), dann mit `labwc --reconfigure` bzw. nach erneuter
  Anmeldung.
