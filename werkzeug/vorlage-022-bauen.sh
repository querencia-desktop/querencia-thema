#!/bin/bash
# Thema 0.2.2: baut integration/022/vorlage aus diesem Repo:
#   Querencia-Klassisch/{gtk-4.0,gtk-3.0,index.theme}
#   Querencia-Klassisch/labwc/       = labwc/Querencia-Klassisch/ + labwc/themerc-override-dunkel
#   Querencia-Klassisch-Dunkel/labwc = labwc/Querencia-Klassisch-Dunkel/
# Prüft vorher: erzeugen.py --pruefen, labwc-knoepfe.py --pruefen, Kontrast
# (Exit 0), index.theme und labwc hell byte-gleich mit der Ablage 0.2.1
# (22824d05ceb49cad, live, nur gelesen). Dazu theme-manifest.txt (Liste der
# neuen Ablage), liste-021.txt (Liste der Ablage 0.2.1 aus integration/021)
# und SHA256SUMS über alle Dateien der Vorlage. Trägt BAUM_NEU und
# SUMMEN_SHA in integration/022/thema-022-integrieren.sh ein und spiegelt
# integration/022 in den Arbeitsordner ~/projects/querencia-thema-022/integration
# (QTH_ARBEITSORDNER). Vorlagen 0.1, 0.2 und 0.2.1 bleiben unberührt.
# Nach dem Tag thema/gtk-0.2.2-int nicht mehr ausführen.
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
ALT=${QTH_ALT_ABLAGE:-$HOME/opt/querencia-theme/22824d05ceb49cad}
I=$E/integration/022
V=$I/vorlage
A=${QTH_ARBEITSORDNER:-$HOME/projects/querencia-thema-022}/integration
python3 -I "$E/werkzeug/erzeugen.py" --pruefen
python3 -I "$E/werkzeug/labwc-knoepfe.py" --pruefen
python3 -I "$E/werkzeug/kontrast.py" >/dev/null || { echo "kontrast.py: Pflichtpaar verfehlt" >&2; exit 1; }
cmp -s "$ALT/Querencia-Klassisch/index.theme" "$E/Querencia-Klassisch/index.theme" \
    || { echo "index.theme weicht von der Ablage 0.2.1 ab" >&2; exit 1; }
diff -r "$ALT/Querencia-Klassisch/labwc" "$E/labwc/Querencia-Klassisch" >/dev/null \
    || { echo "labwc/Querencia-Klassisch weicht von der Ablage 0.2.1 ab" >&2; exit 1; }
[ "$(sha256sum "$E/integration/021/vorlage/theme-manifest.txt" | cut -c1-16)" = "${ALT##*/}" ] \
    || { echo "integration/021/vorlage/theme-manifest.txt passt nicht zur Ablage 0.2.1" >&2; exit 1; }
rm -rf "$V"
mkdir -p "$V/Querencia-Klassisch-Dunkel"
cp -r "$E/Querencia-Klassisch" "$V/"
cp -r "$E/labwc/Querencia-Klassisch" "$V/Querencia-Klassisch/labwc"
cp "$E/labwc/themerc-override-dunkel" "$V/Querencia-Klassisch/labwc/"
cp -r "$E/labwc/Querencia-Klassisch-Dunkel" "$V/Querencia-Klassisch-Dunkel/labwc"
cp "$E/integration/021/vorlage/theme-manifest.txt" "$V/liste-021.txt"
chmod -R u+w,a+r "$V"
find "$V" -type d -exec chmod 0755 {} +
find "$V" -type f -exec chmod 0644 {} +
(cd "$V" && find Querencia-Klassisch Querencia-Klassisch-Dunkel -type f | LC_ALL=C sort | xargs sha256sum) >"$V/theme-manifest.txt"
(cd "$V" && find . -type f ! -name SHA256SUMS | sed 's#^\./##' | LC_ALL=C sort | xargs sha256sum) >"$V/SHA256SUMS"
B=$(sha256sum "$V/theme-manifest.txt" | cut -c1-64)
S=$(sha256sum "$V/SHA256SUMS" | cut -c1-64)
sed -i -e "s/^BAUM_NEU=.*/BAUM_NEU=$B/" -e "s/^SUMMEN_SHA=.*/SUMMEN_SHA=$S/" "$I/thema-022-integrieren.sh"
rm -rf "$A"
mkdir -p "$A"
cp -r "$I/thema-022-integrieren.sh" "$I/probe-022.sh" "$V" "$A/"
diff -r "$I/vorlage" "$A/vorlage" >/dev/null && cmp -s "$I/thema-022-integrieren.sh" "$A/thema-022-integrieren.sh"
echo "Vorlage 0.2.2: $(wc -l <"$V/theme-manifest.txt") Dateien, Liste $B, SHA256SUMS $S"
echo "Arbeitsordner: $A"
