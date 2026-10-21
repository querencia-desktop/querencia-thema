#!/bin/bash
# Thema 0.2.1: Probe der benannten Farben (@sidebar_bg_color, @sidebar_fg_color,
# @menu_bg_color, @menu_fg_color) mit dem Repo-Thema, isoliert (eigenes HOME,
# eigener Bus mit Settings-Portal, gsettings als Schlüsseldatei). Die Farben
# werden aus einem Programm-Provider ohne Bindung aufgelöst. Ein Programm
# läuft beim Umschalten auf prefer-dark, zwei starten danach neu (ohne und mit
# Settings.notify). Erwartet: hell #f5f4f2 #3c3c3c #f5f4f2 #3c3c3c; laufend und
# „mit notify“ dunkel #353430 #e8e6e3 #353430 #dfdbd2; „ohne“ hell
# (GTK-4.22-Startfehler, docs/aufbau.md).
#   bash werkzeug/farbnamen-probe.sh [ergebnisdatei]
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
P=$E/gui-test/farbnamen-probe
AUS=${1:-$P/ergebnis.txt}
rm -rf "$P"
mkdir -p "$P/data/themes/Querencia-Klassisch" "$P/config" "$P/logs"
ln -s "$E/Querencia-Klassisch/gtk-4.0" "$P/data/themes/Querencia-Klassisch/gtk-4.0"
cat >"$P/innen.sh" <<I
set -u
L=\$HMP04_PROFILE/logs/ergebnis.txt
gsettings set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
gsettings set org.gnome.desktop.interface color-scheme default
python3 -I $E/werkzeug/farbnamen-probe.py laufend >>\$L 2>&1 &
sleep 4
echo "== color-scheme prefer-dark" >>\$L
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
sleep 3
python3 -I $E/werkzeug/farbnamen-probe.py neustart-ohne >>\$L 2>&1 &
python3 -I $E/werkzeug/farbnamen-probe.py neustart-mit-notify notify >>\$L 2>&1 &
sleep 4
echo "== color-scheme default" >>\$L
gsettings set org.gnome.desktop.interface color-scheme default
sleep 3
kill %1 %2 %3 2>/dev/null
touch \$HMP04_PROFILE/logs/FERTIG
I
QTH_PORTALE=1 QTH_EIGENES_HOME=1 python3 -I "$E/werkzeug/isoliert.py" "$P" "$P/innen.sh" 60
grep -E '^(==|laufend|neustart)' "$P/logs/ergebnis.txt" | uniq >"$AUS"
cat "$AUS"
