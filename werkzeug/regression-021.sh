#!/bin/bash
# Thema 0.2.1: Regression isoliert gegen die Live-Ablage (gekürzte Matrix:
# de 1024x768 und en 1920x1080, hell und dunkel). Je Fall zwei Läufe mit
# derselben Eingabefolge: „neu“ = Repo-Thema, „live“ = GTK-Teile der
# Live-Ablage (nur gelesen). Rahmen (labwc) immer live. Danach Pixelvergleich
# neu gegen live je Bild.
#   bash werkzeug/regression-021.sh [ziel] [parallel]
# Ziel: $1 bzw. der Standardordner unten; parallel Standard 4 Läufe.
# Ein einzelner Lauf: regression-021.sh --lauf <fall> <spr> <BxH> <hell|dunkel> <neu|live> <ziel>
set -u
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
WB=${QTH_WERKZEUG_BIN:-$HOME/projects/querencia-rechner/werkzeug/bin}
OPT=$HOME/opt/querencia
LIVE=${QTH_LIVE_THEMA:-$(readlink -f "$HOME/.local/share/themes/Querencia-Klassisch")}
LIVE_LABWC=$LIVE/labwc
ZIP=${QTH_KENNWORT_ZIP:-$HOME/projects/querencia-archiv/gui-test/t/geschuetzt.zip}

lauf() {   # fall spr BxH schema quelle ziel
    local fall=$1 spr=$2 r=$3 schema=$4 quelle=$5 ziel=$6 aktion=menue tq
    local -a bin
    case $quelle in neu) tq=$E/Querencia-Klassisch ;; live) tq=$LIVE ;; *) return 2 ;; esac
    local name=$fall-$spr-$r-$schema-$quelle
    local p=$E/gui-test/r021-$name
    rm -rf "$p"
    mkdir -p "$p/config/labwc" "$p/data/themes/Querencia-Klassisch" "$p/daten" "$ziel"
    ln -s "$LIVE_LABWC" "$p/data/themes/Querencia-Klassisch/labwc"
    ln -s "$tq/gtk-4.0" "$p/data/themes/Querencia-Klassisch/gtk-4.0"
    ln -s "$tq/gtk-3.0" "$p/data/themes/Querencia-Klassisch/gtk-3.0"
    case $fall in
    archiv) cp "$ZIP" "$p/daten/geschuetzt.zip"; bin=("$OPT/bin/querencia-archiv" "$p/daten/geschuetzt.zip"); aktion=kennwort ;;
    dokumente) bin=("$OPT/bin/querencia-dokumente") ;;
    editor) cp "$E/README.md" "$p/daten/README.md"; bin=("$OPT/bin/querencia-editor" "$p/daten/README.md") ;;
    rechner) bin=("$OPT/bin/querencia-rechner") ;;
    einstellungen) bin=("$OPT/bin/querencia-einstellungen"); aktion=- ;;
    muster-knoepfe | muster-listen | muster-text) bin=(python3 -I "$E/werkzeug/muster4.py" "${fall#muster-}") ;;
    muster3) bin=(python3 -I "$E/werkzeug/muster3.py") ;;
    *) echo "unbekannter Fall $fall" >&2; return 2 ;;
    esac
    cat >"$p/config/labwc/rc.xml" <<X
<?xml version="1.0"?>
<labwc_config>
  <core><decoration>server</decoration></core>
  <theme><name>Querencia-Klassisch</name><icon>gnome-human</icon></theme>
  <windowRules>
    <windowRule identifier="*"><action name="MoveTo" x="16" y="12" /></windowRule>
  </windowRules>
</labwc_config>
X
    local schrift
    schrift=$(gsettings get org.gnome.desktop.interface font-name 2>/dev/null | tr -d "'")
    {
        printf 'BIN=('; printf '%q ' "${bin[@]}"; printf ')\n'
        printf 'Q=%q\nQA=%q\nOUT=%q\nR=%q\nNAME=%q\nSCHEMA=%q\nAKTION=%q\nSPR=%q\nSCHRIFT=%q\nZIEL=%q\n' \
            "$WB/qeingabe" "$WB/qausgabe" "$ziel" "$r" "$name" "$schema" "$aktion" "$spr" "$schrift" "$p/daten/aus"
    } >"$p/env.sh"
    local lang=en_US.UTF-8
    [ "$spr" = de ] && lang=de_DE.UTF-8
    env QTH_PORTALE=1 QTH_EIGENES_HOME=1 GSK_DEBUG=full-redraw LANG=$lang LANGUAGE=$spr \
        python3 -I "$E/werkzeug/isoliert.py" "$p" "$E/werkzeug/lauf-021.sh" 150 >"$ziel/$name-isoliert.txt" 2>&1
    ls "$ziel/$name"-*.png >/dev/null 2>&1 || echo "keine Bilder: $name" >&2
}

if [ "${1:-}" = --lauf ]; then shift; lauf "$@"; exit $?; fi
Z=${1:-$HOME/review/thema-021-bilder}
PAR=${2:-4}
mkdir -p "$Z/neu" "$Z/live"
{
    for m in "de 1024x768" "en 1920x1080"; do
        for f in archiv dokumente editor; do
            for s in hell dunkel; do echo "$f $m $s"; done
        done
        for f in rechner einstellungen muster-knoepfe muster-listen muster-text muster3; do echo "$f $m hell"; done
    done
} | while read -r f spr r s; do
    for qu in neu live; do echo "$f $spr $r $s $qu $Z/$qu"; done
done | xargs -P "$PAR" -L 1 bash "$E/werkzeug/regression-021.sh" --lauf
(cd "$Z/neu" && for b in *.png; do
    printf '%-58s ' "$b"; python3 -I "$E/werkzeug/bildvergleich.py" "$b" "../live/${b%-neu*}-live${b#*-neu}"
done) >"$Z/vergleich.txt"
ls "$Z"/neu/*.png | wc -l
findmnt -rn -o TARGET | grep "$E/laufzeit" || echo "keine Mounts aus dem Testlauf"
