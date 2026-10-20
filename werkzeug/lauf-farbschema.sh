#!/bin/bash
# Läuft IN der isolierten Sitzung mit Portal (QTH_PORTALE=1, gsettings als
# Schlüsseldatei im Profil; Thema 0.2): Programm hell starten (gtk-theme
# Querencia-Klassisch, color-scheme default), Bildschirmfoto, dann
# color-scheme prefer-dark wie Einstellungen → Erscheinungsbild →
# Farbschema, Bildschirmfoto, Menü (F10 oder Zeigerklick), Bildschirmfoto.
# Laufende Programme folgen über das Settings-Portal (docs/aufbau.md).
set -u
. "$HMP04_PROFILE/env.sh"
coproc QE { "$Q"; }
q() {
    local c line
    for c in "$@"; do printf '%s\n' "$c" >&"${QE[1]}"; done
    printf 'mark SYNC\n' >&"${QE[1]}"
    while IFS= read -r -t 30 line <&"${QE[0]}"; do [[ $line == *SYNC* ]] && return 0; done
    return 1
}
W=${R%x*}; H=${R#*x}
"$QA" "$R" >/dev/null 2>&1
LOG=$OUT/$NAME-ablauf.txt
: >"$LOG"
gs() { gsettings "$@" >>"$LOG" 2>&1; }
gs set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
gs set org.gnome.desktop.interface overlay-scrolling false
gs set org.gnome.desktop.interface color-scheme default
[ -n "${SCHRIFT:-}" ] && gs set org.gnome.desktop.interface font-name "$SCHRIFT"
q "size $W $H" "move $((W - 5)) $((H - 5))" "wait 300"
"${BIN[@]}" >"$HMP04_PROFILE/logs/programm.log" 2>&1 &
PID=$!
sleep 6
grim "$OUT/$NAME-1-hell.png"
gs set org.gnome.desktop.interface color-scheme prefer-dark
sleep 3
echo "color-scheme $(gsettings get org.gnome.desktop.interface color-scheme)," \
    "Portal $(gdbus call --session --dest org.freedesktop.portal.Desktop --object-path /org/freedesktop/portal/desktop \
    --method org.freedesktop.portal.Settings.ReadOne org.freedesktop.appearance color-scheme 2>&1)" >>"$LOG"
grim "$OUT/$NAME-2-dunkel.png"
if [ -n "${ZEIGER:-}" ]; then
    set -- $ZEIGER
    q "move $1 $2" "wait 200" "move $(($1 + 2)) $2" "wait 1500"
    [ "${KLICK:-0}" = 1 ] && q "click" "wait 1200" "move $(($1 + 40)) $(($2 + 40))" "wait 800"
    grim "$OUT/$NAME-3-dunkel-menue.png"
elif [ "${MENUE:-1}" = 1 ] && kill -0 "$PID" 2>/dev/null; then
    q "key F10" "wait 900"
    grim "$OUT/$NAME-3-dunkel-menue.png"
    q "key Escape" "wait 300" "key Escape" "wait 300"
fi
# Zurück auf hell: das laufende Programm muss wieder hell werden.
gs set org.gnome.desktop.interface color-scheme default
sleep 3
grim "$OUT/$NAME-4-wieder-hell.png"
kill "$PID" 2>/dev/null
sleep 0.5
touch "$HMP04_PROFILE/logs/FERTIG"
