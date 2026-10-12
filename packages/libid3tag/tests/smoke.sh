#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libid3tag libid3tag-devel
rpm -q --provides libid3tag | grep -F 'libid3tag.so.0()(64bit)'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/id3tag-smoke.c" <<'EOF'
#include <id3tag.h>
#include <string.h>

int main(void) {
    struct id3_tag *tag = id3_tag_new();
    struct id3_tag *parsed;
    id3_byte_t data[128], rendered[128];
    if (!tag) return 1;
    if (id3_tag_options(tag, ID3_TAG_OPTION_ID3V1, ID3_TAG_OPTION_ID3V1) < 0) return 2;
    if (id3_tag_render(tag, data) != sizeof data) return 3;
    if (memcmp(data, "TAG", 3) != 0) return 4;
    parsed = id3_tag_parse(data, sizeof data);
    if (!parsed) return 5;
    if (id3_tag_render(parsed, rendered) != sizeof rendered) return 6;
    if (memcmp(data, rendered, sizeof data) != 0) return 7;
    id3_tag_delete(parsed);
    id3_tag_delete(tag);
    return 0;
}
EOF
cc "$smoke_dir/id3tag-smoke.c" -o "$smoke_dir/id3tag-smoke" \
  $({ pkg-config --cflags --libs id3tag; })
"$smoke_dir/id3tag-smoke"
