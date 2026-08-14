#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- python3-six
python3 - <<'PY'
import six
from six.moves.urllib.parse import urlsplit

assert six.__version__ == "1.17.0"
parts = urlsplit("https://openeuler.org/riscv")
assert parts.scheme == "https"
assert parts.netloc == "openeuler.org"
assert parts.path == "/riscv"
PY
