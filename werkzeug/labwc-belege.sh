#!/bin/bash
# Thema 0.2.2: Belegbilder der labwc-Titelleisten, isoliert (eigener labwc
# ohne Bildschirm mit eigenem Konfigordner, eigenes HOME, eigener Bus mit
# Settings-Portal, gsettings als Schlüsseldatei im Profil). Zwei GTK-4-Fenster
# (vorn aktiv, hinten inaktiv), je Schritt ein Foto und ein Foto mit offenem
# Fenstermenü (Rechtsklick auf die Titelleiste):
#   1-hell       Theme Querencia-Klassisch, color-scheme default
#   2-override   + themerc-override-dunkel, color-scheme prefer-dark
#   3-dunkel     Theme Querencia-Klassisch-Dunkel, kein override, prefer-dark
#   4-zurueck    wie 1 (override entfernt, Theme hell, default)
# Jeder Wechsel über labwc --reconfigure (SIGHUP an den isolierten labwc).
#   bash werkzeug/labwc-belege.sh [ergebnisordner]
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
P=$E/gui-test/labwc-belege
AUS=${1:-$P/ergebnis}
WB=${QTH_WERKZEUG_BIN:-$HOME/projects/querencia-rechner/werkzeug/bin}
LABWC=${QUERENCIA_LABWC:-$HOME/opt/labwc-0.9.8/bin/labwc}
rm -rf "$P"
mkdir -p "$P/data/themes/Querencia-Klassisch" "$P/data/themes/Querencia-Klassisch-Dunkel" \
    "$P/config/labwc" "$P/logs" "$AUS"
ln -s "$E/Querencia-Klassisch/gtk-4.0" "$P/data/themes/Querencia-Klassisch/gtk-4.0"
ln -s "$E/labwc/Querencia-Klassisch" "$P/data/themes/Querencia-Klassisch/labwc"
ln -s "$E/labwc/Querencia-Klassisch-Dunkel" "$P/data/themes/Querencia-Klassisch-Dunkel/labwc"
rc() {   # Theme-Name
    cat >"$P/config/labwc/rc.xml" <<R
<?xml version="1.0"?>
<labwc_config>
  <core><decoration>server</decoration></core>
  <placement><policy>cascade</policy></placement>
  <theme>
    <name>$1</name>
    <font place="ActiveWindow"><name>DejaVu Sans</name><size>10</size><weight>bold</weight></font>
    <font place="InactiveWindow"><name>DejaVu Sans</name><size>10</size><weight>bold</weight></font>
  </theme>
</labwc_config>
R
}
rc Querencia-Klassisch
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
    q "move 1019 763" "wait 600"
    grim "$AUS/\$1.png"
    # Fenstermenü: Rechtsklick auf die Titelleiste des vorderen Fensters
    q "move \$MX \$MY" "rclick" "wait 700"
    grim "$AUS/\$1-menue.png"
    q "key Escape" "wait 400" "move 1019 763" "wait 400"
    echo "\$1: Theme \$(sed -n 's#.*<name>\(.*\)</name>.*#\1#p' \$C/rc.xml | head -1), override \$([ -e \$C/themerc-override ] && echo ja || echo nein), color-scheme \$(gsettings get org.gnome.desktop.interface color-scheme)" >>\$L
}
$WB/qausgabe 1024x768 >/dev/null 2>&1
q "size 1024 768"
gsettings set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
gsettings set org.gnome.desktop.interface color-scheme default
python3 -I $E/werkzeug/labwc-fenster.py "Hinteres Fenster (inaktiv)" >>\$L 2>&1 &
q "wait 2500"
python3 -I $E/werkzeug/labwc-fenster.py "Vorderes Fenster (aktiv)" >>\$L 2>&1 &
q "wait 3000"
# Titelleiste des vorderen Fensters: Kaskade versetzt um die Titelhöhe; die
# Lage steht im Foto 1-hell, der Klickpunkt liegt in der Titelmitte.
MX=\${QTH_MENUE_X:-560}; MY=\${QTH_MENUE_Y:-290}
foto 1-hell
cp "$E/labwc/themerc-override-dunkel" \$C/themerc-override
gsettings set org.gnome.desktop.interface color-scheme prefer-dark
q "wait 1500"; neu_laden
foto 2-override
rm -f \$C/themerc-override
sed -i 's#<name>Querencia-Klassisch</name>#<name>Querencia-Klassisch-Dunkel</name>#' \$C/rc.xml
neu_laden
foto 3-dunkel
sed -i 's#<name>Querencia-Klassisch-Dunkel</name>#<name>Querencia-Klassisch</name>#' \$C/rc.xml
gsettings set org.gnome.desktop.interface color-scheme default
q "wait 1500"; neu_laden
foto 4-zurueck
touch \$HMP04_PROFILE/logs/FERTIG
I
QTH_PORTALE=1 QTH_EIGENES_HOME=1 python3 -I "$E/werkzeug/isoliert.py" "$P" "$P/innen.sh" 150
cp "$P/logs/ergebnis.txt" "$AUS/ergebnis.txt"
for b in "" -menue; do
    if python3 -I "$E/werkzeug/bildvergleich.py" "$AUS/1-hell$b.png" "$AUS/4-zurueck$b.png" >/dev/null; then
        echo "1-hell$b = 4-zurueck$b: pixelgleich" >>"$AUS/ergebnis.txt"
    else
        echo "1-hell$b = 4-zurueck$b: VERSCHIEDEN" >>"$AUS/ergebnis.txt"
    fi
done
cat "$AUS/ergebnis.txt"
