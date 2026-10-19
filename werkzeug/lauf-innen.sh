#!/bin/bash
# Läuft IN der isolierten labwc-Sitzung (isoliert.py, aufgerufen von
# belege.sh): Programm starten, Bildschirmfoto, Menü per F10 öffnen,
# Bildschirmfoto, beenden.
set -u
. "$HMP04_PROFILE/env.sh"
# Eine dauerhafte qeingabe-Sitzung (wie eingabe.sh in querencia-rechner).
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
q "size $W $H" "move $((W - 5)) $((H - 5))" "wait 300"
"${BIN[@]}" >"$HMP04_PROFILE/logs/programm.log" 2>&1 &
PID=$!
sleep 5
if [ -n "${ZEIGER:-}" ]; then
    set -- $ZEIGER
    q "move $1 $2" "wait 200" "move $(($1 + 2)) $2" "wait 1500"
    [ "${KLICK:-0}" = 1 ] && q "click" "wait 1200" "move $(($1 + 40)) $(($2 + 40))" "wait 800"
fi
grim "$OUT/$NAME-1.png"
if [ "${MENUE:-1}" = 1 ] && kill -0 "$PID" 2>/dev/null; then
    q "key F10" "wait 900"
    grim "$OUT/$NAME-2-menue.png"
    q "key Escape" "wait 300" "key Escape" "wait 300"
fi
kill "$PID" 2>/dev/null
sleep 0.5
touch "$HMP04_PROFILE/logs/FERTIG"
