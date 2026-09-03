#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libcue libcue-devel
pkg-config --modversion libcue | grep -Fx '2.3.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libcue-smoke.c" <<'EOF'
#include <libcue.h>
#include <string.h>

int main(void) {
    static const char cue[] =
        "PERFORMER \"openEuler\"\n"
        "FILE \"disc.wav\" WAVE\n"
        "  TRACK 01 AUDIO\n"
        "    TITLE \"RVA23\"\n"
        "    INDEX 01 00:00:00\n";
    Cd *disc = cue_parse_string(cue);
    Track *track;
    const char *title;
    int ok;

    if (disc == NULL || cd_get_ntrack(disc) != 1)
        return 1;
    track = cd_get_track(disc, 1);
    title = track == NULL ? NULL : cdtext_get(PTI_TITLE, track_get_cdtext(track));
    ok = track != NULL && track_get_mode(track) == MODE_AUDIO &&
         title != NULL && strcmp(title, "RVA23") == 0;
    cd_delete(disc);
    return ok ? 0 : 2;
}
EOF

read -r -a pkg_flags <<<"$(pkg-config --cflags --libs libcue)"
cc "$smoke_dir/libcue-smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/libcue-smoke"
"$smoke_dir/libcue-smoke"
