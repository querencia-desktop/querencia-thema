#!/bin/bash
# Läuft IN der isolierten Sitzung mit Portal (QTH_PORTALE=1, gsettings als
# Schlüsseldatei im Profil): Musterseite starten, dann gtk-theme und
# overlay-scrolling umstellen wie „aktivieren“ und wieder zurück; nach
# jedem Schritt ein Bildschirmfoto. Zeigt, ob laufende Programme die
# Änderung sofort übernehmen.
set -u
. "$HMP04_PROFILE/env.sh"
W=${R%x*}; H=${R#*x}
"$QA" "$R" >/dev/null 2>&1
LOG=$OUT/$NAME-ablauf.txt
: >"$LOG"
gs() { gsettings "$@" >>"$LOG" 2>&1; }
echo "GSETTINGS_BACKEND=$GSETTINGS_BACKEND XDG_CONFIG_HOME=$XDG_CONFIG_HOME" >>"$LOG"
gs set org.gnome.desktop.interface gtk-theme Adwaita
gs set org.gnome.desktop.interface overlay-scrolling true
"${BIN[@]}" >"$HMP04_PROFILE/logs/programm.log" 2>&1 &
PID=$!
sleep 6
grim "$OUT/$NAME-1-adwaita.png"
gs set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
gs set org.gnome.desktop.interface overlay-scrolling false
sleep 3
echo "nach set: $(gsettings get org.gnome.desktop.interface gtk-theme) $(gsettings get org.gnome.desktop.interface overlay-scrolling)" >>"$LOG"
grim "$OUT/$NAME-2-gesetzt-laufend.png"
"${BIN[@]}" >>"$HMP04_PROFILE/logs/programm.log" 2>&1 &
PID2=$!
sleep 5
grim "$OUT/$NAME-3-neu-gestartet.png"
kill "$PID2" 2>/dev/null
gs set org.gnome.desktop.interface gtk-theme Adwaita
gs set org.gnome.desktop.interface overlay-scrolling true
sleep 3
grim "$OUT/$NAME-4-zurueck-laufend.png"
kill "$PID" 2>/dev/null
sleep 0.5
touch "$HMP04_PROFILE/logs/FERTIG"
