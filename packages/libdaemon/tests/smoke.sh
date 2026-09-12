#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdaemon libdaemon-devel
pkg-config --modversion libdaemon | grep -Fx '0.14'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libdaemon-smoke.c" <<'EOF'
#include <fcntl.h>
#include <libdaemon/daemon.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    int fds[2];
    char executable[] = "/usr/bin/libdaemon-smoke";

    if (strcmp(daemon_ident_from_argv0(executable), "libdaemon-smoke") != 0)
        return 1;
    if (pipe(fds) != 0)
        return 2;
    if (daemon_nonblock(fds[0], 1) != 0 ||
        (fcntl(fds[0], F_GETFL) & O_NONBLOCK) == 0 ||
        daemon_nonblock(fds[0], 0) != 0) {
        close(fds[0]);
        close(fds[1]);
        return 3;
    }
    close(fds[0]);
    close(fds[1]);
    return 0;
}
EOF

${CC:-cc} ${CFLAGS:-} "$smoke_dir/libdaemon-smoke.c" \
  $(pkg-config --cflags --libs libdaemon) -o "$smoke_dir/libdaemon-smoke"
"$smoke_dir/libdaemon-smoke"
