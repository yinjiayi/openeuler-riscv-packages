#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libfishsound libfishsound-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat > "$smoke_dir/smoke.c" <<'EOF'
#include <fishsound/fishsound.h>
#include <stdio.h>

int main(void) {
    const int formats[] = {FISH_SOUND_VORBIS, FISH_SOUND_SPEEX, FISH_SOUND_FLAC};
    const char *names[] = {"vorbis", "speex", "flac"};
    unsigned int i;
    for (i = 0; i < 3; ++i) {
        FishSoundInfo info = {16000, 1, formats[i]};
        FishSound *encoder = fish_sound_new(FISH_SOUND_ENCODE, &info);
        FishSound *decoder = fish_sound_new(FISH_SOUND_DECODE, &info);
        if (encoder == NULL || decoder == NULL) return (int)i + 1;
        fish_sound_delete(encoder);
        fish_sound_delete(decoder);
        puts(names[i]);
    }
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs fishsound) -o "$smoke_dir/smoke"
"$smoke_dir/smoke" | grep -Fx 'flac'
