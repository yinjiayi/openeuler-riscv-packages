#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- recode recode-devel recode-help
recode --version | grep -F 'recode 3.7.17'

converted=$(printf '\351\n' | recode ISO-8859-1..UTF-8 | od -An -tx1 | tr -d ' \n')
test "$converted" = 'c3a90a'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/recode-smoke.c" <<'EOF'
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <recode.h>

int main(void) {
    RECODE_OUTER outer = recode_new_outer(0);
    if (outer == NULL) {
        return 1;
    }
    return recode_delete_outer(outer) ? 0 : 2;
}
EOF
cc "$smoke_dir/recode-smoke.c" -o "$smoke_dir/recode-smoke" -lrecode
"$smoke_dir/recode-smoke"

# RPMFILE_LICENSE is bit 7. Resolve paths from each package's own file list
# rather than assuming an RPM vendor's license-directory layout.
for package in recode recode-devel recode-help; do
    owned_files=$(rpm -q --qf '[%{FILENAMES} %{FILEFLAGS}\n]' -- "$package")
    while read -r expected filename; do
        matches=0
        licensed_path=
        while read -r path flags; do
            [[ "$flags" =~ ^[0-9]+$ ]]
            if [[ "${path##*/}" == "$filename" ]] && (( (10#$flags & 128) != 0 )); then
                matches=$((matches + 1))
                licensed_path=$path
            fi
        done <<< "$owned_files"
        test "$matches" -eq 1
        test -f "$licensed_path"
        test ! -L "$licensed_path"
        printf '%s  %s\n' "$expected" "$licensed_path" | sha256sum --check --strict
    done <<'EOF'
8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903 COPYING
da7eabb7bafdf7d3ae5e9f223aa5bdc1eece45ac569dc21b3b037520b4464768 COPYING-LIB
736fa08bdb4b3549a31b76bba5ee22316ff0e691210493289b06e642e08c4119 ansellat1.l
6aa6443e4a26b3ed8b5a7ca151de0e5648bda0ce5fd2da1b766b5c40053b8709 iso5426lat1.l
16c730e720b13f2facc1061f2586093fade1bfcde4ab553053efcade2d7a94e4 merged.c
EOF
done
