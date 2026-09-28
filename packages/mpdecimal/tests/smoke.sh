#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- mpdecimal mpdecimal-devel
rpm -q --provides mpdecimal | grep -F 'libmpdec.so.4()(64bit)'
rpm -q --provides mpdecimal | grep -F 'libmpdec++.so.4()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/mpdecimal-smoke.c" <<'EOF'
#include <mpdecimal.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    mpd_context_t ctx;
    uint32_t status = 0;
    mpd_maxcontext(&ctx);
    mpd_t *a = mpd_new(&ctx), *b = mpd_new(&ctx), *sum = mpd_new(&ctx);
    if (!a || !b || !sum) return 1;
    mpd_qset_string(a, "1.2", &ctx, &status);
    mpd_qset_string(b, "3.4", &ctx, &status);
    mpd_qadd(sum, a, b, &ctx, &status);
    char *result = mpd_to_sci(sum, 0);
    int failed = status != 0 || result == NULL || strcmp(result, "4.6") != 0;
    free(result);
    mpd_del(a); mpd_del(b); mpd_del(sum);
    return failed;
}
EOF
cc "$smoke_dir/mpdecimal-smoke.c" -o "$smoke_dir/mpdecimal-smoke" \
  $(pkg-config --cflags --libs libmpdec)
"$smoke_dir/mpdecimal-smoke"

cat >"$smoke_dir/mpdecimal-smoke.cc" <<'EOF'
#include <decimal.hh>
int main() {
    const decimal::Decimal sum = decimal::Decimal("1.2") + decimal::Decimal("3.4");
    return sum.to_sci() == "4.6" ? 0 : 1;
}
EOF
c++ "$smoke_dir/mpdecimal-smoke.cc" -o "$smoke_dir/mpdecimal-smoke-cxx" \
  $(pkg-config --cflags --libs 'libmpdec++')
"$smoke_dir/mpdecimal-smoke-cxx"
