#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lhasa lhasa-devel
test -x /usr/bin/lha
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <lhasa.h>

#include <stddef.h>

int main(void) {
    const LHADecoderType *decoder = lha_decoder_for_name("-lh5-");
    return decoder == NULL ? 1 : 0;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs liblhasa) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
