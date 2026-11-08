#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liblognorm liblognorm-devel liblognorm-utils liblognorm-help
lognormalizer -V 2>&1 | grep -F 'liblognorm version: 2.1.0'
pkg-config --modversion lognorm | grep -Fx '2.1.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/rules.rb" <<'EOF'
version=2
rule=:hello %name:word%
EOF
printf 'hello RVA23\n' | lognormalizer -r "$smoke_dir/rules.rb" -e json \
  >"$smoke_dir/classic.json"
printf 'hello RVA23\n' | lognormalizer -oturbo -r "$smoke_dir/rules.rb" -e json \
  >"$smoke_dir/turbo.json"
# The engines may serialize JSON with different whitespace. Check the complete
# result, not a substring that can accept unparsed input or extra fields.
python3 - "$smoke_dir/classic.json" "$smoke_dir/turbo.json" <<'PY'
import json
import sys


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError("non-JSON constant: " + value)


results = []
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as stream:
        result = json.load(stream, object_pairs_hook=unique_object,
                           parse_constant=invalid_constant)
    if result != {"name": "RVA23"}:
        raise SystemExit("unexpected normalization result in " + path)
    results.append(result)
if len(results) != 2 or results[0] != results[1]:
    raise SystemExit("classic and TurboVM results differ")
print("classic and TurboVM JSON both equal", json.dumps(results[0], sort_keys=True))
PY

cat >"$smoke_dir/liblognorm-smoke.c" <<'EOF'
#include <liblognorm.h>
#include <string.h>

int main(void) {
    ln_ctx context = ln_initCtx();
    if (context == NULL || strcmp(ln_version(), "2.1.0") != 0) {
        return 1;
    }
    ln_exitCtx(context);
    return 0;
}
EOF
cc $({ pkg-config --cflags lognorm; }) "$smoke_dir/liblognorm-smoke.c" \
  -o "$smoke_dir/liblognorm-smoke" $({ pkg-config --libs lognorm; })
"$smoke_dir/liblognorm-smoke"
