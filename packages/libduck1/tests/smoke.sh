#!/usr/bin/env bash
set -euo pipefail
rpm -q libduck1 libduck1-devel
rpm -V libduck1 libduck1-devel
bash /usr/share/libduck1/tests/run-checks.sh
