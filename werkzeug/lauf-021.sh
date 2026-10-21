#!/bin/bash
# Thema 0.2.1: läuft IN der isolierten Sitzung mit Settings-Portal
# (regression-021.sh, isoliert.py mit QTH_PORTALE=1 QTH_EIGENES_HOME=1).
# gsettings nur in der Schlüsseldatei des Profils. Programm hell starten;
# bei SCHEMA=dunkel color-scheme prefer-dark im laufenden Programm (so
# unabhängig vom GTK-4.22-Startfehler); Bildschirmfoto; dann AKTION:
#   menue    F10 (erstes Menü der Menüleiste, mit Tastenkürzeln), Foto
#   kennwort Archiv: Entpacken (Strg+E) → Kennwortfenster, Foto; falsches
#            Kennwort → Fenster mit Fehlerzeile (label.error), Foto
#   -        nur das erste Foto
set -u
. "$HMP04_PROFILE/env.sh"
coproc QE { "$Q"; }
q() {
    local c line
    for c in "$@"; do printf '%s\n' "$c" >&"${QE[1]}"; done
    printf 'mark SYNC\n' >&"${QE[1]}"
    while IFS= read -r -t 60 line <&"${QE[0]}"; do [[ $line == *SYNC* ]] && return 0; done
    return 1
}
W=${R%x*}; H=${R#*x}
LOG=$OUT/$NAME-ablauf.txt
: >"$LOG"
gs() { gsettings "$@" >>"$LOG" 2>&1; }
gs set org.gnome.desktop.interface gtk-theme Querencia-Klassisch
gs set org.gnome.desktop.interface overlay-scrolling false
gs set org.gnome.desktop.interface color-scheme default
gs set org.gnome.desktop.interface cursor-blink false
[ -n "${SCHRIFT:-}" ] && gs set org.gnome.desktop.interface font-name "$SCHRIFT"
"$QA" "$R" >/dev/null 2>&1
q "size $W $H" "move $((W - 5)) $((H - 5))" "wait 300"
"${BIN[@]}" >"$HMP04_PROFILE/logs/programm.log" 2>&1 &
PID=$!
q "wait 6000"
if [ "$SCHEMA" = dunkel ]; then
    gs set org.gnome.desktop.interface color-scheme prefer-dark
    q "wait 3000"
fi
echo "LANG=$LANG LANGUAGE=${LANGUAGE:-} color-scheme $(gsettings get org.gnome.desktop.interface color-scheme)" >>"$LOG"
grim "$OUT/$NAME-1.png"
case $AKTION in
menue)
    q "key F10" "wait 1500"
    grim "$OUT/$NAME-2-menue.png"
    q "key Escape" "wait 300" "key Escape" "wait 300" ;;
kennwort)
    case $SPR in de) ALLE=d ;; *) ALLE=a ;; esac
    q "chord ctrl e" "wait 1500" "chord ctrl a" "type $ZIEL" "chord alt $ALLE" "key Return" "wait 3000"
    grim "$OUT/$NAME-2-kennwort.png"
    q "type falsch" "key Return" "wait 3000"
    grim "$OUT/$NAME-3-kennwort-falsch.png"
    q "key Escape" "wait 500" ;;
esac
kill "$PID" 2>/dev/null
q "wait 500"
touch "$HMP04_PROFILE/logs/FERTIG"
