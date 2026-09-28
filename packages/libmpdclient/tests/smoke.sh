#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmpdclient libmpdclient-devel
test "$(pkg-config --modversion libmpdclient)" = 2.26

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'C'
#include <mpd/client.h>

int main(void) {
    if (!LIBMPDCLIENT_CHECK_VERSION(2, 26, 0))
        return 1;
    if (mpd_tag_name_parse("Artist") != MPD_TAG_ARTIST)
        return 2;
    if (mpd_tag_name_parse("not-a-tag") != MPD_TAG_UNKNOWN)
        return 3;
    return 0;
}
C

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libmpdclient) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
