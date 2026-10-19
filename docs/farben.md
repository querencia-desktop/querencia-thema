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

## Kontrast-Tabelle

Erzeugt mit `python3 -I werkzeug/kontrast.py --markdown`. Jedes Paar muss in
der erzeugten `gtk-4.0/gtk.css` vorkommen, sonst schlägt die Prüfung fehl.

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
| Deaktivierte Schrift (WCAG-Ausnahme) | `#a5a09a` | `#f2f1f0` | 2,3:1 | (Info) unter AA |
| Vergleich: weiße Auswahlschrift (Ambiance, Panelmenü) | `#ffffff` | `#f07746` | 2,8:1 | (Info) unter AA |
| Vergleich: weiße Schrift, Verlauf oben | `#ffffff` | `#f6a179` | 2,0:1 | (Info) unter AA |
