#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libatomic-queue libatomic-queue-tests
test "$(rpm -q --qf '%{VERSION}' libatomic-queue)" = 1.9.4
test "$(rpm -q --qf '%{ARCH}' libatomic-queue)" = noarch
printf '%s  %s\n' 22e4fce4f072000d810546875f26ad1e8b23fcb942fe0a00c85602eb3626c1bb /usr/share/licenses/libatomic-queue/LICENSE | sha256sum -c -
bash /usr/share/libatomic-queue/tests/run-tests.sh
