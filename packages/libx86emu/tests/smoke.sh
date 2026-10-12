#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libx86emu libx86emu-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <x86emu.h>

int main(void)
{
    x86emu_t *emu = x86emu_new(X86EMU_PERM_RWX, 0);
    if (emu == 0)
        return 1;
    return x86emu_done(emu) != 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  "$smoke_dir/smoke.c" -lx86emu -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
