#!/bin/bash
# Thema 0.2.2, QD-088 (5): Fokus nach einem Farbschema-Wechsel im Lauf
# (Befund Systemmonitor 0.1.3: Fokusrahmen am Reiter erst nach dem Wechsel).
# Ergänzt fokus-probe.sh (0.2.1) um den Fall „erst eine Taste, dann der
# Wechsel“. Isoliert wie fokus-probe.sh; je Thema (Querencia-Klassisch aus dem
# Repo, GTK-eigenes „Default“ über gtk-theme Adwaita):
#   1-start             gestartet, keine Eingabe
#   2-nach-tab          Tab (Tastatur, wie Strg+F im Systemmonitor-Szenario)
#   3-dunkel            gleich danach color-scheme prefer-dark
#   4-zurueck           color-scheme default
#   5-gewartet          6 s ohne Eingabe
#   6-dunkel-gewartet   color-scheme prefer-dark
#   7-zurueck-gewartet  color-scheme default
# Meldet je Schritt Fokus-Widget, Window:focus-visible und die Zustände des
# Fokus-Widgets (werkzeug/fokus-probe.py), dazu ein Foto.
#   bash werkzeug/fokus-probe-022.sh [ergebnisordner]
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
P=$E/gui-test/fokus-probe-022
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
# Meldung der Probe kommt jede Sekunde: 1,2 s warten, dann Marke und Foto
schritt() { q "wait 1200"; echo "== \$T \$1" >>\$L; grim "$AUS/\$T-\$1.png"; }
cs() { gsettings set org.gnome.desktop.interface color-scheme \$1; }
for T in Querencia-Klassisch Adwaita; do
    gsettings set org.gnome.desktop.interface gtk-theme \$T
    cs default
    python3 -I $E/werkzeug/fokus-probe.py \$T >>\$L 2>&1 &
    PID=\$!
    q "wait 2500"; schritt 1-start
    q "key Tab"; schritt 2-nach-tab
    cs prefer-dark; schritt 3-dunkel
    cs default; schritt 4-zurueck
    q "wait 6000"; schritt 5-gewartet
    cs prefer-dark; schritt 6-dunkel-gewartet
    cs default; schritt 7-zurueck-gewartet
    kill \$PID; wait \$PID 2>/dev/null
done
touch \$HMP04_PROFILE/logs/FERTIG
I
QTH_PORTALE=1 QTH_EIGENES_HOME=1 python3 -I "$E/werkzeug/isoliert.py" "$P" "$P/innen.sh" 150
awk '/^==/{print prev; print} !/^==/{prev=$0}' "$P/logs/ergebnis.txt" | grep -v '^$' >"$AUS/ergebnis.txt"
vergleich() {   # a b
    if python3 -I "$E/werkzeug/bildvergleich.py" "$AUS/$1.png" "$AUS/$2.png" >/dev/null; then
        echo "$1 = $2: pixelgleich"
    else
        echo "$1 = $2: verschieden"
    fi >>"$AUS/ergebnis.txt"
}
for T in Querencia-Klassisch Adwaita; do
    vergleich "$T-2-nach-tab" "$T-4-zurueck"
    vergleich "$T-1-start" "$T-7-zurueck-gewartet"
    vergleich "$T-5-gewartet" "$T-7-zurueck-gewartet"
done
cat "$AUS/ergebnis.txt"
