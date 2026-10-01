#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- gengetopt
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/options.ggo" <<'EOF'
package "openeuler-riscv-smoke"
version "1"
option "isa" i "target ISA" string typestr="NAME" required
EOF

gengetopt \
  --input="$smoke_dir/options.ggo" \
  --file-name=options \
  --output-dir="$smoke_dir"

cat >"$smoke_dir/main.c" <<'EOF'
#include "options.h"

#include <string.h>

int main(int argc, char **argv) {
    struct gengetopt_args_info args;
    if (cmdline_parser(argc, argv, &args) != 0) {
        return 1;
    }
    const int result = strcmp(args.isa_arg, "RVA23") == 0 ? 0 : 1;
    cmdline_parser_free(&args);
    return result;
}
EOF

cc "$smoke_dir/main.c" "$smoke_dir/options.c" -I"$smoke_dir" -o "$smoke_dir/smoke"
"$smoke_dir/smoke" --isa RVA23
