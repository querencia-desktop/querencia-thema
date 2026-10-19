#!/bin/bash
# SHA256SUMS im Repo-Wurzelordner: Thema, Vorlage, Integrationsskript, Probe,
# Quellen und Werkzeuge (Grundlage der Freigabe durch die Status-Session).
set -euo pipefail
E=$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)
cd "$E"
{
    find Querencia-Klassisch integration quelle werkzeug -type f \
        ! -path 'werkzeug/__pycache__/*' | LC_ALL=C sort | xargs sha256sum
} >SHA256SUMS
sha256sum -c --quiet SHA256SUMS
echo "SHA256SUMS: $(wc -l <SHA256SUMS) Dateien, $(sha256sum SHA256SUMS | cut -c1-64)"
