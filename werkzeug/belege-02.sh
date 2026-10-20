#!/bin/bash
# Thema 0.2: Belegbilder hell/dunkel (Farbschema über das Settings-Portal)
# und Regression der hellen Fassung gegen die Live-Ablage, alles isoliert
# (belege.sh). Ziel:  (oder $1). Dauer ca. 12 min.
set -u
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
B=$E/werkzeug/belege.sh
Z=${1:-$HOME/review/thema-02-bilder}
LIVE=${QTH_LIVE_THEMA:-$(readlink -f "$HOME/.local/share/themes/Querencia-Klassisch")}
mkdir -p "$Z/regression/neu" "$Z/regression/live"
for r in 1024x768 1920x1080; do
    for f in einstellungen files editor panel-menue; do bash "$B" $f $r farbschema "$Z" >/dev/null 2>&1; done
done
for f in muster-knoepfe muster-listen muster-text muster-regler muster3 rechner systemmonitor software dateisuche bilder desktop; do
    bash "$B" $f 1024x768 farbschema "$Z" >/dev/null 2>&1
done
# Regression hell: dieselben Fälle mit dem Repo-Thema und mit der Live-Ablage
for f in muster-knoepfe muster-listen muster-text muster-regler muster3 einstellungen editor rechner systemmonitor; do
    bash "$B" $f 1024x768 nachher "$Z/regression/neu" >/dev/null 2>&1
    QTH_THEMA_QUELLE=$LIVE bash "$B" $f 1024x768 nachher "$Z/regression/live" >/dev/null 2>&1
done
(cd "$Z/regression/neu" && for b in *.png; do
    printf '%-50s ' "$b"; python3 -I "$E/werkzeug/bildvergleich.py" "$b" "../live/$b"
done) >"$Z/regression/vergleich.txt"
ls "$Z"/*.png | wc -l
findmnt -rn -o TARGET | grep "$E/laufzeit" || echo "keine Mounts aus dem Testlauf"
