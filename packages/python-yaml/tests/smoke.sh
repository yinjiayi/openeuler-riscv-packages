#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- python3-pyyaml
python3 - <<'PY'
import yaml
import yaml._yaml

assert yaml.__version__ == "6.0.3"
assert yaml.__with_libyaml__
document = yaml.safe_load("target: riscv64\nisa: RVA23\n")
assert document == {"target": "riscv64", "isa": "RVA23"}
encoded = yaml.safe_dump(document, sort_keys=True)
assert yaml.safe_load(encoded) == document
PY
