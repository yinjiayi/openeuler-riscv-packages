#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libmsnumpress libmsnumpress-devel libmsnumpress-static
rpm -V libmsnumpress libmsnumpress-devel libmsnumpress-static
bash /usr/share/libmsnumpress/tests/run-tests.sh /
