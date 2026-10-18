#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libansilove libansilove-devel
test -f /usr/include/ansilove.h

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'C'
#include <ansilove.h>

int main(int argc, char **argv) {
  struct ansilove_ctx ctx;
  struct ansilove_options options;
  if (argc != 3 || ansilove_init(&ctx, &options) != 0)
    return 1;
  int ok = ansilove_loadfile(&ctx, argv[1]) == 0 &&
           ansilove_ansi(&ctx, &options) == 0 &&
           ansilove_savefile(&ctx, argv[2]) == 0;
  ansilove_clean(&ctx);
  return ok ? 0 : 1;
}
C

cc "$smoke_dir/smoke.c" -lansilove -o "$smoke_dir/smoke"
printf 'Hello, RVA23!\n' >"$smoke_dir/fixture.ans"
"$smoke_dir/smoke" "$smoke_dir/fixture.ans" "$smoke_dir/fixture.png"
test "$(od -An -tx1 -N8 "$smoke_dir/fixture.png" | tr -d ' \n')" = 89504e470d0a1a0a
