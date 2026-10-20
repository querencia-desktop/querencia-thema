#!/bin/bash
# Belegbilder für Querencia-Klassisch im ISOLIERTEN Lauf (eigener headless
# labwc, eigener D-Bus, GSETTINGS_BACKEND=memory, Wegwerfprofil). Die
# laufende Sitzung und dconf bleiben unberührt.
#
#   bash werkzeug/belege.sh <fall> <BREITExHÖHE> <vorher|nachher|weiss|dunkel|farbschema|gtkdark> [ziel]
#
# fall: muster-knoepfe muster-listen muster-regler muster-text muster-dialog
#       muster-popover muster-tooltip muster-klein muster3 muster3-liste rechner
#       einstellungen files
#       editor systemmonitor dateisuche software bilder panel panel-menue desktop
#       portal, portal-panel (mit Desktop-Portal: gsettings im laufenden
#       Programm umstellen)
# vorher  = GTK-Standardthema (wie live heute), Überlagerungsbalken an
# nachher = Querencia-Klassisch, gtk-overlay-scrolling=false (wie nach
#           „aktivieren“)
# weiss   = wie nachher, Auswahlschrift weiß (Vergleich, nicht ausgeliefert)
# dunkel  = wie nachher, Menü- und Werkzeugleiste dunkel (Ambiance-Kopf,
#           Vergleich der Richtungen, nicht ausgeliefert)
# farbschema = Thema 0.2: Querencia-Klassisch über das Settings-Portal,
#           Programm hell starten, dann color-scheme prefer-dark und zurück
#           (lauf-farbschema.sh); eigenes HOME im Profil.
# gtkdark   = wie nachher, aber GTK_THEME=Querencia-Klassisch:dark und
#           gtk-application-prefer-dark-theme: GTK lädt gtk-dark.css (auch GTK 3)
# QTH_THEMA_QUELLE=<Ordner Querencia-Klassisch> nimmt gtk-4.0/gtk-3.0 von dort
#           statt aus dem Repo (Regression gegen die Live-Ablage, nur gelesen).
# Alle Läufe mit GSK_DEBUG=full-redraw (ganze Fläche je Bild neu zeichnen).
# Ergebnis: <ziel>/<fall>-<R>-<thema>-*.png (Standard: nachweis/bilder)
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
FALL=${1:?fall}; R=${2:?Auflösung}; THEMA=${3:?vorher|nachher}
ZIEL=${4:-$E/nachweis/bilder}
case $R in *x*) ;; *) echo "Auflösung als BREITExHÖHE" >&2; exit 2 ;; esac
WB=${QTH_WERKZEUG_BIN:-$HOME/projects/querencia-rechner/werkzeug/bin}
[ -x "$WB/qeingabe" ] && [ -x "$WB/qausgabe" ] || { echo "qeingabe/qausgabe fehlen in $WB" >&2; exit 2; }
TQ=${QTH_THEMA_QUELLE:-$E/Querencia-Klassisch}
LIVE_LABWC=$(readlink -f "$HOME/.local/share/themes/Querencia-Klassisch/labwc")
OPT=$HOME/opt/querencia

MENUE=1
ZEIGER=""
INNEN=lauf-innen.sh
KLICK=0
case $FALL in
muster-knoepfe | muster-listen | muster-regler | muster-text) BIN=(python3 -I "$E/werkzeug/muster4.py" "${FALL#muster-}") ;;
muster-dialog) BIN=(python3 -I "$E/werkzeug/muster4.py" knoepfe dialog); MENUE=0 ;;
muster-popover) BIN=(python3 -I "$E/werkzeug/muster4.py" knoepfe popover); MENUE=0 ;;
muster-tooltip) BIN=(python3 -I "$E/werkzeug/muster4.py" knoepfe tooltip); MENUE=0; ZEIGER="98 495" ;;
muster-klein) BIN=(python3 -I "$E/werkzeug/muster4.py" listen klein) ;;
portal) BIN=(python3 -I "$E/werkzeug/muster4.py" listen); INNEN=lauf-portal.sh ;;
muster3) BIN=(python3 -I "$E/werkzeug/muster3.py") ;;
muster3-liste) BIN=(python3 -I "$E/werkzeug/muster3.py" liste) ;;
rechner) BIN=("$OPT/bin/querencia-rechner") ;;
einstellungen) BIN=("$OPT/bin/querencia-einstellungen"); MENUE=0 ;;
files) BIN=("$(sed -n 's/^Exec=\([^ ]*\).*/\1/p' "$HOME/.local/share/applications/io.github.lgse.Strata.desktop" | head -1)" /usr/share/doc) ;;
editor) BIN=("$OPT/bin/querencia-editor" "$E/README.md") ;;
systemmonitor) BIN=("$OPT/bin/querencia-systemmonitor") ;;
dateisuche) BIN=("$OPT/bin/querencia-dateisuche") ;;
software) BIN=("$OPT/bin/querencia-software"); MENUE=0 ;;
bilder) BIN=("$OPT/bin/querencia-bilder") ;;
panel) BIN=("$OPT/bin/querencia-panel"); MENUE=0 ;;
panel-menue) BIN=("$OPT/bin/querencia-panel"); MENUE=0; ZEIGER="85 16"; KLICK=1 ;;
desktop) BIN=("$OPT/bin/querencia-desktop"); MENUE=0 ;;
portal-panel) BIN=("$OPT/bin/querencia-panel"); INNEN=lauf-portal.sh ;;
*) echo "unbekannter Fall $FALL" >&2; exit 2 ;;
esac

PROFIL=$E/gui-test/$FALL-$R-$THEMA
[ -d "$E/gui-test" ] && [ "$(dirname "$PROFIL")" = "$E/gui-test" ] && rm -rf "$PROFIL"
mkdir -p "$PROFIL/config/labwc" "$PROFIL/config/gtk-4.0" "$PROFIL/config/gtk-3.0" \
    "$PROFIL/data/themes/Querencia-Klassisch" "$ZIEL"
# Fensterrahmen wie live (labwc-Teil des Themas, nur gelesen); GTK-Teile aus
# dem Repo bzw. einer Variante.
ln -s "$LIVE_LABWC" "$PROFIL/data/themes/Querencia-Klassisch/labwc"
SCHRIFT=$(gsettings get org.gnome.desktop.interface font-name 2>/dev/null | tr -d "'")
{
    echo "[Settings]"
    [ -n "$SCHRIFT" ] && echo "gtk-font-name=$SCHRIFT"
    # portal: Thema nur über gsettings (Portal), nicht über settings.ini
    if [ "$THEMA" != vorher ] && [ "$THEMA" != farbschema ] && [ "${FALL#portal}" = "$FALL" ]; then
        echo "gtk-theme-name=Querencia-Klassisch"
        echo "gtk-overlay-scrolling=false"
        if [ "$THEMA" = gtkdark ]; then echo "gtk-application-prefer-dark-theme=true"; fi
    fi
} | tee "$PROFIL/config/gtk-4.0/settings.ini" >"$PROFIL/config/gtk-3.0/settings.ini"
case $THEMA in
vorher) ;;
nachher | farbschema | gtkdark)
    ln -s "$TQ/gtk-4.0" "$PROFIL/data/themes/Querencia-Klassisch/gtk-4.0"
    ln -s "$TQ/gtk-3.0" "$PROFIL/data/themes/Querencia-Klassisch/gtk-3.0" ;;
weiss | dunkel)
    for v in gtk-4.0 gtk-3.0; do
        mkdir -p "$PROFIL/data/themes/Querencia-Klassisch/$v"
        cp -r "$E/Querencia-Klassisch/$v/." "$PROFIL/data/themes/Querencia-Klassisch/$v/"
    done
    cat "$E/werkzeug/varianten/$THEMA.css" >>"$PROFIL/data/themes/Querencia-Klassisch/gtk-4.0/gtk.css" ;;
*) echo "Thema vorher|nachher|weiss|dunkel|farbschema|gtkdark" >&2; exit 2 ;;
esac
cat >"$PROFIL/config/labwc/rc.xml" <<X
<?xml version="1.0"?>
<labwc_config>
  <core><decoration>server</decoration></core>
  <theme><name>Querencia-Klassisch</name><icon>gnome-human</icon></theme>
  <windowRules>
    <windowRule identifier="*"><action name="MoveTo" x="16" y="12" /></windowRule>
  </windowRules>
</labwc_config>
X
{
    printf 'BIN=('; printf '%q ' "${BIN[@]}"; printf ')\n'
    printf 'Q=%q\nQA=%q\nOUT=%q\nR=%q\nNAME=%q\nMENUE=%q\nZEIGER=%q\nKLICK=%q\nSCHRIFT=%q\n' \
        "$WB/qeingabe" "$WB/qausgabe" "$ZIEL" "$R" "$FALL-$R-$THEMA" "$MENUE" "$ZEIGER" "$KLICK" "$SCHRIFT"
} >"$PROFIL/env.sh"
# GTK 3 nimmt unter Wayland Thema und Balkenart aus gsettings (im Test nur
# Speicher-Backend), nicht aus settings.ini: dort GTK_THEME und
# GTK_OVERLAY_SCROLLING. GTK 4 liest settings.ini (ohne Portal).
UMG=()
[ "$THEMA" != vorher ] && UMG=(GTK_THEME=Querencia-Klassisch GTK_OVERLAY_SCROLLING=0)
[ "$THEMA" = gtkdark ] && UMG=(GTK_THEME=Querencia-Klassisch:dark GTK_OVERLAY_SCROLLING=0)
# Sprache wie live (session/querencia/labwc/environment)
case $FALL in portal*) UMG=(QTH_PORTALE=1) ;; esac
[ "$THEMA" = farbschema ] && { INNEN=lauf-farbschema.sh; UMG=(QTH_PORTALE=1 QTH_EIGENES_HOME=1); }
env "${UMG[@]}" GSK_DEBUG=full-redraw LANG=en_US.UTF-8 LANGUAGE=de python3 -I "$E/werkzeug/isoliert.py" "$PROFIL" "$E/werkzeug/$INNEN" 90 || true
ls "$ZIEL"/"$FALL-$R-$THEMA"-*.png 2>/dev/null || echo "keine Bilder: $FALL $R $THEMA" >&2
