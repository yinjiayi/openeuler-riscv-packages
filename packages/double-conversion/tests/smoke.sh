#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- double-conversion double-conversion-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cc" <<'EOF'
#include <cstring>
#include <double-conversion/double-conversion.h>
int main() {
    char text[32];
    double_conversion::StringBuilder output(text, sizeof(text));
    const bool ok = double_conversion::DoubleToStringConverter::EcmaScriptConverter().ToShortest(1.5, &output);
    output.Finalize();
    return ok && std::strcmp(text, "1.5") == 0 ? 0 : 1;
}
EOF
c++ "$smoke_dir/smoke.cc" -ldouble-conversion -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
