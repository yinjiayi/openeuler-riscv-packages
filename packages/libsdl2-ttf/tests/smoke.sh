#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- SDL2_ttf SDL2_ttf-devel
test "$(pkg-config --modversion SDL2_ttf)" = 2.24.0

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#define SDL_MAIN_HANDLED
#include <SDL.h>
#include <SDL_ttf.h>

int main(void) {
    int freetype_major = 0;
    int freetype_minor = 0;
    int freetype_patch = 0;
    int harfbuzz_major = 0;
    int harfbuzz_minor = 0;
    int harfbuzz_patch = 0;
    const SDL_version *linked = 0;

    SDL_SetMainReady();
    if (SDL_Init(0) != 0 || TTF_Init() != 0) {
        return 1;
    }
    linked = TTF_Linked_Version();
    TTF_GetFreeTypeVersion(&freetype_major, &freetype_minor, &freetype_patch);
    TTF_GetHarfBuzzVersion(&harfbuzz_major, &harfbuzz_minor, &harfbuzz_patch);
    TTF_Quit();
    SDL_Quit();
    return linked == 0 || linked->major != 2 || linked->minor != 24 ||
           linked->patch != 0 || freetype_major <= 0 || harfbuzz_major <= 0;
}
EOF

read -r -a sdl_ttf_flags <<<"$(pkg-config --cflags --libs SDL2_ttf)"
cc "$smoke_dir/smoke.c" "${sdl_ttf_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
