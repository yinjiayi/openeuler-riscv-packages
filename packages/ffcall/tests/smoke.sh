#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- ffcall ffcall-devel ffcall-static
for archive in \
  libavcall.a \
  libcallback.a \
  libffcall.a \
  libtrampoline.a \
  libvacall.a
do
  test -f "/usr/lib64/$archive"
done

for soname in \
  libavcall.so.1 \
  libcallback.so.1 \
  libffcall.so.0 \
  libtrampoline.so.1
do
  ldconfig -p | grep -F "$soname"
done

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <avcall.h>
#include <ffcall-version.h>

static int add(int left, int right)
{
    return left + right;
}

int main(void)
{
    av_alist arguments;
    int result = 0;

    if (LIBFFCALL_VERSION != 0x0205) {
        return 1;
    }
    av_start_int(arguments, add, &result);
    av_int(arguments, 19);
    av_int(arguments, 23);
    if (av_call(arguments) != 0) {
        return 2;
    }
    return result == 42 ? 0 : 3;
}
EOF

${CC:-cc} ${CFLAGS:-} -Wall -Wextra -Werror \
  "$smoke_dir/smoke.c" -lffcall -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
