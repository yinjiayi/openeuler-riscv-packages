#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lcms2 lcms2-utils lcms2-devel lcms2-help
test -x /usr/bin/jpgicc
test -x /usr/bin/tifdiff
test -x /usr/bin/transicc
pkg-config --modversion lcms2 | grep -E '^2\.19(\.|$)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/lcms2-smoke.c" <<'EOF'
#include <lcms2.h>

int main(void) {
    cmsHPROFILE profile = cmsCreate_sRGBProfile();
    cmsUInt32Number version;
    if (profile == NULL) {
        return 1;
    }
    version = cmsGetEncodedICCversion(profile);
    cmsCloseProfile(profile);
    return version == 0 ? 2 : 0;
}
EOF
cc $({ pkg-config --cflags lcms2; }) "$smoke_dir/lcms2-smoke.c" \
  -o "$smoke_dir/lcms2-smoke" $({ pkg-config --libs lcms2; })
"$smoke_dir/lcms2-smoke"
