#!/bin/bash
# Thema 0.2: baut integration/vorschlag-02/Querencia-Klassisch. labwc/ und
# index.theme byte-gleich aus der Ablage 0.1 (a53ff41c34adeb72, nur gelesen),
# gtk-4.0/ und gtk-3.0/ aus diesem Repo; dazu die Liste
# integration/vorschlag-02/theme-manifest.txt. Trägt BAUM_NEU in
# integration/thema-02-integrieren.sh ein. Die Vorlage 0.1
# (integration/vorschlag/, vorlage-bauen.sh) bleibt unberührt.
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
ALT=${QTH_ALT_ABLAGE:-$HOME/opt/querencia-theme/a53ff41c34adeb72}
V=$E/integration/vorschlag-02
python3 -I "$E/werkzeug/erzeugen.py" --pruefen
cmp -s "$ALT/Querencia-Klassisch/index.theme" "$E/Querencia-Klassisch/index.theme" \
    || { echo "index.theme weicht von der Ablage 0.1 ab" >&2; exit 1; }
rm -rf "$V"
mkdir -p "$V/Querencia-Klassisch"
cp -r "$ALT/Querencia-Klassisch/labwc" "$ALT/Querencia-Klassisch/index.theme" "$V/Querencia-Klassisch/"
cp -r "$E/Querencia-Klassisch/gtk-4.0" "$E/Querencia-Klassisch/gtk-3.0" "$V/Querencia-Klassisch/"
chmod -R u+w,a+r "$V"
find "$V" -type d -exec chmod 0755 {} +
find "$V" -type f -exec chmod 0644 {} +
(cd "$V" && find Querencia-Klassisch -type f | LC_ALL=C sort | xargs sha256sum) >"$V/theme-manifest.txt"
B=$(sha256sum "$V/theme-manifest.txt" | cut -c1-64)
sed -i "s/^BAUM_NEU=.*/BAUM_NEU=$B/" "$E/integration/thema-02-integrieren.sh"
echo "Vorlage 0.2: $(wc -l <"$V/theme-manifest.txt") Dateien, Liste $B"
