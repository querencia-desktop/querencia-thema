# Erscheinungsbild: Schrift und Mauszeiger

Schriften und Mauszeiger von Querencia Desktop in der Optik von Ubuntu 10.04
(GNOME 2). Bis 20.10.2026 ein eigenes Arbeitsrepo (`querencia-erscheinungsbild`,
Stand 0.1); die Vorgaben und die Doku gehören jetzt zum Thema. Schrift- und
Zeigerdateien liefert Querencia nicht mit, sie kommen aus Ubuntu-Paketen.

## Gewählte Werte (Variante A)

| Was | Wert | Wo gesetzt |
|---|---|---|
| Oberfläche (`org.gnome.desktop.interface font-name`) | DejaVu Sans 10 | gsettings |
| Dokumente (`document-font-name`) | DejaVu Sans 10 | gsettings |
| Festbreite (`monospace-font-name`) | DejaVu Sans Mono 10 | gsettings |
| Zeiger (`cursor-theme`, `cursor-size`) | DMZ-White, 24 | gsettings |
| Fenstertitel, Menü, Fensterwechsler | DejaVu Sans 10, Titel und Menüüberschrift fett | labwc `rc.xml` ([labwc/rc.xml-theme-fonts.xml](labwc/rc.xml-theme-fonts.xml)) |
| Zeiger des Compositors | `XCURSOR_THEME=DMZ-White`, `XCURSOR_SIZE=24` | labwc `environment` ([labwc/querencia-erscheinungsbild.env](labwc/querencia-erscheinungsbild.env)) |

Die labwc-Werte kommen als Querencia-Standard aus der labwc-Vorgabe im Repo
`querencia-shell`; der Sitzungsstarter übernimmt sie in die Benutzerkopie
`~/.config/querencia/labwc/`. Variante B (Ubuntu-Schrift) und die Gründe der
Wahl: [entscheidungsvorlage-schrift-zeiger.md](entscheidungsvorlage-schrift-zeiger.md).
Einrichtung, verworfene Fassung 0.2 und Proben: [einrichtung.md](einrichtung.md).

## Pakete (Ubuntu 26.04)

```bash
sudo apt install fonts-dejavu-core fonts-dejavu-extra dmz-cursor-theme
```

Lizenzen der Pakete (nicht mitgeliefert): DejaVu Bitstream-Vera-Lizenz bzw.
gemeinfrei, DMZ CC-BY-SA-3.0, Ubuntu-Schrift Ubuntu Font Licence 1.0.
