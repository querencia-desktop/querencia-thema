#!/bin/bash
# Thema 0.2.2: GTK-3-Dunkelfassung für fremde Programme (QD-103), isoliert
# (eigener labwc ohne Bildschirm, eigenes HOME, eigener Bus mit
# Settings-Portal, gsettings als Schlüsseldatei im Profil). Prüfling:
# gtk-builder-tool preview (GTK 3.24) mit werkzeug/gtk3-muster.ui. Fälle:
#   1-hell          gtk-theme Querencia-Klassisch, color-scheme default
#   2-nur-schema    color-scheme prefer-dark, keine settings.ini (QD-103)
#   3-settings-ini  ~/.config/gtk-3.0/settings.ini
#                   gtk-application-prefer-dark-theme=true (Vorschlag QD-103)
#   4-gtk-theme     GTK_THEME=Querencia-Klassisch:dark (Vergleich)
#   5-im-lauf       hell gestartet, dann settings.ini geschrieben und
#                   color-scheme prefer-dark, ohne Neustart
# Je Fall ein Foto, dazu offenes Datei-Menü (F10).
#   bash werkzeug/gtk3-belege.sh [ergebnisordner]
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
P=$E/gui-test/gtk3-belege
AUS=${1:-$P/ergebnis}
WB=${QTH_WERKZEUG_BIN:-$HOME/projects/querencia-rechner/werkzeug/bin}
rm -rf "$P"
mkdir -p "$P/data/themes/Querencia-Klassisch" "$P/config/labwc" "$P/logs" "$AUS"
ln -s "$E/Querencia-Klassisch/gtk-3.0" "$P/data/themes/Querencia-Klassisch/gtk-3.0"
ln -s "$E/Querencia-Klassisch/gtk-4.0" "$P/data/themes/Querencia-Klassisch/gtk-4.0"
cat >"$P/innen.sh" <<I
set -u
L=\$HMP04_PROFILE/logs/ergebnis.txt
INI=\$HMP04_PROFILE/config/gtk-3.0/settings.ini
coproc QE { $WB/qeingabe; }
q() {
    local c line
    for c in "\$@"; do printf '%s\n' "\$c" >&"\${QE[1]}"; done
    printf 'mark SYNC\n' >&"\${QE[1]}"
    while IFS= read -r -t 30 line <&"\${QE[0]}"; do [[ \$line == *SYNC* ]] && return 0; done
    return 1
}
$WB/qausgabe 1024x768 >/dev/null 2>&1
q "size 1024 768"
gsettings set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
start() { gtk-builder-tool preview --id=fenster $E/werkzeug/gtk3-muster.ui >>\$L 2>&1 & PID=\$!; q "wait 3000"; }
ende() { kill \$PID; wait \$PID 2>/dev/null; q "wait 500"; }
foto() {
    q "move 1019 763" "wait 500"
    grim "$AUS/\$1.png"
    q "key F10" "wait 800"
    grim "$AUS/\$1-menue.png"
    q "key Escape" "wait 300" "key Escape" "wait 300"
    echo "\$1: color-scheme \$(gsettings get org.gnome.desktop.interface color-scheme), settings.ini \$([ -e \$INI ] && tr '\n' ' ' <\$INI || echo -), GTK_THEME \${GTK_THEME:--}" >>\$L
}
gsettings set org.gnome.desktop.interface color-scheme default
start; foto 1-hell; ende
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
start; foto 2-nur-schema; ende
mkdir -p \$(dirname \$INI)
printf '[Settings]\ngtk-application-prefer-dark-theme=true\n' >\$INI
start; foto 3-settings-ini; ende
rm -f \$INI
GTK_THEME=Querencia-Klassisch:dark start; GTK_THEME=Querencia-Klassisch:dark foto 4-gtk-theme; ende
gsettings set org.gnome.desktop.interface color-scheme default
start
printf '[Settings]\ngtk-application-prefer-dark-theme=true\n' >\$INI
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
q "wait 3000"; foto 5-im-lauf; ende
rm -f \$INI
touch \$HMP04_PROFILE/logs/FERTIG
I
QTH_PORTALE=1 QTH_EIGENES_HOME=1 python3 -I "$E/werkzeug/isoliert.py" "$P" "$P/innen.sh" 150
grep -E '^[0-9]-' "$P/logs/ergebnis.txt" >"$AUS/ergebnis.txt" || true
vergleich() {   # a b
    if python3 -I "$E/werkzeug/bildvergleich.py" "$AUS/$1.png" "$AUS/$2.png" >/dev/null; then
        echo "$1 = $2: pixelgleich"
    else
        echo "$1 = $2: verschieden"
    fi >>"$AUS/ergebnis.txt"
}
vergleich 1-hell 2-nur-schema
vergleich 3-settings-ini 4-gtk-theme
vergleich 3-settings-ini-menue 4-gtk-theme-menue
vergleich 1-hell 5-im-lauf
cat "$AUS/ergebnis.txt"
