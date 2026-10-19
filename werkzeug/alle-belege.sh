#!/bin/bash
# Alle Belegbilder neu (isoliert), Ergebnis nachweis/bilder/. Dauer ca. 12 min.
set -u
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
B=$E/werkzeug/belege.sh
rm -rf "$E/nachweis/bilder"
for r in 1024x768 1920x1080; do
    for a in einstellungen files rechner editor systemmonitor dateisuche software bilder panel desktop muster3 muster-knoepfe muster-listen; do
        for t in vorher nachher; do bash "$B" $a $r $t >/dev/null 2>&1; done
    done
    for f in muster-regler muster-text muster-dialog muster-popover muster-tooltip muster3-liste panel-menue; do
        bash "$B" $f $r nachher >/dev/null 2>&1
    done
done
for f in muster-regler muster-text muster-dialog muster-popover muster-tooltip muster3-liste panel-menue muster-klein; do
    bash "$B" $f 1024x768 vorher >/dev/null 2>&1
done
bash "$B" muster-klein 1024x768 nachher >/dev/null 2>&1
for t in dunkel weiss; do for f in muster-knoepfe muster-listen files; do bash "$B" $f 1024x768 $t >/dev/null 2>&1; done; done
bash "$B" portal 1024x768 nachher >/dev/null 2>&1
bash "$B" portal-panel 1024x768 nachher >/dev/null 2>&1
ls "$E/nachweis/bilder" | wc -l
findmnt -rn -o TARGET | grep "$E/laufzeit" || echo "keine Mounts aus dem Testlauf"
