#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- soundtouch soundtouch-devel
version_output=$(soundstretch 2>&1 || :)
printf '%s\n' "$version_output" | grep -F 'SoundStretch v2.4.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cpp" <<'EOF'
#include <SoundTouch.h>

int main() {
    soundtouch::SoundTouch processor;
    processor.setSampleRate(48000);
    processor.setChannels(2);
    processor.setTempo(1.0f);
    return processor.getVersionId() == 20401 ? 0 : 1;
}
EOF

read -r -a soundtouch_flags <<<"$(pkg-config --cflags --libs soundtouch)"
c++ -std=c++17 "$smoke_dir/smoke.cpp" \
  "${soundtouch_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
