#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- flac flac-devel flac-help
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

dd if=/dev/zero of="$smoke_dir/silence.raw" bs=2 count=8000 status=none
flac --force --silent --force-raw-format --endian=little --sign=signed \
  --channels=1 --bps=16 --sample-rate=8000 \
  -o "$smoke_dir/silence.flac" "$smoke_dir/silence.raw"
flac --test --silent "$smoke_dir/silence.flac"
flac --decode --force --silent --force-raw-format --endian=little --sign=signed \
  -o "$smoke_dir/decoded.raw" "$smoke_dir/silence.flac"
cmp "$smoke_dir/silence.raw" "$smoke_dir/decoded.raw"
test "$(metaflac --show-sample-rate "$smoke_dir/silence.flac")" = 8000

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <FLAC/format.h>
#include <FLAC/stream_encoder.h>

int main(void) {
    FLAC__StreamEncoder *encoder;
    if (!FLAC__format_sample_rate_is_valid(48000)) return 1;
    encoder = FLAC__stream_encoder_new();
    if (encoder == 0) return 2;
    FLAC__stream_encoder_delete(encoder);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs flac) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
