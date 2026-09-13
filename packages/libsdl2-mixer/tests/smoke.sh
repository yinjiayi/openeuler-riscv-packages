#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- SDL2_mixer SDL2_mixer-devel
test "$(pkg-config --modversion SDL2_mixer)" = "2.8.2"

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>

#include <stdio.h>

static const unsigned char wave[] = {
    'R','I','F','F', 40,0,0,0, 'W','A','V','E',
    'f','m','t',' ', 16,0,0,0, 1,0, 1,0,
    0x40,0x1f,0,0, 0x80,0x3e,0,0, 2,0, 16,0,
    'd','a','t','a', 4,0,0,0, 0,0, 0,0
};

int main(void) {
    const SDL_version *linked = Mix_Linked_Version();
    const int wanted = MIX_INIT_FLAC | MIX_INIT_MOD | MIX_INIT_MP3 |
                       MIX_INIT_OGG | MIX_INIT_MID | MIX_INIT_OPUS |
                       MIX_INIT_WAVPACK;
    SDL_RWops *input;
    Mix_Chunk *chunk;

    if (linked == NULL || linked->major != 2 || linked->minor != 8 ||
        linked->patch != 2) {
        return 1;
    }
    if (SDL_Init(SDL_INIT_AUDIO) != 0) {
        fprintf(stderr, "SDL_Init: %s\n", SDL_GetError());
        return 2;
    }
    if ((Mix_Init(wanted) & wanted) != wanted) {
        fprintf(stderr, "Mix_Init: %s\n", Mix_GetError());
        return 3;
    }
    if (Mix_OpenAudio(8000, AUDIO_S16SYS, 1, 256) != 0) {
        fprintf(stderr, "Mix_OpenAudio: %s\n", Mix_GetError());
        return 4;
    }
    if (!Mix_HasMusicDecoder("FLAC") || !Mix_HasMusicDecoder("MOD") ||
        !Mix_HasMusicDecoder("MP3") || !Mix_HasMusicDecoder("OGG") ||
        !Mix_HasMusicDecoder("MIDI") || !Mix_HasMusicDecoder("OPUS") ||
        !Mix_HasMusicDecoder("WAVPACK")) {
        return 5;
    }
    input = SDL_RWFromConstMem(wave, (int)sizeof(wave));
    chunk = input == NULL ? NULL : Mix_LoadWAV_RW(input, 1);
    if (chunk == NULL) {
        fprintf(stderr, "Mix_LoadWAV_RW: %s\n", Mix_GetError());
        return 6;
    }
    if (Mix_PlayChannel(-1, chunk, 0) < 0) {
        fprintf(stderr, "Mix_PlayChannel: %s\n", Mix_GetError());
        return 7;
    }
    Mix_HaltChannel(-1);
    Mix_FreeChunk(chunk);
    Mix_CloseAudio();
    Mix_Quit();
    SDL_Quit();
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -o "$smoke_dir/smoke" \
  $(pkg-config --cflags --libs SDL2_mixer)
SDL_AUDIODRIVER=dummy "$smoke_dir/smoke"
