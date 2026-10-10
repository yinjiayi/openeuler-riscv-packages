#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- allegro allegro-devel

modules=(
  allegro-5
  allegro_acodec-5
  allegro_audio-5
  allegro_color-5
  allegro_dialog-5
  allegro_font-5
  allegro_image-5
  allegro_main-5
  allegro_memfile-5
  allegro_physfs-5
  allegro_primitives-5
  allegro_ttf-5
  allegro_video-5
)
for module in "${modules[@]}"; do
  pkg-config --modversion "$module" | grep -Fx '5.2.11'
done

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/allegro-smoke.c" <<'EOF'
#include <stdint.h>
#include <allegro5/allegro.h>
#include <allegro5/allegro_acodec.h>
#include <allegro5/allegro_audio.h>
#include <allegro5/allegro_color.h>
#include <allegro5/allegro_font.h>
#include <allegro5/allegro_image.h>
#include <allegro5/allegro_memfile.h>
#include <allegro5/allegro_native_dialog.h>
#include <allegro5/allegro_physfs.h>
#include <allegro5/allegro_primitives.h>
#include <allegro5/allegro_ttf.h>
#include <allegro5/allegro_video.h>

static int is_expected_version(uint32_t version)
{
    return (version >> 8) == ((5u << 16) | (2u << 8) | 11u);
}

int main(void)
{
    const uint32_t versions[] = {
        al_get_allegro_version(),
        al_get_allegro_acodec_version(),
        al_get_allegro_audio_version(),
        al_get_allegro_color_version(),
        al_get_allegro_font_version(),
        al_get_allegro_image_version(),
        al_get_allegro_memfile_version(),
        al_get_allegro_native_dialog_version(),
        al_get_allegro_physfs_version(),
        al_get_allegro_primitives_version(),
        al_get_allegro_ttf_version(),
        al_get_allegro_video_version()
    };
    unsigned int index;

    for (index = 0; index < sizeof versions / sizeof versions[0]; ++index) {
        if (!is_expected_version(versions[index])) {
            return 1;
        }
    }
    return 0;
}
EOF

read -r -a allegro_cflags <<<"$(pkg-config --cflags "${modules[@]}")"
read -r -a allegro_libs <<<"$(pkg-config --libs "${modules[@]}")"
cc "${allegro_cflags[@]}" "$smoke_dir/allegro-smoke.c" \
  "${allegro_libs[@]}" -o "$smoke_dir/allegro-smoke"
"$smoke_dir/allegro-smoke"
