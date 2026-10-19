#!/bin/bash
# Baut integration/vorschlag/Querencia-Klassisch: labwc-Teil byte-gleich aus
# der heute aktiven Theme-Ablage (G2-R, e72ae8ed962abecb, nur gelesen) plus
# gtk-4.0, gtk-3.0 und index.theme aus diesem Repo; dazu die Liste
# integration/vorschlag/theme-manifest.txt (Format wie G2-R).
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
ALT=${QTH_ALT_ABLAGE:-$HOME/opt/querencia-theme/e72ae8ed962abecb}
V=$E/integration/vorschlag
python3 -I "$E/werkzeug/erzeugen.py" --pruefen
rm -rf "$V"
mkdir -p "$V/Querencia-Klassisch"
cp -r "$ALT/Querencia-Klassisch/labwc" "$V/Querencia-Klassisch/"
cp -r "$E/Querencia-Klassisch/gtk-4.0" "$E/Querencia-Klassisch/gtk-3.0" "$E/Querencia-Klassisch/index.theme" "$V/Querencia-Klassisch/"
chmod -R u+w,a+r "$V"
find "$V" -type d -exec chmod 0755 {} +
find "$V" -type f -exec chmod 0644 {} +
(cd "$V" && find Querencia-Klassisch -type f | LC_ALL=C sort | xargs sha256sum) >"$V/theme-manifest.txt"
B=$(sha256sum "$V/theme-manifest.txt" | cut -c1-64)
# Liste ins Integrationsskript eintragen (BAUM_NEU), wie es G2-R von Hand tat
sed -i "s/^BAUM_NEU=.*/BAUM_NEU=$B/" "$E/integration/thema-integrieren.sh"
echo "Vorlage: $(wc -l <"$V/theme-manifest.txt") Dateien, Liste $B"
