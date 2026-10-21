# Farben

## Palette

Die Werte stimmen mit dem labwc-Thema, dem Panel (HMP-05) und den eigenen
CSS-Dateien von Rechner, Systemmonitor, Dateisuche und Software überein.

| Rolle | Wert | Herkunft |
|---|---|---|
| Fenstergrund | `#f2f1f0` | Ambiance (GTK 3) `bg_color`, Menüleisten der Programme |
| Schrift | `#3c3c3c` | Ambiance `text_color`, Panel |
| Text in Ansichten und Feldern | `#1a1a1a` auf `#ffffff` | Human/Human-Clearlooks `text_color` |
| Menügrund | `#f5f4f2` | Panelmenüs (HMP-05), labwc-Fensterwechsler |
| Rahmen hell | `#c7c2be` | Panelmenüs, Programme |
| Knopf- und Feldrand | `#a8a29d` | Anzeige des Rechners |
| Kästchenrand | `#8f8a85` | – |
| Akzent | `#F07746` | Querencia-Marke = Ambiance `selected_bg_color` |
| Auswahl-Verlauf | `#f6a179` → `#f07746`, Rand `#c6602f` | Programme (Rechner „=“, Menüs) |
| Auswahl ohne Fokus | `#c6b9a6` | Ambiance 10.04 (light-themes 0.1.6.6) `selected_bg_color` |
| Zebrazeile | `#f5f4f2` | – |
| Tooltip | Schrift weiß auf `rgba(30, 30, 30, 0.95)` | Ambiance: dunkle Tooltips |
| Verweis | `#b33c0b`, besucht `#8a3a1c` | Ambiance `link_color` #DD4814, für AA abgedunkelt |
| Gefährliche Aktion | `#cc3b35` → `#b02a24`, weiße Schrift | Ambiance `error_bg_color` #df382c, für AA abgedunkelt |
| Fensterrahmen (labwc) | `#7a7570`, Titelleiste `#eeece9` → `#d8d4d0` | Querencia-Klassisch/labwc/themerc |

Gelesene Quellen (nur lesend, Farbwerte): Ubuntu-Paket light-themes
0.1.6.6 (Lucid, Ambiance/Radiance gtk-2.0/gtkrc), human-theme 0.39.1 (Human,
Human-Clearlooks gtk-2.0/gtkrc), beide von old-releases.ubuntu.com, CC BY-SA
3.0. Zum Vergleich außerdem Ambiance GTK 3 aus dem Snap
`gtk-common-themes` (`/snap/gtk-common-themes/current/share/themes/Ambiance`).

## Auswahlschrift: dunkel statt weiß

Ubuntu und die Panelmenüs schreiben weiß auf Orange. Das ergibt 2,8:1 (unten
im Verlauf) bis 2,0:1 (oben) und verfehlt WCAG AA (4,5:1). Das Thema nimmt
`#1a1a1a` (6,2:1 bzw. 8,5:1). Die Vergleichsvariante
`werkzeug/varianten/weiss.css` zeigt die Ubuntu-Optik; die Entscheidung liegt
beim Besitzer.

## Gedimmter Text

GTK blendet `dim-label`, Platzhalter und Untertitel mit 55 % Deckkraft ab.
Das ergibt rund 3:1. Das Thema setzt 75 % (4,9:1 auf dem Fenstergrund).

## Dunkle Fassung (0.2)

Ambiance-Töne aus Ubuntu 10.04 (Menü- und Werkzeugleisten `#3c3b37`,
Schrift `#dfdbd2`, Ränder `#2b2a27`, light-themes 0.1.6.6 wie oben). Die
vollständige Zuordnung jeder Farbe der hellen Schicht steht in
`quelle/dunkel-zuordnung.txt`.

| Rolle | hell | dunkel |
|---|---|---|
| Fenstergrund, Menüleiste, Statusleiste | `#f2f1f0` | `#3c3b37` |
| Werkzeugleiste (Verlauf) | `#f7f6f5` → `#e9e7e4` | `#45443f` → `#3c3b37` |
| Schrift | `#3c3c3c` | `#dfdbd2` |
| Ansicht, Eingabefeld | `#ffffff`, Schrift `#1a1a1a` | `#2b2a27`, Schrift `#f2f1f0` |
| Menügrund, Zebrazeile | `#f5f4f2` | `#353430` |
| Knopf (Verlauf) | `#fefefe` → `#e9e6e2` | `#57554f` → `#4a4843` |
| Rahmen, Knopfrand | `#c7c2be`, `#a8a29d` | `#2b2a27`, `#23221f` |
| Akzent, Auswahl | `#f6a179` → `#f07746`, Schrift `#1a1a1a` | gleich |
| Auswahl ohne Fokus | `#c6b9a6`, Schrift `#1a1a1a` | `#6b6153`, Schrift `#f2f1f0` |
| Verweis, besucht, überfahren | `#b33c0b`, `#8a3a1c`, `#d2501a` | `#f6a179`, `#e5a383`, `#fbbb9a` |
| Info-/Warnleiste | `#fcf3c8`, `#fbdcb5` | `#4d4528`, `#5a4228` |
| deaktivierte Schrift | `#a5a09a` | `#858079` |
| Tooltip, Fehlerleiste, gefährliche Aktion | wie hell | gleich |

Die Auswahl bleibt Orange mit dunkler Schrift: das Paar hängt nicht vom
Fenstergrund ab (6,2:1 unten, 8,5:1 oben). Ein helleres Orange war nicht
nötig.

## Fehlerschrift und Tastenkürzel (0.2.1)

- **Fehlerschrift** (`label.error`, Eingabefelder mit `.error`): Das
  Grundthema setzt hell und dunkel `#cc0000`. Hell ergibt das 5,2:1 auf dem
  Fenstergrund, dunkel nur 1,9:1 auf `#3c3b37`. Die dunkle Fassung setzt
  deshalb `#ed8b85`: 4,6:1 auf Fenster und Dialog, 5,1:1 auf dem Menü und
  5,9:1 in der Ansicht. Hell bleibt `#cc0000`.
- **Tastenkürzel im Menü** (`popover.menu accelerator`, GTK 3
  `menuitem accelerator`): GTK dimmt sie auf 55 % der Schrift. Das ergibt
  hell 2,9:1 und dunkel 3,9:1. Das Thema setzt 75 %: hell 4,9:1, dunkel
  5,8:1. Auf der orangen Auswahl steht das Kürzel in voller Schrift
  `#1a1a1a` (6,2:1 unten, 8,5:1 oben). Das ist die einzige Änderung von 0.2.1
  an der hellen Darstellung: Die Kürzel sind etwas dunkler.

## Benannte Farben (0.2.1)

Programme können diese Namen in ihrer eigenen CSS verwenden, statt die
Werte fest einzutragen. Die Farben wechseln dann mit dem Farbschema, ohne
einen eigenen `@media`-Block und ohne Bindung des Programm-Providers an
`gtk-interface-color-scheme`. Die Namen stehen in `gtk.css` (hell, und
dunkel im `@media`-Block) und in `gtk-dark.css`, für GTK 4 und GTK 3. Das
Thema selbst zeichnet nichts damit. Die Programme stellen in späteren
Fassungen darauf um.

| Name | hell | dunkel | Zweck |
|---|---|---|---|
| `@sidebar_bg_color` | `#f5f4f2` | `#353430` | Grund von Seitenleisten (z. B. Software, Kategorien) |
| `@sidebar_fg_color` | `#3c3c3c` | `#e8e6e3` | Schrift auf der Seitenleiste (hell 10,0:1, dunkel 10,0:1) |
| `@menu_bg_color` | `#f5f4f2` | `#353430` | Grund eigener Menüs und Popover, wie `popover.menu` |
| `@menu_fg_color` | `#3c3c3c` | `#dfdbd2` | Schrift eigener Menüs, wie `popover.menu` (dunkel 9,0:1) |

Die Menünamen tragen genau die Werte, mit denen das Thema `popover.menu`
zeichnet. Ein Programm-Menü sieht damit aus wie die Menüs des Themas. Für
Rahmen gibt es schon `@borders` aus dem Grundthema (hell `#c7c2be`, dunkel
`#23221f`), für Ansichten `@theme_base_color`.

Beispiel (Programm-CSS):

```css
list.qs-seite { background-color: @sidebar_bg_color; color: @sidebar_fg_color; }
```

## Kontrast-Tabelle

Erzeugt mit `python3 -I werkzeug/kontrast.py --markdown`. Jedes Paar muss in
der erzeugten Datei vorkommen (hell: `gtk-4.0/gtk.css` vor dem Dunkelblock,
dunkel: `gtk-4.0/gtk-dark.css`), sonst schlägt die Prüfung fehl.

**Hell (gtk.css)**

| Element | Schrift | Grund | Kontrast | AA (4,5:1) |
|---|---|---|---|---|
| Fensterschrift auf Fenstergrund | `#3c3c3c` | `#f2f1f0` | 9,8:1 | bestanden |
| Menüeintrag auf Menügrund | `#3c3c3c` | `#f5f4f2` | 10,0:1 | bestanden |
| Text in Ansichten und Feldern | `#1a1a1a` | `#ffffff` | 17,4:1 | bestanden |
| Zebrazeile | `#1a1a1a` | `#f5f4f2` | 15,8:1 | bestanden |
| Auswahl, Verlauf oben | `#1a1a1a` | `#f6a179` | 8,5:1 | bestanden |
| Auswahl, Verlauf unten (Akzent) | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| Auswahl ohne Fokus (Ambiance-Beige) | `#1a1a1a` | `#c6b9a6` | 9,0:1 | bestanden |
| Empfohlene Aktion, oben | `#1a1a1a` | `#f8ad88` | 9,4:1 | bestanden |
| Empfohlene Aktion, unten | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| Gefährliche Aktion, oben | `#ffffff` | `#cc3b35` | 4,9:1 | bestanden |
| Gefährliche Aktion, unten | `#ffffff` | `#b02a24` | 6,6:1 | bestanden |
| Knopf, Verlauf unten | `#3c3c3c` | `#e9e6e2` | 8,9:1 | bestanden |
| Gedrückter Knopf | `#3c3c3c` | `#d6d2cd` | 7,3:1 | bestanden |
| Spaltenkopf | `#3c3c3c` | `#ecebe9` | 9,3:1 | bestanden |
| Reiter inaktiv, Verlauf unten | `#5a5652` | `#dedad6` | 5,2:1 | bestanden |
| Tooltip | `#ffffff` | `#1e1e1e` | 16,7:1 | bestanden |
| Verweis auf Fenstergrund | `#b33c0b` | `#f2f1f0` | 5,2:1 | bestanden |
| Verweis auf Weiß | `#b33c0b` | `#ffffff` | 5,9:1 | bestanden |
| Besuchter Verweis | `#8a3a1c` | `#f2f1f0` | 6,9:1 | bestanden |
| Fehlerleiste | `#ffffff` | `#c7342a` | 5,3:1 | bestanden |
| Info-/Frageleiste | `#3c3c3c` | `#fcf3c8` | 9,9:1 | bestanden |
| Warnleiste | `#3c3c3c` | `#fbdcb5` | 8,4:1 | bestanden |
| Kopfleiste (nur GTK-Dialoge), unten | `#3c3c3c` | `#d8d4d0` | 7,5:1 | bestanden |
| Schalter an (Textteil) | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| Gedimmter Text (dim-label, 75 %) auf Fenstergrund | `#3c3c3c@0.75` | `#f2f1f0` | 4,9:1 | bestanden |
| Platzhalter (75 %) im Eingabefeld | `#1a1a1a@0.75` | `#ffffff` | 7,7:1 | bestanden |
| Fehlerschrift (label.error) auf Fenstergrund | `#cc0000` | `#f2f1f0` | 5,2:1 | bestanden |
| Fehlerschrift auf Menügrund | `#cc0000` | `#f5f4f2` | 5,4:1 | bestanden |
| Fehlerschrift in Ansicht und Eingabefeld | `#cc0000` | `#ffffff` | 5,9:1 | bestanden |
| Tastenkürzel im Menü (75 %) | `#3c3c3c@0.75` | `#f5f4f2` | 4,9:1 | bestanden |
| Tastenkürzel auf Auswahl, oben | `#1a1a1a` | `#f6a179` | 8,5:1 | bestanden |
| Tastenkürzel auf Auswahl, unten | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| @sidebar_fg_color auf @sidebar_bg_color | `#3c3c3c` | `#f5f4f2` | 10,0:1 | bestanden |
| @menu_fg_color auf @menu_bg_color | `#3c3c3c` | `#f5f4f2` | 10,0:1 | bestanden |
| Deaktivierte Schrift (WCAG-Ausnahme) | `#a5a09a` | `#f2f1f0` | 2,3:1 | (Info) unter AA |
| Vergleich: Tastenkürzel bis 0.2 (55 %) | `#3c3c3c@0.55` | `#f5f4f2` | 2,9:1 | (Info) unter AA |
| Tastenkürzel auf Auswahl, gedrückt (Augenblick) | `#1a1a1a` | `#e2683a` | 5,2:1 | (Info) erfüllt |
| Vergleich: weiße Auswahlschrift (Ambiance, Panelmenü) | `#ffffff` | `#f07746` | 2,8:1 | (Info) unter AA |
| Vergleich: weiße Schrift, Verlauf oben | `#ffffff` | `#f6a179` | 2,0:1 | (Info) unter AA |

**Dunkel (gtk-dark.css und @media-Block in gtk.css)**

| Element | Schrift | Grund | Kontrast | AA (4,5:1) |
|---|---|---|---|---|
| Fensterschrift auf Fenstergrund | `#dfdbd2` | `#3c3b37` | 8,1:1 | bestanden |
| Werkzeugleiste, Verlauf oben | `#dfdbd2` | `#45443f` | 7,1:1 | bestanden |
| Menüeintrag auf Menügrund | `#dfdbd2` | `#353430` | 9,0:1 | bestanden |
| Text in Ansichten und Feldern | `#f2f1f0` | `#2b2a27` | 12,7:1 | bestanden |
| Zebrazeile | `#f2f1f0` | `#353430` | 11,0:1 | bestanden |
| Seitenleiste | `#f2f1f0` | `#34332f` | 11,2:1 | bestanden |
| Auswahl, Verlauf oben | `#1a1a1a` | `#f6a179` | 8,5:1 | bestanden |
| Auswahl, Verlauf unten (Akzent) | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| Auswahl ohne Fokus (dunkles Beige) | `#f2f1f0` | `#6b6153` | 5,4:1 | bestanden |
| Empfohlene Aktion, oben | `#1a1a1a` | `#f8ad88` | 9,4:1 | bestanden |
| Empfohlene Aktion, unten | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| Gefährliche Aktion, oben | `#ffffff` | `#cc3b35` | 4,9:1 | bestanden |
| Gefährliche Aktion, unten | `#ffffff` | `#b02a24` | 6,6:1 | bestanden |
| Knopf, Verlauf oben | `#dfdbd2` | `#57554f` | 5,4:1 | bestanden |
| Knopf, Verlauf unten | `#dfdbd2` | `#4a4843` | 6,6:1 | bestanden |
| Knopf überfahren, oben | `#dfdbd2` | `#5f5d57` | 4,8:1 | bestanden |
| Gedrückter Knopf | `#dfdbd2` | `#33322e` | 9,3:1 | bestanden |
| Spaltenkopf, oben | `#dfdbd2` | `#55534d` | 5,6:1 | bestanden |
| Spaltenkopf, unten | `#dfdbd2` | `#46443f` | 7,0:1 | bestanden |
| Reiter inaktiv, Verlauf oben | `#bdb7b1` | `#36352f` | 6,2:1 | bestanden |
| Reiter inaktiv, Verlauf unten | `#bdb7b1` | `#2f2e2a` | 6,8:1 | bestanden |
| Schalter aus (Textteil) | `#bdb7b1` | `#2f2e2a` | 6,8:1 | bestanden |
| Schalter an (Textteil) | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| Tooltip | `#ffffff` | `#1e1e1e` | 16,7:1 | bestanden |
| Verweis auf Fenstergrund | `#f6a179` | `#3c3b37` | 5,5:1 | bestanden |
| Verweis auf Ansicht | `#f6a179` | `#2b2a27` | 7,0:1 | bestanden |
| Besuchter Verweis | `#e5a383` | `#3c3b37` | 5,3:1 | bestanden |
| Verweis überfahren | `#fbbb9a` | `#3c3b37` | 6,8:1 | bestanden |
| Fehlerleiste | `#ffffff` | `#c7342a` | 5,3:1 | bestanden |
| Info-/Frageleiste | `#dfdbd2` | `#4d4528` | 6,9:1 | bestanden |
| Warnleiste | `#dfdbd2` | `#5a4228` | 6,8:1 | bestanden |
| Kopfleiste (nur GTK-Dialoge), unten | `#dfdbd2` | `#3c3b37` | 8,1:1 | bestanden |
| Gedimmter Text (dim-label, 75 %) auf Fenstergrund | `#dfdbd2@0.75` | `#3c3b37` | 5,4:1 | bestanden |
| Platzhalter (75 %) im Eingabefeld | `#f2f1f0@0.75` | `#2b2a27` | 7,8:1 | bestanden |
| Skalenmarken | `#b3aea7` | `#3c3b37` | 5,1:1 | bestanden |
| Fehlerschrift (label.error) auf Fenstergrund und Dialog | `#ed8b85` | `#3c3b37` | 4,6:1 | bestanden |
| Fehlerschrift auf Menügrund | `#ed8b85` | `#353430` | 5,1:1 | bestanden |
| Fehlerschrift in Ansicht und Eingabefeld | `#ed8b85` | `#2b2a27` | 5,9:1 | bestanden |
| Tastenkürzel im Menü (75 %) | `#dfdbd2@0.75` | `#353430` | 5,8:1 | bestanden |
| Tastenkürzel auf Auswahl, oben | `#1a1a1a` | `#f6a179` | 8,5:1 | bestanden |
| Tastenkürzel auf Auswahl, unten | `#1a1a1a` | `#f07746` | 6,2:1 | bestanden |
| @sidebar_fg_color auf @sidebar_bg_color | `#e8e6e3` | `#353430` | 10,0:1 | bestanden |
| @menu_fg_color auf @menu_bg_color | `#dfdbd2` | `#353430` | 9,0:1 | bestanden |
| Deaktivierte Schrift (WCAG-Ausnahme) | `#858079` | `#3c3b37` | 2,9:1 | (Info) unter AA |
| Deaktivierte Schrift im Feld (WCAG-Ausnahme) | `#858079` | `#353430` | 3,2:1 | (Info) unter AA |
| Vergleich: Fehlerschrift bis 0.2 (#cc0000) | `#cc0000` | `#3c3b37` | 1,9:1 | (Info) unter AA |
| Vergleich: Tastenkürzel bis 0.2 (55 %) | `#dfdbd2@0.55` | `#353430` | 3,9:1 | (Info) unter AA |
| Vergleich: weiße Auswahlschrift (Ambiance) | `#ffffff` | `#f07746` | 2,8:1 | (Info) unter AA |
