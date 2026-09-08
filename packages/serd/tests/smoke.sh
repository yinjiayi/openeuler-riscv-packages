#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- serd serd-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '@prefix ex: <https://example.invalid/> .\nex:s ex:p "RVA23" .\n' >"$d/in.ttl"
serdi -i turtle -o ntriples "$d/in.ttl" >"$d/out.nt"
grep -F '"RVA23"' "$d/out.nt"
