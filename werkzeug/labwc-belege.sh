#!/bin/bash
# Thema 0.2.2: Belegbilder der labwc-Themen Querencia-Klassisch und
# Querencia-Klassisch-Dunkel, isoliert (eigener labwc ohne Bildschirm mit
# eigenem Konfigordner, eigenes HOME, eigener Bus mit Settings-Portal,
# gsettings als Schlüsseldatei im Profil). Beide Themen liegen wie live unter
# $XDG_DATA_HOME/themes/<Name>/labwc. Zwei GTK-4-Fenster (vorn aktiv, hinten
# inaktiv), je Schritt ein Foto und ein Foto mit offenem Fenstermenü
# (Alt+Leertaste, labwc-Standardbelegung):
#   1-hell     Theme Querencia-Klassisch, color-scheme default
#   2-dunkel   Theme Querencia-Klassisch-Dunkel, color-scheme prefer-dark
#   3-zurueck  wie 1
# Jeder Wechsel des Theme-Namens in rc.xml über labwc --reconfigure (SIGHUP an
# den isolierten labwc), wie es Einstellungen 0.1.6 live tun soll.
#   bash werkzeug/labwc-belege.sh [ergebnisordner] [BxH …]
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
AUS=${1:-$E/gui-test/labwc-belege/ergebnis}
shift || true
GROESSEN=${*:-1024x768 1920x1080}
WB=${QTH_WERKZEUG_BIN:-$HOME/projects/querencia-rechner/werkzeug/bin}
LABWC=${QUERENCIA_LABWC:-$HOME/opt/labwc-0.9.8/bin/labwc}
mkdir -p "$AUS"
: >"$AUS/ergebnis.txt"
for G in $GROESSEN; do
B=${G%x*}; H=${G#*x}
P=$E/gui-test/labwc-belege-$G
A=$AUS/$G
rm -rf "$P"
mkdir -p "$P/data/themes/Querencia-Klassisch" "$P/data/themes/Querencia-Klassisch-Dunkel" \
    "$P/config/labwc" "$P/logs" "$A"
ln -s "$E/Querencia-Klassisch/gtk-4.0" "$P/data/themes/Querencia-Klassisch/gtk-4.0"
ln -s "$E/labwc/Querencia-Klassisch" "$P/data/themes/Querencia-Klassisch/labwc"
ln -s "$E/labwc/Querencia-Klassisch-Dunkel" "$P/data/themes/Querencia-Klassisch-Dunkel/labwc"
cat >"$P/config/labwc/rc.xml" <<R
<?xml version="1.0"?>
<labwc_config>
  <core><decoration>server</decoration></core>
  <placement><policy>cascade</policy></placement>
  <theme>
    <name>Querencia-Klassisch</name>
    <font place="ActiveWindow"><name>DejaVu Sans</name><size>10</size><weight>bold</weight></font>
    <font place="InactiveWindow"><name>DejaVu Sans</name><size>10</size><weight>bold</weight></font>
  </theme>
</labwc_config>
R
cat >"$P/innen.sh" <<I
set -u
L=\$HMP04_PROFILE/logs/ergebnis.txt
C=\$HMP04_PROFILE/config/labwc
# Nur der eigene labwc: LABWC_PID muss in diesem Lauf liegen
[ -n "\${LABWC_PID:-}" ] && grep -qz "^XDG_RUNTIME_DIR=\$XDG_RUNTIME_DIR\$" /proc/\$LABWC_PID/environ \
    || { echo "LABWC_PID nicht isoliert" >>\$L; touch \$HMP04_PROFILE/logs/FERTIG; exit 1; }
coproc QE { $WB/qeingabe; }
q() {
    local c line
    for c in "\$@"; do printf '%s\n' "\$c" >&"\${QE[1]}"; done
    printf 'mark SYNC\n' >&"\${QE[1]}"
    while IFS= read -r -t 30 line <&"\${QE[0]}"; do [[ \$line == *SYNC* ]] && return 0; done
    return 1
}
neu_laden() { "$LABWC" --reconfigure; q "wait 1500"; }
foto() {
    q "move $((B - 5)) $((H - 5))" "wait 600"
    grim "$A/\$1.png"
    q "chord alt space" "wait 700"
    grim "$A/\$1-menue.png"
    q "key Escape" "wait 500"
    echo "$G \$1: Theme \$(sed -n 's#^    <name>\(.*\)</name>#\1#p' \$C/rc.xml), color-scheme \$(gsettings get org.gnome.desktop.interface color-scheme)" >>\$L
}
$WB/qausgabe $G >/dev/null 2>&1
q "size $B $H"
gsettings set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
gsettings set org.gnome.desktop.interface color-scheme default
python3 -I $E/werkzeug/labwc-fenster.py "Hinteres Fenster (inaktiv)" >>\$L 2>&1 &
q "wait 2500"
python3 -I $E/werkzeug/labwc-fenster.py "Vorderes Fenster (aktiv)" >>\$L 2>&1 &
q "wait 3000"
foto 1-hell
sed -i 's#^    <name>Querencia-Klassisch</name>#    <name>Querencia-Klassisch-Dunkel</name>#' \$C/rc.xml
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
q "wait 1500"; neu_laden
foto 2-dunkel
sed -i 's#^    <name>Querencia-Klassisch-Dunkel</name>#    <name>Querencia-Klassisch</name>#' \$C/rc.xml
gsettings set org.gnome.desktop.interface color-scheme default
q "wait 1500"; neu_laden
foto 3-zurueck
touch \$HMP04_PROFILE/logs/FERTIG
I
QTH_PORTALE=1 QTH_EIGENES_HOME=1 python3 -I "$E/werkzeug/isoliert.py" "$P" "$P/innen.sh" 150
grep -E "^$G " "$P/logs/ergebnis.txt" >>"$AUS/ergebnis.txt" || true
for b in "" -menue; do
    if python3 -I "$E/werkzeug/bildvergleich.py" "$A/1-hell$b.png" "$A/3-zurueck$b.png" >/dev/null; then
        echo "$G 1-hell$b = 3-zurueck$b: pixelgleich" >>"$AUS/ergebnis.txt"
    else
        echo "$G 1-hell$b = 3-zurueck$b: VERSCHIEDEN" >>"$AUS/ergebnis.txt"
    fi
done
done
cat "$AUS/ergebnis.txt"
