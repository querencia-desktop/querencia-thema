#!/bin/bash
# Thema 0.2.1: baut integration/021/vorlage. labwc/ und index.theme
# byte-gleich aus der Ablage 0.2 (b531c62050830d10, live, nur gelesen),
# gtk-4.0/ und gtk-3.0/ aus diesem Repo; dazu theme-manifest.txt (Liste der
# neuen Ablage), liste-02.txt (Liste der Ablage 0.2 aus vorschlag-02) und
# SHA256SUMS über alle Dateien der Vorlage. Trägt BAUM_NEU und SUMMEN_SHA in
# integration/021/thema-021-integrieren.sh ein und spiegelt integration/021
# in den Arbeitsordner ~/projects/querencia-thema-021/integration
# (QTH_ARBEITSORDNER). Vorlagen 0.1 und 0.2 bleiben unberührt.
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
ALT=${QTH_ALT_ABLAGE:-$HOME/opt/querencia-theme/b531c62050830d10}
I=$E/integration/021
V=$I/vorlage
A=${QTH_ARBEITSORDNER:-$HOME/projects/querencia-thema-021}/integration
python3 -I "$E/werkzeug/erzeugen.py" --pruefen
cmp -s "$ALT/Querencia-Klassisch/index.theme" "$E/Querencia-Klassisch/index.theme" \
    || { echo "index.theme weicht von der Ablage 0.2 ab" >&2; exit 1; }
[ "$(sha256sum "$E/integration/vorschlag-02/theme-manifest.txt" | cut -c1-16)" = "${ALT##*/}" ] \
    || { echo "vorschlag-02/theme-manifest.txt passt nicht zur Ablage 0.2" >&2; exit 1; }
rm -rf "$V"
mkdir -p "$V/Querencia-Klassisch"
cp -r "$ALT/Querencia-Klassisch/labwc" "$ALT/Querencia-Klassisch/index.theme" "$V/Querencia-Klassisch/"
cp -r "$E/Querencia-Klassisch/gtk-4.0" "$E/Querencia-Klassisch/gtk-3.0" "$V/Querencia-Klassisch/"
cp "$E/integration/vorschlag-02/theme-manifest.txt" "$V/liste-02.txt"
chmod -R u+w,a+r "$V"
find "$V" -type d -exec chmod 0755 {} +
find "$V" -type f -exec chmod 0644 {} +
(cd "$V" && find Querencia-Klassisch -type f | LC_ALL=C sort | xargs sha256sum) >"$V/theme-manifest.txt"
(cd "$V" && find . -type f ! -name SHA256SUMS | sed 's#^\./##' | LC_ALL=C sort | xargs sha256sum) >"$V/SHA256SUMS"
B=$(sha256sum "$V/theme-manifest.txt" | cut -c1-64)
S=$(sha256sum "$V/SHA256SUMS" | cut -c1-64)
sed -i -e "s/^BAUM_NEU=.*/BAUM_NEU=$B/" -e "s/^SUMMEN_SHA=.*/SUMMEN_SHA=$S/" "$I/thema-021-integrieren.sh"
rm -rf "$A"
mkdir -p "$A"
cp -r "$I/thema-021-integrieren.sh" "$I/probe-021.sh" "$V" "$A/"
diff -r "$I/vorlage" "$A/vorlage" >/dev/null && cmp -s "$I/thema-021-integrieren.sh" "$A/thema-021-integrieren.sh"
echo "Vorlage 0.2.1: $(wc -l <"$V/theme-manifest.txt") Dateien, Liste $B, SHA256SUMS $S"
echo "Arbeitsordner: $A"
