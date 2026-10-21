#!/bin/bash
# Thema 0.2.1: Fokus nach einem Farbschema-Wechsel (Notiz Systemmonitor
# 0.1.3), isoliert (eigenes HOME, eigener Bus mit Settings-Portal, gsettings
# als Schlüsseldatei). Je Thema (Querencia-Klassisch aus dem Repo, GTK-eigenes
# „Default“ über gtk-theme Adwaita): Start, dunkel und zurück ohne Taste,
# dann F10/Esc wie lauf-farbschema.sh, dunkel und zurück. Meldet Fokus und
# focus-visible je Schritt, Bildschirmfotos je Schritt.
#   bash werkzeug/fokus-probe.sh [ergebnisordner]
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
P=$E/gui-test/fokus-probe
AUS=${1:-$P/ergebnis}
WB=${QTH_WERKZEUG_BIN:-$HOME/projects/querencia-rechner/werkzeug/bin}
rm -rf "$P"
mkdir -p "$P/data/themes/Querencia-Klassisch" "$P/config" "$P/logs" "$AUS"
ln -s "$E/Querencia-Klassisch/gtk-4.0" "$P/data/themes/Querencia-Klassisch/gtk-4.0"
cat >"$P/innen.sh" <<I
set -u
L=\$HMP04_PROFILE/logs/ergebnis.txt
coproc QE { $WB/qeingabe; }
q() {
    local c line
    for c in "\$@"; do printf '%s\n' "\$c" >&"\${QE[1]}"; done
    printf 'mark SYNC\n' >&"\${QE[1]}"
    while IFS= read -r -t 30 line <&"\${QE[0]}"; do [[ \$line == *SYNC* ]] && return 0; done
    return 1
}
$WB/qausgabe 1024x768 >/dev/null 2>&1
q "size 1024 768" "move 1019 763" "wait 300"
schritt() { q "wait 2500"; echo "== \$T \$1" >>\$L; q "wait 1200"; grim "$AUS/\$T-\$1.png"; }
cs() { gsettings set org.gnome.desktop.interface color-scheme \$1; }
for T in Querencia-Klassisch Adwaita; do
    gsettings set org.gnome.desktop.interface gtk-theme \$T
    cs default
    python3 -I $E/werkzeug/fokus-probe.py \$T >>\$L 2>&1 &
    PID=\$!
    schritt 1-start
    cs prefer-dark; schritt 2-dunkel-ohne-taste
    cs default; schritt 3-zurueck-ohne-taste
    q "key F10" "wait 900" "key Escape" "wait 300" "key Escape" "wait 300"
    schritt 4-nach-f10-esc
    q "wait 4000"; schritt 4b-nur-gewartet
    cs prefer-dark; schritt 5-dunkel
    cs default; schritt 6-zurueck
    kill \$PID; wait \$PID 2>/dev/null
done
touch \$HMP04_PROFILE/logs/FERTIG
I
QTH_PORTALE=1 QTH_EIGENES_HOME=1 python3 -I "$E/werkzeug/isoliert.py" "$P" "$P/innen.sh" 120
# je Schritt die letzte Meldung davor
awk '/^==/{print prev; print} !/^==/{prev=$0}' "$P/logs/ergebnis.txt" | grep -v '^$' >"$AUS/ergebnis.txt"
cat "$AUS/ergebnis.txt"
