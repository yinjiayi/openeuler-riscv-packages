#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libshine libshine-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'C'
#include <shine/layer3.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
  static const unsigned char header[44] = {
    'R','I','F','F', 0x24,0x09,0,0, 'W','A','V','E',
    'f','m','t',' ', 16,0,0,0, 1,0, 1,0,
    0x44,0xac,0,0, 0x88,0x58,0x01,0, 2,0, 16,0,
    'd','a','t','a', 0,9,0,0
  };
  unsigned char samples[2304];
  FILE *wave;
  if (argc != 2 || shine_check_config(44100, 128) != MPEG_I) return 1;
  wave = fopen(argv[1], "wb");
  if (!wave) return 2;
  memset(samples, 0, sizeof(samples));
  if (fwrite(header, 1, sizeof(header), wave) != sizeof(header) ||
      fwrite(samples, 1, sizeof(samples), wave) != sizeof(samples) ||
      fclose(wave) != 0) return 3;
  return 0;
}
C
gcc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs shine) -o "$smoke_dir/smoke"
"$smoke_dir/smoke" "$smoke_dir/silence.wav"
shineenc -q "$smoke_dir/silence.wav" "$smoke_dir/silence.mp3"
test -s "$smoke_dir/silence.mp3"
magic=$(od -An -tx1 -N2 "$smoke_dir/silence.mp3" | tr -d '[:space:]')
case "$magic" in
  ffe?|fff?) ;;
  *) echo "invalid installed MP3 frame sync: $magic" >&2; exit 1 ;;
esac
