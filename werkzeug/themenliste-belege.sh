#!/bin/bash
# Thema 0.2.2: Taucht das labwc-Theme Querencia-Klassisch-Dunkel (nur labwc/,
# kein gtk-4.0/gtk-3.0) in GTK-Themenlisten auf? Isoliert (eigener labwc,
# eigenes HOME, eigener Bus mit Settings-Portal, gsettings als
# Schlüsseldatei). Beide Themen liegen wie live in $XDG_DATA_HOME/themes.
#   1-einstellungen-erscheinungsbild  Einstellungen aus der Ablage (nur
#                                     ausgeführt), Seite „erscheinungsbild“:
#                                     Auswahl GTK-Thema
#   2-einstellungen-fensterdesign     Seite „fensterdesign“: labwc-Themen
#                                     (dort soll es erscheinen)
#   3-inspector-*                     GTK-Inspector (GTK_DEBUG=interactive)
#                                     eines GTK-4-Fensters, Global →
#                                     Einstellungen, Auswahl GTK-Thema geöffnet
# Klickpunkte im Inspector: QTH_INSPECTOR_REITER („x y;x y“, nacheinander),
# QTH_INSPECTOR_THEMA (x y, öffnet die Auswahl); Vorgaben in 1024×768 gemessen.
#   bash werkzeug/themenliste-belege.sh [ergebnisordner]
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
P=$E/gui-test/themenliste
AUS=${1:-$P/ergebnis}
WB=${QTH_WERKZEUG_BIN:-$HOME/projects/querencia-rechner/werkzeug/bin}
EINST=${QTH_EINSTELLUNGEN:-$(readlink -f "$HOME/opt/querencia/bin/querencia-einstellungen")}
REITER=${QTH_INSPECTOR_REITER-449 152;175 219}
THEMA=${QTH_INSPECTOR_THEMA-723 253}
rm -rf "$P"
mkdir -p "$P/data/themes/Querencia-Klassisch" "$P/data/themes/Querencia-Klassisch-Dunkel" \
    "$P/config/labwc" "$P/logs" "$AUS"
for t in gtk-4.0 gtk-3.0; do ln -s "$E/Querencia-Klassisch/$t" "$P/data/themes/Querencia-Klassisch/$t"; done
ln -s "$E/labwc/Querencia-Klassisch" "$P/data/themes/Querencia-Klassisch/labwc"
ln -s "$E/labwc/Querencia-Klassisch-Dunkel" "$P/data/themes/Querencia-Klassisch-Dunkel/labwc"
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
q "size 1024 768"
gsettings set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
gsettings set org.gnome.desktop.interface color-scheme default
echo "Themenordner: \$(ls \$XDG_DATA_HOME/themes | tr '\n' ' ')" >>\$L
for s in erscheinungsbild fensterdesign; do
    $EINST --seite \$s >>\$L 2>&1 & PID=\$!
    q "wait 4000" "move 1019 763" "wait 300"
    [ \$s = erscheinungsbild ] && n=1 || n=2
    grim "$AUS/\$n-einstellungen-\$s.png"
    kill \$PID; wait \$PID 2>/dev/null; q "wait 800"
done
GTK_DEBUG=interactive python3 -I $E/werkzeug/labwc-fenster.py "Inspector-Probe" >>\$L 2>&1 & PID=\$!
q "wait 4000"
grim "$AUS/3-inspector-1-start.png"
if [ -n "$REITER" ]; then
    IFS=';' read -ra PUNKTE <<<"$REITER"
    for pk in "\${PUNKTE[@]}"; do q "move \$pk" "click" "wait 1500"; done
    grim "$AUS/3-inspector-2-einstellungen.png"
fi
if [ -n "$THEMA" ]; then
    q "move $THEMA" "click" "wait 1200"
    grim "$AUS/3-inspector-3-themenliste.png"
    q "key Escape" "wait 300"
fi
kill \$PID; wait \$PID 2>/dev/null
touch \$HMP04_PROFILE/logs/FERTIG
I
QTH_PORTALE=1 QTH_EIGENES_HOME=1 python3 -I "$E/werkzeug/isoliert.py" "$P" "$P/innen.sh" 120
cp "$P/logs/ergebnis.txt" "$AUS/lauf.log"
ls "$AUS"
