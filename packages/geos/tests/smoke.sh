#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- geos geos-devel
geosop --help | grep -F -- 'geosop - GEOS 3.14.1' >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <geos_c.h>

int main(void) {
    GEOSContextHandle_t context = GEOS_init_r();
    GEOSGeometry *geometry;
    if (context == 0)
        return 1;
    geometry = GEOSGeomFromWKT_r(context, "POINT (1 2)");
    if (geometry == 0)
        return 1;
    GEOSGeom_destroy_r(context, geometry);
    GEOS_finish_r(context);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -lgeos_c -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
